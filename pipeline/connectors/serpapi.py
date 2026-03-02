"""
SERP API Connector
Fetches SERP data, features, and competitor information
"""

import os
from typing import Dict, List, Optional
import requests
from .base_connector import BaseConnector


class SERPApiConnector(BaseConnector):
    """Connector for SERP API (serpapi.com)"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize SERP API connector.
        
        Args:
            api_key: SERP API key (or set SERPAPI_KEY env var)
        """
        super().__init__()
        self.api_key = api_key or os.getenv('SERPAPI_KEY')
        self.base_url = "https://serpapi.com/search"
        self.rate_limit_remaining = 100
        self.rate_limit_reset = None
    
    def authenticate(self) -> bool:
        """Check if API key is valid"""
        if not self.api_key:
            self.logger.error("SERP API key not provided")
            return False
        
        # Test with a simple query
        try:
            result = self.search("test", num=1, engine="google")
            if result.get('error'):
                self.logger.error(f"SERP API authentication failed: {result.get('error')}")
                return False
            
            self.is_authenticated = True
            self.logger.info("SERP API authenticated successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"SERP API authentication error: {e}")
            return False
    
    def search(
        self,
        query: str,
        num: int = 10,
        engine: str = "google",
        location: Optional[str] = None,
        google_domain: str = "google.com",
        device: str = "desktop"
    ) -> Dict:
        """
        Perform a SERP search.
        
        Args:
            query: Search query
            num: Number of results to return
            engine: Search engine (google, bing, etc.)
            location: Location for localized results
            google_domain: Google domain
            device: Device type (desktop, mobile)
        
        Returns:
            SERP results dictionary
        """
        if not self.is_authenticated:
            if not self.authenticate():
                return {}
        
        params = {
            "api_key": self.api_key,
            "engine": engine,
            "q": query,
            "num": num,
            "google_domain": google_domain,
            "device": device
        }
        
        if location:
            params["location"] = location
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Update rate limit info from headers
            if 'X-RateLimit-Remaining' in response.headers:
                self.rate_limit_remaining = int(response.headers['X-RateLimit-Remaining'])
            if 'X-RateLimit-Reset' in response.headers:
                self.rate_limit_reset = response.headers['X-RateLimit-Reset']
            
            return data
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"SERP API request failed: {e}")
            return {"error": str(e)}
    
    def get_serp_features(self, query: str) -> Dict:
        """
        Get all SERP features for a query.
        
        Args:
            query: Search query
        
        Returns:
            Dictionary of SERP features present
        """
        result = self.search(query, num=10)
        
        if result.get('error'):
            return {}
        
        features = {
            "featured_snippet": None,
            "people_also_ask": [],
            "related_questions": [],
            "knowledge_graph": None,
            "local_pack": [],
            "shopping_results": [],
            "image_results": [],
            "video_results": [],
            "news_results": [],
            "organic_results": result.get('organic_results', []),
            "paid_results": result.get('ads', []),
            "sitelinks": []
        }
        
        # Check for featured snippet
        if 'answer_box' in result:
            features['featured_snippet'] = {
                'type': result['answer_box'].get('type'),
                'title': result['answer_box'].get('title'),
                'answer': result['answer_box'].get('answer'),
                'link': result['answer_box'].get('link')
            }
        
        # People Also Ask
        if 'related_questions' in result:
            features['people_also_ask'] = result['related_questions']
        
        # Related Questions (different from PAA)
        if 'questions' in result:
            features['related_questions'] = result['questions']
        
        # Knowledge Graph
        if 'knowledge_graph' in result:
            features['knowledge_graph'] = {
                'title': result['knowledge_graph'].get('title'),
                'type': result['knowledge_graph'].get('type'),
                'description': result['knowledge_graph'].get('description')
            }
        
        # Local Pack
        if 'local_results' in result:
            features['local_pack'] = result['local_results']
        
        # Shopping Results
        if 'shopping_results' in result:
            features['shopping_results'] = result['shopping_results']
        
        # Image Results
        if 'images_results' in result:
            features['image_results'] = result['images_results']
        
        # Video Results
        if 'video_results' in result:
            features['video_results'] = result['video_results']
        
        # News Results
        if 'news_results' in result:
            features['news_results'] = result['news_results']
        
        # Sitelinks (from organic results)
        for organic in result.get('organic_results', []):
            if 'sitelinks' in organic:
                features['sitelinks'].extend(organic['sitelinks'])
        
        return features
    
    def get_competitor_analysis(self, query: str, top_n: int = 5) -> List[Dict]:
        """
        Get competitor analysis for a query.
        
        Args:
            query: Search query
            top_n: Number of top results to analyze
        
        Returns:
            List of competitor data
        """
        result = self.search(query, num=top_n)
        
        if result.get('error'):
            return []
        
        competitors = []
        for i, organic in enumerate(result.get('organic_results', []), 1):
            competitor = {
                'position': i,
                'title': organic.get('title', ''),
                'link': organic.get('link', ''),
                'snippet': organic.get('snippet', ''),
                'displayed_link': organic.get('displayed_link', ''),
                'favicon': organic.get('favicon', ''),
                'age': organic.get('age', None),
                'sitelinks': organic.get('sitelinks', []),
                'rich_snippet': organic.get('rich_snippet', {}),
                'cached_page_link': organic.get('cached_page_link', '')
            }
            competitors.append(competitor)
        
        return competitors
    
    def analyze_snippet_opportunity(self, query: str) -> Dict:
        """
        Analyze opportunity for featured snippet.
        
        Args:
            query: Search query
        
        Returns:
            Opportunity analysis
        """
        result = self.search(query, num=3)
        
        if result.get('error'):
            return {}
        
        analysis = {
            'has_featured_snippet': 'answer_box' in result,
            'featured_snippet_format': None,
            'competitors': [],
            'opportunity_score': 0,
            'recommended_format': None
        }
        
        # Get current snippet details
        if 'answer_box' in result:
            answer_box = result['answer_box']
            analysis['featured_snippet_format'] = answer_box.get('type', '')
            analysis['snippet_target'] = {
                'title': answer_box.get('title', ''),
                'link': answer_box.get('link', '')
            }
        else:
            # No snippet exists - opportunity!
            analysis['opportunity_score'] = 70  # Base score
            
            # Analyze top results to recommend format
            top_snippets = []
            for result_item in result.get('organic_results', [])[:5]:
                snippet_text = result_item.get('snippet', '')
                if ':' in snippet_text or ' - ' in snippet_text:
                    top_snippets.append('definition')
                elif snippet_text.count('\n') > 1:
                    top_snippets.append('list')
                elif '|' in snippet_text or snippet_text.count('\t') > 1:
                    top_snippets.append('table')
            
            # Recommend most common format
            if top_snippets:
                from collections import Counter
                format_counts = Counter(top_snippets)
                analysis['recommended_format'] = format_counts.most_common(1)[0][0]
            else:
                analysis['recommended_format'] = 'paragraph'
        
        # Get competitor data
        analysis['competitors'] = result.get('organic_results', [])[:5]
        
        # Adjust opportunity score based on position
        our_site = "salamtalk.com"  # Adjust based on target
        for i, comp in enumerate(result.get('organic_results', []), 1):
            if our_site in comp.get('link', ''):
                if i <= 3:
                    analysis['opportunity_score'] += 20
                elif i <= 5:
                    analysis['opportunity_score'] += 10
                break
        
        return analysis
    
    def get_related_keywords(self, query: str) -> List[str]:
        """
        Get related keywords from SERP.
        
        Args:
            query: Search query
        
        Returns:
            List of related keywords
        """
        result = self.search(query, num=10)
        
        if result.get('error'):
            return []
        
        related = set()
        
        # From related searches
        if 'related_searches' in result:
            for search in result['related_searches']:
                related.add(search.get('query', ''))
        
        # From people also ask questions
        if 'related_questions' in result:
            for qa in result['related_questions']:
                related.add(qa.get('question', ''))
        
        # From knowledge graph
        if 'knowledge_graph' in result:
            kg = result['knowledge_graph']
            if 'types' in kg:
                related.update(kg['types'])
            if 'description' in kg:
                # Extract potential keywords from description
                words = kg['description'].split()
                for word in words:
                    if len(word) > 4:
                        related.add(word.lower())
        
        return list(related)[:20]  # Top 20
    
    def get_rankings_for_keywords(
        self,
        keywords: List[str],
        domain: str
    ) -> List[Dict]:
        """
        Find rankings for specific domain across multiple keywords.
        
        Args:
            keywords: List of keywords to search
            domain: Domain to find rankings for
        
        Returns:
            List of ranking data
        """
        rankings = []
        
        for keyword in keywords:
            result = self.search(keyword, num=10)
            
            if result.get('error'):
                continue
            
            # Find our domain in results
            for i, organic in enumerate(result.get('organic_results', []), 1):
                if domain in organic.get('link', ''):
                    rankings.append({
                        'keyword': keyword,
                        'position': i,
                        'title': organic.get('title', ''),
                        'link': organic.get('link', ''),
                        'snippet': organic.get('snippet', ''),
                        'featured_snippet': 'answer_box' in result and result['answer_box'].get('link') == organic.get('link')
                    })
                    break
        
        return rankings
    
    def get_page_speed(self, url: str) -> Dict:
        """
        Get PageSpeed insights for a URL.
        
        Args:
            url: URL to analyze
        
        Returns:
            PageSpeed data
        """
        params = {
            "api_key": self.api_key,
            "url": url
        }
        
        try:
            response = requests.get(
                f"https://serpapi.com/search",
                params={**params, "engine": "google_page_speed_insights_mobile"},
                timeout=30
            )
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'mobile': data,
                'desktop': self._get_page_speed_desktop(url, params)
            }
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"PageSpeed API request failed: {e}")
            return {"error": str(e)}
    
    def _get_page_speed_desktop(self, url: str, base_params: Dict) -> Dict:
        """Helper to get desktop PageSpeed data"""
        try:
            response = requests.get(
                f"https://serpapi.com/search",
                params={**base_params, "engine": "google_page_speed_insights_desktop"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    def get_rate_limit_info(self) -> Dict:
        """Get rate limit information"""
        return {
            "connector": self.name,
            "rate_limit": "100 searches/month",
            "remaining": self.rate_limit_remaining,
            "reset": self.rate_limit_reset
        }