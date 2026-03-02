"""
Competitor Intelligence Module
Analyzes competitor strategies and identifies competitive opportunities
"""

from typing import Dict, List, Optional, Set
from collections import Counter
from ..utils.logger import get_logger


class CompetitorIntelligence:
    """Analyze competitor data and identify opportunities"""
    
    def __init__(self):
        self.logger = get_logger()
    
    def analyze_competitors(
        self,
        domain: str,
        competitor_data: List[Dict],
        keyword_universe: List[Dict]
    ) -> Dict:
        """
        Comprehensive competitor analysis.
        
        Args:
            domain: Our domain
            competitor_data: List of competitor keyword data
            keyword_universe: Full keyword dataset
        
        Returns:
            Competitor intelligence report
        """
        if not competitor_data or not keyword_universe:
            return {}
        
        # Identify top competitors
        top_competitors = self._identify_top_competitors(competitor_data)
        
        analysis = {
            'domain': domain,
            'top_competitors': top_competitors,
            'keyword_gaps': self.find_keyword_gaps(domain, competitor_data, keyword_universe),
            'content_gaps': self.find_content_gaps(domain, competitor_data),
            'backlink_gaps': self.analyze_backlink_gaps(domain, competitor_data),
            'authority_comparison': self.compare_authority(domain, competitor_data),
            'content_strategy_analysis': self.analyze_content_strategy(domain, competitor_data),
            'serp_feature_comparison': self.compare_serp_features(domain, competitor_data),
            'growth_opportunities': self.identify_growth_opportunities(domain, competitor_data, keyword_universe),
            'white_space': self.identify_white_space(domain, competitor_data, keyword_universe)
        }
        
        return analysis
    
    def _identify_top_competitors(self, competitor_data: List[Dict]) -> List[Dict]:
        """Identify top competitors by presence in SERP"""
        # Count occurrences of each competitor domain in top positions
        competitor_counts = Counter()
        
        for data in competitor_data:
            url = data.get('url', data.get('link', ''))
            position = data.get('position', 0)
            
            if url and position <= 10:
                # Extract domain
                domain = self._extract_domain(url)
                if domain and domain != data.get('our_domain', ''):
                    # Weight by position (position 1 gets more weight)
                    weight = 11 - position  # Position 1 = weight 10, position 10 = weight 1
                    competitor_counts[domain] += weight
        
        # Get top 5 competitors
        top_domains = [domain for domain, count in competitor_counts.most_common(5)]
        
        return [
            {
                'domain': domain,
                'relevance_score': count,
                'estimated_traffic_share': round(count / sum(competitor_counts.values()) * 100, 1)
            }
            for domain, count in competitor_counts.most_common(5)
        ]
    
    def find_keyword_gaps(
        self,
        our_domain: str,
        competitor_data: List[Dict],
        keyword_universe: List[Dict]
    ) -> List[Dict]:
        """
        Find keywords where competitors rank but we don't.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor keyword data
            keyword_universe: Full keyword dataset
        
        Returns:
            List of keyword gap opportunities
        """
        # Get competitor domains
        competitor_domains = set()
        for data in competitor_data:
            url = data.get('url', data.get('link', ''))
            if url:
                domain = self._extract_domain(url)
                if domain != our_domain:
                    competitor_domains.add(domain)
        
        # Find keywords we don't rank for but competitors do
        our_keywords = set()
        for kw in keyword_universe:
            url = kw.get('URL', kw.get('url', ''))
            if url and our_domain in url:
                our_keywords.add(kw.get('Keyword', kw.get('keyword', '')))
        
        gaps = []
        for kw in keyword_universe:
            keyword = kw.get('Keyword', kw.get('keyword', ''))
            
            if keyword in our_keywords:
                continue
            
            # Check if any competitor ranks well for this
            competitor_ranks = []
            for data in competitor_data:
                if data.get('Keyword', data.get('keyword', '')) == keyword:
                    url = data.get('url', data.get('link', ''))
                    if url and self._extract_domain(url) in competitor_domains:
                        position = data.get('position', data.get('Position', 0))
                        if position <= 10:
                            competitor_ranks.append({
                                'domain': self._extract_domain(url),
                                'position': position
                            })
            
            if competitor_ranks:
                # Sort by position
                competitor_ranks.sort(key=lambda x: x['position'])
                
                gaps.append({
                    'keyword': keyword,
                    'volume': kw.get('volume', kw.get('Search Volume', 0)),
                    'difficulty': kw.get('difficulty', kw.get('Keyword Difficulty', 0)),
                    'top_competitor': competitor_ranks[0]['domain'],
                    'competitor_position': competitor_ranks[0]['position'],
                    'all_competitors': competitor_ranks,
                    'priority_score': self._calculate_gap_priority(kw, competitor_ranks)
                })
        
        # Sort by priority
        gaps.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return gaps[:50]
    
    def find_content_gaps(
        self,
        our_domain: str,
        competitor_data: List[Dict]
    ) -> List[Dict]:
        """
        Find content topics competitors cover that we don't.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor data
        
        Returns:
            List of content gap opportunities
        """
        # Group competitor content by topic (using first 2 words of keyword)
        competitor_topics = set()
        our_topics = set()
        
        for data in competitor_data:
            url = data.get('url', data.get('link', ''))
            keyword = data.get('Keyword', data.get('keyword', ''))
            
            if not url or not keyword:
                continue
            
            domain = self._extract_domain(url)
            if domain == our_domain:
                # Extract topics from our keywords
                topics = self._extract_topics(keyword)
                our_topics.update(topics)
            else:
                # Extract topics from competitor keywords
                topics = self._extract_topics(keyword)
                competitor_topics.update(topics)
        
        # Find topics in competitors not in ours
        missing_topics = competitor_topics - our_topics
        
        content_gaps = []
        for topic in missing_topics[:20]:  # Top 20 missing topics
            content_gaps.append({
                'topic': topic,
                'coverage': self._estimate_topic_coverage(topic, competitor_data),
                'difficulty': 'medium',
                'priority': 'high' if len(topic.split()) == 1 else 'medium',
                'content_type': self._recommend_content_type(topic)
            })
        
        # Sort by coverage
        content_gaps.sort(key=lambda x: x['coverage'], reverse=True)
        
        return content_gaps[:15]
    
    def analyze_backlink_gaps(
        self,
        our_domain: str,
        competitor_data: List[Dict]
    ) -> Dict:
        """
        Analyze backlink gaps between us and competitors.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor data with backlink information
        
        Returns:
            Backlink gap analysis
        """
        # Aggregate backlink data
        our_backlinks = 0
        competitor_backlinks = {}
        
        for data in competitor_data:
            url = data.get('url', data.get('link', ''))
            domain = self._extract_domain(url) if url else None
            backlinks = data.get('backlinks', data.get('referring_domains', 0))
            
            if not domain:
                continue
            
            if domain == our_domain:
                our_backlinks = backlinks
            else:
                if domain not in competitor_backlinks:
                    competitor_backlinks[domain] = []
                competitor_backlinks[domain].append(backlinks)
        
        # Calculate average competitor backlinks
        avg_competitor_backlinks = 0
        if competitor_backlinks:
            total = sum(links[0] for links in competitor_backlinks.values() if links)
            avg_competitor_backlinks = total / len(competitor_backlinks)
        
        return {
            'our_backlinks': our_backlinks,
            'average_competitor_backlinks': round(avg_competitor_backlinks),
            'backlink_gap': round(avg_competitor_backlinks - our_backlinks),
            'gap_percentage': round(
                ((avg_competitor_backlinks - our_backlinks) / avg_competitor_backlinks * 100)
                if avg_competitor_backlinks > 0 else 0
            ),
            'priority': 'high' if avg_competitor_backlinks > our_backlinks * 1.5 else 'medium'
        }
    
    def compare_authority(
        self,
        our_domain: str,
        competitor_data: List[Dict]
    ) -> Dict:
        """
        Compare domain authority metrics.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor data
        
        Returns:
            Authority comparison
        """
        # Collect authority metrics
        our_authority = 0
        competitor_authorities = []
        
        for data in competitor_data:
            url = data.get('url', data.get('link', ''))
            domain = self._extract_domain(url) if url else None
            authority = data.get('domain_authority', data.get('da', 0))
            
            if not domain:
                continue
            
            if domain == our_domain:
                our_authority = authority
            else:
                competitor_authorities.append(authority)
        
        avg_competitor_authority = sum(competitor_authorities) / len(competitor_authorities) if competitor_authorities else 0
        
        return {
            'our_authority': our_authority,
            'average_competitor_authority': round(avg_competitor_authority, 1),
            'authority_gap': round(avg_competitor_authority - our_authority, 1),
            'percentile': round((our_authority / max(avg_competitor_authority, 1)) * 100, 1)
        }
    
    def analyze_content_strategy(
        self,
        our_domain: str,
        competitor_data: List[Dict]
    ) -> Dict:
        """
        Analyze competitor content strategies.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor data
        
        Returns:
            Content strategy analysis
        """
        # Analyze content types by keyword intent and format
        our_content_types = Counter()
        competitor_content_types = Counter()
        
        for data in competitor_data:
            url = data.get('url', data.get('link', ''))
            keyword = data.get('Keyword', data.get('keyword', ''))
            
            if not url or not keyword:
                continue
            
            domain = self._extract_domain(url)
            content_type = self._detect_content_type(url)
            
            if domain == our_domain:
                our_content_types[content_type] += 1
            else:
                competitor_content_types[content_type] += 1
        
        # Calculate content type distribution
        our_total = sum(our_content_types.values())
        competitor_total = sum(competitor_content_types.values())
        
        our_distribution = {
            ct: round(count / our_total * 100, 1) if our_total > 0 else 0
            for ct, count in our_content_types.items()
        }
        
        competitor_distribution = {
            ct: round(count / competitor_total * 100, 1) if competitor_total > 0 else 0
            for ct, count in competitor_content_types.items()
        }
        
        return {
            'our_content_distribution': our_distribution,
            'competitor_content_distribution': competitor_distribution,
            'content_differences': [
                {
                    'content_type': ct,
                    'our_percentage': our_distribution.get(ct, 0),
                    'competitor_percentage': competitor_distribution.get(ct, 0),
                    'gap': competitor_distribution.get(ct, 0) - our_distribution.get(ct, 0)
                }
                for ct in set(list(our_distribution.keys()) + list(competitor_distribution.keys()))
            ]
        }
    
    def compare_serp_features(
        self,
        our_domain: str,
        competitor_data: List[Dict]
    ) -> Dict:
        """
        Compare SERP feature capture between us and competitors.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor data with SERP features
        
        Returns:
            SERP feature comparison
        """
        # Count SERP features
        our_features = Counter()
        competitor_features = Counter()
        
        for data in competitor_data:
            url = data.get('url', data.get('link', ''))
            domain = self._extract_domain(url) if url else None
            features = data.get('SERP Features by Keyword', data.get('serp_features', ''))
            
            if not domain or not features:
                continue
            
            # Parse features
            feature_list = self._parse_serp_features(features)
            
            for feature in feature_list:
                if domain == our_domain:
                    our_features[feature] += 1
                else:
                    competitor_features[feature] += 1
        
        return {
            'our_features': dict(our_features),
            'competitor_features': dict(competitor_features),
            'feature_gaps': [
                {
                    'feature': feature,
                    'our_count': our_features.get(feature, 0),
                    'competitor_count': competitor_features.get(feature, 0),
                    'gap': competitor_features.get(feature, 0) - our_features.get(feature, 0)
                }
                for feature in set(list(our_features.keys()) + list(competitor_features.keys()))
            ]
        }
    
    def identify_growth_opportunities(
        self,
        our_domain: str,
        competitor_data: List[Dict],
        keyword_universe: List[Dict]
    ) -> List[Dict]:
        """
        Identify high-opportunity keywords where competition is weaker.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor data
            keyword_universe: Full keyword dataset
        
        Returns:
            List of growth opportunities
        """
        opportunities = []
        
        for kw in keyword_universe:
            keyword = kw.get('Keyword', kw.get('keyword', ''))
            volume = kw.get('volume', kw.get('Search Volume', 0))
            difficulty = kw.get('difficulty', kw.get('Keyword Difficulty', 0))
            
            # Get competitor positions for this keyword
            competitor_positions = []
            for data in competitor_data:
                if data.get('Keyword', data.get('keyword', '')) == keyword:
                    url = data.get('url', data.get('link', ''))
                    if url and self._extract_domain(url) != our_domain:
                        position = data.get('position', data.get('Position', 0))
                        competitor_positions.append(position)
            
            if competitor_positions:
                avg_competitor_position = sum(competitor_positions) / len(competitor_positions)
                
                # Opportunity: high competition (high positions) but reasonable difficulty
                if avg_competitor_position <= 5 and difficulty <= 60 and volume >= 500:
                    opportunities.append({
                        'keyword': keyword,
                        'search_volume': volume,
                        'keyword_difficulty': difficulty,
                        'avg_competitor_position': round(avg_competitor_position, 1),
                        'opportunity_score': round(volume / max(difficulty, 1), 0),
                        'recommendation': 'Investment recommended - high value, manageable difficulty'
                    })
        
        # Sort by opportunity score
        opportunities.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return opportunities[:30]
    
    def identify_white_space(
        self,
        our_domain: str,
        competitor_data: List[Dict],
        keyword_universe: List[Dict]
    ) -> List[Dict]:
        """
        Identify white space opportunities - low competition keywords.
        
        Args:
            our_domain: Our domain
            competitor_data: Competitor data
            keyword_universe: Full keyword dataset
        
        Returns:
            List of white space opportunities
        """
        white_space = []
        
        for kw in keyword_universe:
            keyword = kw.get('Keyword', kw.get('keyword', ''))
            volume = kw.get('volume', kw.get('Search Volume', 0))
            difficulty = kw.get('difficulty', kw.get('Keyword Difficulty', 0))
            
            # Check competition level
            competitors_ranking = 0
            for data in competitor_data:
                if data.get('Keyword', data.get('keyword', '')) == keyword:
                    url = data.get('url', data.get('link', ''))
                    if url and self._extract_domain(url) != our_domain:
                        position = data.get('position', data.get('Position', 0))
                        if position <= 10:
                            competitors_ranking += 1
            
            # White space: low competition but decent volume
            if competitors_ranking <= 2 and volume >= 200 and difficulty <= 40:
                white_space.append({
                    'keyword': keyword,
                    'search_volume': volume,
                    'keyword_difficulty': difficulty,
                    'competition_level': competitors_ranking,
                    'ease_score': round(volume / max(difficulty, 1) * (4 - competitors_ranking), 0),
                    'recommendation': 'Quick win - low competition, good volume'
                })
        
        # Sort by ease score
        white_space.sort(key=lambda x: x['ease_score'], reverse=True)
        
        return white_space[:25]
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        from urllib.parse import urlparse
        try:
            parsed = urlparse(url)
            return parsed.netloc.replace('www.', '')
        except Exception:
            return ''
    
    def _extract_topics(self, keyword: str) -> Set[str]:
        """Extract topics from keyword (first 2 words and combinations)"""
        words = keyword.split()
        topics = set()
        
        if len(words) >= 2:
            topics.add(f"{words[0]} {words[1]}")
            topics.add(words[0])
        
        return topics
    
    def _estimate_topic_coverage(self, topic: str, competitor_data: List[Dict]) -> int:
        """Estimate how many competitor keywords cover this topic"""
        count = 0
        topic_lower = topic.lower()
        
        for data in competitor_data:
            keyword = data.get('Keyword', data.get('keyword', '')).lower()
            if topic_lower in keyword:
                count += 1
        
        return count
    
    def _recommend_content_type(self, topic: str) -> str:
        """Recommend content type based on topic"""
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['how to', 'what is', 'why', 'guide']):
            return 'blog_post'
        elif any(word in topic_lower for word in ['best', 'top', 'vs', 'review']):
            return 'comparison_page'
        elif any(word in topic_lower for word in ['price', 'cost', 'buy', 'purchase']):
            return 'landing_page'
        elif '?' in topic_lower:
            return 'faq'
        else:
            return 'informational'
    
    def _detect_content_type(self, url: str) -> str:
        """Detect content type from URL"""
        url_lower = url.lower()
        
        if '/blog/' in url_lower or '/article/' in url_lower:
            return 'blog'
        elif '/product/' in url_lower or '/pricing/' in url_lower:
            return 'product'
        elif '/category/' in url_lower or '/tag/' in url_lower:
            return 'category'
        elif '/about/' in url_lower or '/contact/' in url_lower:
            return 'informational'
        elif '/faq/' in url_lower:
            return 'faq'
        else:
            return 'page'
    
    def _parse_serp_features(self, features_str: str) -> List[str]:
        """Parse SERP features string into list"""
        if not features_str:
            return []
        
        # Split by comma and clean
        features = [f.strip() for f in str(features_str).split(',')]
        
        # Common SERP features
        known_features = [
            'Featured snippet',
            'People also ask',
            'Local pack',
            'Image pack',
            'Video',
            'Top stories',
            'Sitelinks',
            'Reviews',
            'FAQ'
        ]
        
        # Filter to known features
        return [f for f in features if any(kf.lower() in f.lower() for kf in known_features)]
    
    def _calculate_gap_priority(self, keyword: Dict, competitor_ranks: List[Dict]) -> float:
        """Calculate priority score for keyword gap"""
        volume = keyword.get('volume', keyword.get('Search Volume', 0))
        difficulty = keyword.get('difficulty', keyword.get('Keyword Difficulty', 0))
        
        # Higher priority for keywords where competitors rank well but it's not too difficult
        avg_competitor_position = sum(r['position'] for r in competitor_ranks) / len(competitor_ranks)
        
        position_bonus = max(0, (10 - avg_competitor_position) * 10)  # Up to 100 points
        volume_score = min(volume / 100, 50)  # Up to 50 points
        difficulty_adjustment = max(0, (80 - difficulty) / 2)  # Up to 40 points
        
        return position_bonus + volume_score + difficulty_adjustment