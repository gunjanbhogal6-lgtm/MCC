"""
Stage 0: Data Collection - Multi-source data ingestion
Collects data from Google Search Console, SERP API, and keyword research tools
"""

import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..connectors.search_console import SearchConsoleConnector
from ..connectors.serpapi import SERPApiConnector
from ..utils.keyword_intelligence import KeywordIntelligenceEngine
from ..utils.competitor_intelligence import CompetitorIntelligence
from ..utils.config import get_config
from ..utils.logger import get_logger
from .ingest import IngestResult


@dataclass
class DataCollectionResult:
    """Result of the data collection stage"""
    success: bool
    gsc_data: Optional[Dict] = None
    serp_data: Optional[Dict] = None
    keyword_intelligence: Optional[Dict] = None
    competitor_intelligence: Optional[Dict] = None
    merged_dataset: Optional[List[Dict]] = None
    errors: List[str] = field(default_factory=list)
    cache_file: Optional[str] = None


class DataCollectionStage:
    """
    Stage 0: Data Collection and Intelligence Gathering
    
    Collects SEO data from multiple sources and generates comprehensive intelligence.
    """
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self._gsc_connector = SearchConsoleConnector()
        self._serp_connector = SERPApiConnector()
        self._keyword_engine = KeywordIntelligenceEngine()
        self._competitor_engine = CompetitorIntelligence()
        
    def collect_all_data(
        self,
        domain: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        enable_gsc: bool = True,
        enable_serp: bool = True,
        sample_serp_keywords: int = 20
    ) -> DataCollectionResult:
        """
        Collect data from all enabled sources.
        
        Args:
            domain: Domain to analyze
            start_date: Start date for data collection (YYYY-MM-DD)
            end_date: End date for data collection (YYYY-MM-DD)
            enable_gsc: Enable Google Search Console collection
            enable_serp: Enable SERP API collection
            sample_serp_keywords: Number of keywords to sample for SERP analysis (SerpAPI has rate limits)
        
        Returns:
            DataCollectionResult with comprehensive data
        """
        self.logger.stage("DATA COLLECTION", "Starting comprehensive SEO data collection...")
        
        result = DataCollectionResult(success=False)
        
        # Step 1: Collect GSC data
        gsc_data = None
        if enable_gsc:
            try:
                self.logger.info("Collecting Google Search Console data...")
                gsc_data = self._collect_gsc_data(
                    domain=domain,
                    start_date=start_date,
                    end_date=end_date
                )
                result.gsc_data = gsc_data
                self.logger.success(f"Collected {len(gsc_data.get('keyword_performance', []))} keywords from GSC")
            except Exception as e:
                error_msg = f"GSC data collection failed: {str(e)}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
        
        # Step 2: Collect SERP data for top keywords
        serp_data = None
        if enable_serp:
            try:
                self.logger.info("Collecting SERP feature data...")
                
                # Get top keywords to analyze
                top_keywords = []
                if gsc_data:
                    top_keywords = [
                        k['query'] for k in gsc_data.get('keyword_performance', [])[:sample_serp_keywords]
                    ]
                
                if top_keywords:
                    serp_data = self._collect_serp_data(top_keywords)
                    result.serp_data = serp_data
                    self.logger.success(f"Collected SERP data for {len(serp_data)} keywords")
                else:
                    self.logger.warning("No keywords available for SERP analysis")
            except Exception as e:
                error_msg = f"SERP data collection failed: {str(e)}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
        
        # Step 3: Generate keyword intelligence
        keyword_intelligence = None
        if gsc_data:
            try:
                self.logger.info("Generating keyword intelligence...")
                
                # Format GSC data for keyword engine
                keyword_dataset = self._format_gsc_for_intelligence(gsc_data)
                
                # Add SERP data if available
                if serp_data:
                    for kw in keyword_dataset:
                        serp_info = serp_data.get(kw['Keyword'], {})
                        kw['SERP Features by Keyword'] = ', '.join(serp_info.get('features_present', []))
                
                keyword_intelligence = self._keyword_engine.analyze_keyword_portfolio(keyword_dataset)
                result.keyword_intelligence = keyword_intelligence
                self.logger.success("Generated keyword intelligence analysis")
            except Exception as e:
                error_msg = f"Keyword intelligence generation failed: {str(e)}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
        
        # Step 4: Generate competitor intelligence
        competitor_intelligence = None
        if gsc_data:
            try:
                self.logger.info("Generating competitor intelligence...")
                
                # Format data for competitor analysis
                keyword_dataset = self._format_gsc_for_intelligence(gsc_data)
                
                # Build competitor data from GSC (simulated)
                competitor_data = self._build_competitor_data_from_gsc(gsc_data, domain)
                
                competitor_intelligence = self._competitor_engine.analyze_competitors(
                    domain=domain,
                    competitor_data=competitor_data,
                    keyword_universe=keyword_dataset
                )
                result.competitor_intelligence = competitor_intelligence
                self.logger.success("Generated competitor intelligence")
            except Exception as e:
                error_msg = f"Competitor intelligence generation failed: {str(e)}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
        
        # Step 5: Merge all data into unified dataset
        if gsc_data or serp_data:
            try:
                self.logger.info("Merging all data sources...")
                merged = self._merge_all_data(
                    gsc_data=gsc_data,
                    serp_data=serp_data,
                    keyword_intelligence=keyword_intelligence
                )
                result.merged_dataset = merged
                
                # Cache merged data
                cache_file = self._cache_merged_data(merged, domain)
                result.cache_file = cache_file
                
                self.logger.success(f"Merged dataset contains {len(merged)} comprehensive data points")
            except Exception as e:
                error_msg = f"Data merging failed: {str(e)}"
                self.logger.error(error_msg)
                result.errors.append(error_msg)
        
        result.success = True
        return result
    
    def _collect_gsc_data(
        self,
        domain: str,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> Dict:
        """Collect comprehensive data from Google Search Console"""
        with self._gsc_connector as connector:
            if not connector.service:
                raise Exception("Failed to connect to Search Console")
            
            # Get keyword performance
            keyword_performance = connector.get_keyword_performance(
                site_url=f"https://{domain}",
                start_date=start_date,
                end_date=end_date
            )
            
            # Get page performance
            page_performance = connector.get_page_performance(
                site_url=f"https://{domain}",
                start_date=start_date,
                end_date=end_date
            )
            
            # Get mobile vs desktop comparison
            mobile_desktop = connector.get_mobile_vs_desktop(
                site_url=f"https://{domain}",
                start_date=start_date,
                end_date=end_date
            )
            
            # Get trending keywords
            trending_keywords = connector.get_trending_keywords(
                site_url=f"https://{domain}",
                days_back=7
            )
            
            return {
                'domain': domain,
                'collection_date': datetime.now().isoformat(),
                'date_range': {
                    'start': start_date,
                    'end': end_date
                },
                'keyword_performance': keyword_performance,
                'page_performance': page_performance,
                'device_comparison': mobile_desktop,
                'trending_keywords': trending_keywords,
                'summary': {
                    'total_keywords': len(keyword_performance),
                    'total_pages': len(page_performance),
                    'total_impressions': sum(k.get('impressions', 0) for k in keyword_performance),
                    'total_clicks': sum(k.get('clicks', 0) for k in keyword_performance),
                    'avg_position': (
                        sum(k.get('position', 0) for k in keyword_performance) / len(keyword_performance)
                        if keyword_performance else 0
                    )
                }
            }
    
    def _collect_serp_data(self, keywords: List[str]) -> Dict:
        """Collect SERP feature data for keywords"""
        with self._serp_connector as connector:
            if not connector.is_authenticated:
                raise Exception("Failed to authenticate with SERP API")
            
            serp_features = {}
            
            for keyword in keywords:
                features = connector.get_serp_features(keyword)
                serp_features[keyword] = features
            
            return serp_features
    
    def _format_gsc_for_intelligence(self, gsc_data: Dict) -> List[Dict]:
        """Format GSC data for keyword intelligence engine"""
        keyword_data = []
        
        for row in gsc_data.get('keyword_performance', []):
            keyword_data.append({
                'Keyword': row.get('query', ''),
                'volume': row.get('impressions', 0),  # Use impressions as proxy for volume
                'difficulty': 0,  # Not available in GSC, will use position as proxy
                'CPC': 0,  # Not available in GSC
                'Position': row.get('position', 0),
                'URL': row.get('page', ''),
                'Trends': {},  # Not available in basic GSC
                'Keyword Intents': self._classify_intent_from_position(row.get('position', 0)),
                'SERP Features by Keyword': '',  # Will be filled from SERP data
                'clicks': row.get('clicks', 0),
                'ctr': row.get('ctr', 0),
                'impressions': row.get('impressions', 0)
            })
        
        return keyword_data
    
    def _classify_intent_from_position(self, position: int) -> str:
        """Simple intent classification based on position"""
        if position <= 3:
            return 'transactional'
        elif position <= 10:
            return 'informational'
        else:
            return 'informational'
    
    def _build_competitor_data_from_gsc(self, gsc_data: Dict, our_domain: str) -> List[Dict]:
        """Build competitor data from GSC (simulated, would use competitor APIs in production)"""
        # This is a placeholder - in production you'd use Ahrefs, SEMrush, etc.
        # For now, we'll just return empty data
        return []
    
    def _merge_all_data(
        self,
        gsc_data: Optional[Dict],
        serp_data: Optional[Dict],
        keyword_intelligence: Optional[Dict]
    ) -> List[Dict]:
        """Merge all data sources into unified dataset"""
        if not gsc_data:
            return []
        
        merged = []
        
        for gsc_row in gsc_data.get('keyword_performance', []):
            keyword = gsc_row.get('query', '')
            
            # Base data from GSC
            merged_row = {
                'keyword': keyword,
                'page': gsc_row.get('page', ''),
                'impressions': gsc_row.get('impressions', 0),
                'clicks': gsc_row.get('clicks', 0),
                'ctr': gsc_row.get('ctr', 0),
                'position': gsc_row.get('position', 0),
                'country': gsc_row.get('country', 'unknown'),
                'device': gsc_row.get('device', 'unknown')
            }
            
            # Add SERP features if available
            if serp_data and keyword in serp_data:
                features = serp_data[keyword]
                merged_row['serp_features'] = features.get('features_present', [])
                merged_row['has_featured_snippet'] = features.get('featured_snippet') is not None
                merged_row['snippet_type'] = features.get('featured_snippet', {}).get('type') if features.get('featured_snippet') else None
            
            # Add keyword intelligence if available
            if keyword_intelligence:
                # Look for keyword in various intelligence outputs
                quick_wins = keyword_intelligence.get('quick_wins', [])
                kw_quick_win = next((kw for kw in quick_wins if kw.get('keyword') == keyword), None)
                
                if kw_quick_win:
                    merged_row['priority_score'] = kw_quick_win.get('priority_score', 0)
                    merged_row['is_quick_win'] = True
                else:
                    merged_row['is_quick_win'] = False
                
                # Add intent classification
                intent_dist = keyword_intelligence.get('intent_distribution', {})
                # Simple intent inference
                if merged_row['position'] <= 3 and merged_row['clicks'] > merged_row['impressions'] * 0.1:
                    merged_row['intent'] = 'transactional'
                else:
                    merged_row['intent'] = 'informational'
            
            # Calculate opportunity score
            volume = merged_row['impressions']
            position = merged_row['position']
            
            if position > 0 and volume > 0:
                # Opportunity = (volume * (100 - position * 10)) / 100, capped at 100
                position_factor = max(0, 100 - position * 10)
                merged_row['opportunity_score'] = round((volume * position_factor) / 100, 2)
            else:
                merged_row['opportunity_score'] = 0
            
            merged.append(merged_row)
        
        # Sort by opportunity score
        merged.sort(key=lambda x: x.get('opportunity_score', 0), reverse=True)
        
        return merged
    
    def _cache_merged_data(self, merged_data: List[Dict], domain: str) -> str:
        """Cache merged data to file"""
        cache_dir = self.config.cache_dir
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cache_file = os.path.join(cache_dir, f"merged_data_{domain}_{timestamp}.json")
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2)
        
        return cache_file
    
    def get_status(self) -> Dict:
        """Get current data collection status"""
        return {
            'gsc_authenticated': self._gsc_connector.is_authenticated,
            'serp_authenticated': self._serp_connector.is_authenticated,
            'gsc_rate_limit': self._gsc_connector.get_rate_limit_info() if self._gsc_connector.service else {},
            'serp_rate_limit': self._serp_connector.get_rate_limit_info() if self._serp_connector.is_authenticated else {}
        }