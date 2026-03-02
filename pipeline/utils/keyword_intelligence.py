"""
Advanced Keyword Intelligence Engine
Provides sophisticated keyword analysis beyond basic scoring
"""

import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
from ..utils.logger import get_logger


class KeywordIntelligenceEngine:
    """Advanced keyword analysis including clustering, intent, and opportunity scoring"""
    
    INTENT_MAPPING = {
        'informational': ['how to', 'what is', 'why', 'guide', 'tutorial', 'learn', 'understand', 'explain', 'definition', 'meaning'],
        'transactional': ['buy', 'purchase', 'price', 'cost', 'cheap', 'discount', 'deal', 'best', 'top', 'review', 'comparison', 'vs'],
        'navigational': ['login', 'sign in', 'website', 'official site', 'app', 'download'],
        'commercial': ['services', 'companies', 'near me', 'location', 'contact', 'quote', 'consultation']
    }
    
    def __init__(self):
        self.logger = get_logger()
    
    def analyze_keyword_portfolio(self, keywords: List[Dict]) -> Dict:
        """
        Complete analysis of keyword portfolio.
        
        Args:
            keywords: List of keyword data dicts with required fields
        
        Returns:
            Comprehensive keyword analysis
        """
        if not keywords:
            return {}
        
        analysis = {
            'portfolio_summary': self.get_summary_stats(keywords),
            'intent_distribution': self.classify_all_intents(keywords),
            'topic_clusters': self.generate_clusters(keywords),
            'keyword_cannibalization': self.detect_cannibalization(keywords),
            'long_tail_opportunities': self.identify_long_tail(keywords),
            'quick_wins': self.identify_quick_wins(keywords),
            'high_value_targets': self.identify_high_value(keywords),
            'seasonal_patterns': self.detect_seasonality(keywords),
            'serp_feature_opportunities': self.analyze_serp_features(keywords),
            'click_potential': self.calculate_click_potential(keywords),
            'conversion_probability': self.estimate_conversion(keywords)
        }
        
        return analysis
    
    def get_summary_stats(self, keywords: List[Dict]) -> Dict:
        """Get portfolio summary statistics"""
        total_keywords = len(keywords)
        
        if total_keywords == 0:
            return {}
        
        total_volume = sum(k.get('volume', k.get('Search Volume', 0)) for k in keywords)
        avg_position = sum(k.get('position', k.get('Position', 0)) for k in keywords) / total_keywords
        avg_difficulty = sum(k.get('difficulty', k.get('Keyword Difficulty', 0)) for k in keywords) / total_keywords
        
        position_distribution = Counter(k.get('position', k.get('Position', 0)) for k in keywords)
        
        return {
            'total_keywords': total_keywords,
            'total_search_volume': total_volume,
            'average_position': round(avg_position, 1),
            'average_difficulty': round(avg_difficulty, 1),
            'keywords_in_top_3': position_distribution[1] + position_distribution[2] + position_distribution[3],
            'keywords_in_top_10': sum(count for pos, count in position_distribution.items() if pos <= 10),
            'keywords_missing_rankings': position_distribution.get(0, 0)
        }
    
    def classify_intent(self, keyword: str) -> str:
        """
        Classify search intent for a single keyword.
        
        Args:
            keyword: Keyword string
        
        Returns:
            Intent classification (informational, transactional, navigational, commercial)
        """
        keyword_lower = keyword.lower()
        intent_scores = {intent: 0 for intent in self.INTENT_MAPPING}
        
        # Score each intent based on keyword phrases
        for intent, phrases in self.INTENT_MAPPING.items():
            for phrase in phrases:
                if phrase in keyword_lower:
                    intent_scores[intent] += 1
        
        # Get highest scoring intent
        max_intent = max(intent_scores, key=intent_scores.get)
        if intent_scores[max_intent] == 0:
            return 'informational'  # Default
        
        return max_intent
    
    def classify_all_intents(self, keywords: List[Dict]) -> Dict:
        """Classify intent for all keywords"""
        intent_counts = Counter()
        
        for kw in keywords:
            keyword_text = kw.get('Keyword', kw.get('keyword', ''))
            if keyword_text:
                intent = self.classify_intent(keyword_text)
                intent_counts[intent] += 1
        
        total = sum(intent_counts.values())
        
        return {
            'distribution': dict(intent_counts),
            'percentages': {
                intent: round((count / total) * 100, 1) if total > 0 else 0
                for intent, count in intent_counts.items()
            }
        }
    
    def generate_clusters(self, keywords: List[Dict]) -> List[Dict]:
        """
        Generate topic clusters from keywords using semantic similarity.
        
        Args:
            keywords: List of keyword data
        
        Returns:
            List of topic clusters
        """
        if not keywords:
            return []
        
        # Extract keyword text
        keyword_texts = [
            kw.get('Keyword', kw.get('keyword', '')).lower()
            for kw in keywords
            if kw.get('Keyword', kw.get('keyword', ''))
        ]
        
        # Simple clustering based on common words
        clusters = []
        used_indices = set()
        
        for i, keyword1 in enumerate(keyword_texts):
            if i in used_indices:
                continue
            
            # Find similar keywords
            similar_indices = []
            words1 = set(keyword1.split())
            
            for j, keyword2 in enumerate(keyword_texts):
                if i == j or j in used_indices:
                    continue
                
                words2 = set(keyword2.split())
                
                # Calculate Jaccard similarity
                intersection = len(words1 & words2)
                union = len(words1 | words2)
                similarity = intersection / union if union > 0 else 0
                
                if similarity >= 0.3:  # 30% similarity threshold
                    similar_indices.append(j)
            
            # Create cluster if we have at least 2 keywords
            if similar_indices:
                cluster_keywords = [
                    keywords[idx] for idx in [i] + similar_indices
                ]
                
                # Extract common topic
                all_words = []
                for kw in cluster_keywords:
                    kw_text = kw.get('Keyword', kw.get('keyword', ''))
                    all_words.extend(kw_text.split())
                
                word_counts = Counter(all_words)
                topic = word_counts.most_common(1)[0][0] if word_counts else 'general'
                
                # Calculate cluster metrics
                total_volume = sum(
                    kw.get('volume', kw.get('Search Volume', 0))
                    for kw in cluster_keywords
                )
                avg_position = sum(
                    kw.get('position', kw.get('Position', 99))
                    for kw in cluster_keywords
                ) / len(cluster_keywords)
                
                clusters.append({
                    'topic': topic,
                    'keyword_count': len(cluster_keywords),
                    'total_search_volume': total_volume,
                    'average_position': round(avg_position, 1),
                    'keywords': cluster_keywords
                })
                
                # Mark all used
                used_indices.update([i] + similar_indices)
        
        # Remaining unclustered keywords
        remaining = [
            keywords[idx] for idx in range(len(keywords)) if idx not in used_indices
        ]
        
        if remaining:
            clusters.append({
                'topic': 'miscellaneous',
                'keyword_count': len(remaining),
                'total_search_volume': sum(
                    kw.get('volume', kw.get('Search Volume', 0)) for kw in remaining
                ),
                'average_position': (
                    sum(kw.get('position', kw.get('Position', 99)) for kw in remaining) / len(remaining)
                    if remaining else 0
                ),
                'keywords': remaining
            })
        
        # Sort clusters by volume
        clusters.sort(key=lambda x: x['total_search_volume'], reverse=True)
        
        return clusters[:10]  # Top 10 clusters
    
    def detect_cannibalization(self, keywords: List[Dict]) -> List[Dict]:
        """
        Detect keyword cannibalization (multiple URLs for same intent).
        
        Args:
            keywords: List of keyword data with URLs
        
        Returns:
            List of cannibalization issues
        """
        # Group by simplified keyword (remove stop words, singular/plural)
        keyword_url_map = {}
        
        for kw in keywords:
            keyword_text = kw.get('Keyword', kw.get('keyword', ''))
            url = kw.get('URL', kw.get('url', ''))
            
            if not keyword_text or not url:
                continue
            
            # Normalize keyword
            normalized = self._normalize_keyword(keyword_text)
            
            if normalized not in keyword_url_map:
                keyword_url_map[normalized] = []
            
            keyword_url_map[normalized].append({
                'keyword': keyword_text,
                'url': url,
                'position': kw.get('position', kw.get('Position', 0))
            })
        
        # Find cannibalization
        cannibalizations = []
        for normalized_keyword, entries in keyword_url_map.items():
            urls = set(e['url'] for e in entries)
            
            if len(urls) > 1:
                # Multiple URLs ranking for similar keyword
                cannibalizations.append({
                    'keyword_group': normalized_keyword,
                    'affected_keywords': [e['keyword'] for e in entries],
                    'competing_urls': list(urls),
                    'best_position': min(e['position'] for e in entries),
                    'recommendation': f"Consolidate ranking authority to one URL for these variations"
                })
        
        return canonical_keywords
    
    def _normalize_keyword(self, keyword: str) -> str:
        """Normalize keyword for grouping"""
        # Remove common words and normalize
        stop_words = {'the', 'a', 'an', 'and', 'or', 'to', 'for', 'in', 'on', 'at', 'by'}
        words = keyword.lower().split()
        filtered = [w for w in words if w not in stop_words]
        
        # Simple singular/plural handling
        normalized = []
        for word in filtered:
            if word.endswith('s') and len(word) > 3:
                normalized.append(word[:-1])
            else:
                normalized.append(word)
        
        return ' '.join(normalized)
    
    def identify_long_tail(self, keywords: List[Dict]) -> List[Dict]:
        """
        Identify long-tail keyword opportunities.
        
        Long-tail = 3+ words, lower competition but higher intent
        
        Args:
            keywords: List of keyword data
        
        Returns:
            List of long-tail opportunities
        """
        long_tail = []
        
        for kw in keywords:
            keyword_text = kw.get('Keyword', kw.get('keyword', ''))
            word_count = len(keyword_text.split())
            
            if word_count >= 3:
                long_tail.append({
                    'keyword': keyword_text,
                    'word_count': word_count,
                    'volume': kw.get('volume', kw.get('Search Volume', 0)),
                    'difficulty': kw.get('difficulty', kw.get('Keyword Difficulty', 0)),
                    'position': kw.get('position', kw.get('Position', 0)),
                    'opportunity_score': self._calculate_opportunity_score(kw),
                    'intent': self.classify_intent(keyword_text)
                })
        
        # Sort by opportunity score
        long_tail.sort(key=lambda x: x['opportunity_score'], reverse=True)
        
        return long_tail[:50]  # Top 50 long-tail opportunities
    
    def identify_quick_wins(self, keywords: List[Dict]) -> List[Dict]:
        """
        Identify quick win opportunities (positions 4-15 with decent volume).
        
        Args:
            keywords: List of keyword data
        
        Returns:
            List of quick win opportunities
        """
        quick_wins = []
        
        for kw in keywords:
            position = kw.get('position', kw.get('Position', 0))
            volume = kw.get('volume', kw.get('Search Volume', 0))
            difficulty = kw.get('difficulty', kw.get('Keyword Difficulty', 0))
            
            # Quick win criteria
            if 4 <= position <= 15 and volume >= 500:
                quick_wins.append({
                    'keyword': kw.get('Keyword', kw.get('keyword', '')),
                    'current_position': position,
                    'search_volume': volume,
                    'keyword_difficulty': difficulty,
                    'potential_traffic_lift': self._estimate_traffic_potential(position, volume),
                    'optimization_effort': self._estimate_effort(position, difficulty),
                    'priority_score': self._calculate_priority_score(position, volume, difficulty)
                })
        
        # Sort by priority score
        quick_wins.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return quick_wins[:30]
    
    def identify_high_value(self, keywords: List[Dict]) -> List[Dict]:
        """
        Identify high-value target keywords (high volume, reasonable difficulty).
        
        Args:
            keywords: List of keyword data
        
        Returns:
            List of high-value targets
        """
        high_value = []
        
        for kw in keywords:
            volume = kw.get('volume', kw.get('Search Volume', 0))
            difficulty = kw.get('difficulty', kw.get('Keyword Difficulty', 0))
            position = kw.get('position', kw.get('Position', 0))
            cpc = kw.get('CPC', 0)
            
            # High value criteria
            if volume >= 1000 and difficulty <= 70 and cpc > 1:
                high_value.append({
                    'keyword': kw.get('Keyword', kw.get('keyword', '')),
                    'search_volume': volume,
                    'keyword_difficulty': difficulty,
                    'cost_per_click': cpc,
                    'commercial_value': volume * cpc,
                    'current_position': position,
                    'opportunity_score': self._calculate_opportunity_score(kw),
                    'intent': self.classify_intent(kw.get('Keyword', kw.get('keyword', '')))
                })
        
        # Sort by commercial value
        high_value.sort(key=lambda x: x['commercial_value'], reverse=True)
        
        return high_value[:25]
    
    def detect_seasonality(self, keywords: List[Dict]) -> List[Dict]:
        """
        Detect seasonal patterns in keywords.
        
        Args:
            keywords: List of keyword data with trend information
        
        Returns:
            List of seasonal keywords
        """
        seasonal = []
        
        for kw in keywords:
            trends = kw.get('Trends', {})
            
            if trends and isinstance(trends, dict) or isinstance(trends, list):
                # Look for significant variance
                trend_data = list(trends) if isinstance(trends, list) else trends.values()
                
                if len(trend_data) >= 3:
                    values = [float(v) for v in trend_data if str(v).replace('.', '').isdigit()]
                    
                    if values:
                        max_val = max(values)
                        min_val = min(values)
                        variance = (max_val - min_val) / max_val if max_val > 0 else 0
                        
                        # If variance > 50%, it's seasonal
                        if variance > 0.5:
                            seasonal.append({
                                'keyword': kw.get('Keyword', kw.get('keyword', '')),
                                'trend_variance': round(variance * 100, 1),
                                'peak_period': values.index(max_val),
                                'off_peak_period': values.index(min_val),
                                'recommendation': 'Plan seasonal content strategy'
                            })
        
        return seasonal[:20]
    
    def analyze_serp_features(self, keywords: List[Dict], serp_data: Optional[Dict] = None) -> List[Dict]:
        """
        Analyze SERP feature opportunities for keywords.
        
        Args:
            keywords: List of keyword data
            serp_data: Optional SERP feature data from SERP API
        
        Returns:
            List of SERP feature opportunities
        """
        opportunities = []
        
        for kw in keywords:
            keyword_text = kw.get('Keyword', kw.get('keyword', ''))
            position = kw.get('position', kw.get('Position', 0))
            volume = kw.get('volume', kw.get('Search Volume', 0))
            
            # Check if we have SERP data
            features = None
            if serp_data and keyword_text in serp_data:
                features = serp_data[keyword_text]
            
            # High opportunity: ranking well but no featured snippet
            if position <= 5 and features and not features.get('featured_snippet'):
                opportunities.append({
                    'keyword': keyword_text,
                    'current_position': position,
                    'volume': volume,
                    'opportunity': 'featured_snippet',
                    'reason': 'Ranking in top 5 but no featured snippet captured',
                    'priority': 'high'
                })
            
            # High opportunity: no local pack but local intent
            elif self._has_local_intent(keyword_text):
                opportunities.append({
                    'keyword': keyword_text,
                    'current_position': position,
                    'volume': volume,
                    'opportunity': 'local_pack',
                    'reason': 'Local intent detected',
                    'priority': 'medium'
                })
        
        return opportunities[:30]
    
    def calculate_click_potential(self, keywords: List[Dict]) -> Dict:
        """
        Calculate click potential for keywords based on SERP features and position.
        
        Args:
            keywords: List of keyword data
        
        Returns:
            Dictionary with click potential analysis
        """
        # CTR model based on position and SERP features
        ctr_model = {
            1: 0.28,  # Featured snippet can boost to ~40%
            2: 0.15,
            3: 0.11,
            4: 0.08,
            5: 0.07,
            6: 0.05,
            7: 0.04,
            8: 0.03,
            9: 0.02,
            10: 0.02
        }
        
        click_potential = {}
        
        for kw in keywords:
            keyword_text = kw.get('Keyword', kw.get('keyword', ''))
            position = kw.get('position', kw.get('Position', 0))
            
            # Base CTR from position
            base_ctr = ctr_model.get(position, 0.01)
            
            # Adjust for SERP features
            serp_features = kw.get('SERP Features by Keyword', '')
            has_featured_snippet = 'Featured snippet' in str(serp_features) if serp_features else False
            
            # Boost if we have featured snippet
            if has_featured_snippet and position == 1:
                base_ctr *= 1.4  # 40% boost
            
            click_potential[keyword_text] = {
                'current_position': position,
                'base_ctr': round(base_ctr * 100, 1),
                'has_featured_snippet': has_featured_snippet,
                'boosted_ctr': round(base_ctr * 100 * 1.4, 1) if has_featured_snippet and position == 1 else round(base_ctr * 100, 1),
                'potential_increase': 40 if has_featured_snippet and position == 1 else 0
            }
        
        return click_potential
    
    def estimate_conversion(self, keywords: List[Dict]) -> Dict:
        """
        Estimate conversion probability for keywords based on intent and commercial data.
        
        Args:
            keywords: List of keyword data
        
        Returns:
            Dictionary with conversion probability analysis
        """
        conversion_scores = {
            'transactional': 0.7,
            'commercial': 0.5,
            'navigational': 0.4,
            'informational': 0.15
        }
        
        conversion_probability = {}
        
        for kw in keywords:
            keyword_text = kw.get('Keyword', kw.get('keyword', ''))
            volume = kw.get('volume', kw.get('Search Volume', 0))
            cpc = kw.get('CPC', 0)
            
            # Base probability from intent
            intent = self.classify_intent(keyword_text)
            base_probability = conversion_scores.get(intent, 0.2)
            
            # Adjust based on CPC (higher CPC = more commercial)
            if cpc > 0:
                probability = base_probability * (1 + min(cpc / 10, 0.5))
            else:
                probability = base_probability
            
            conversion_probability[keyword_text] = {
                'intent': intent,
                'conversion_probability': round(probability * 100, 1),
                'commercial_signal': cpc,
                'estimated_conversions': round(volume * probability, 0),
                'revenue_potential': round(volume * probability * cpc, 0)
            }
        
        return conversion_probability
    
    def _calculate_opportunity_score(self, keyword: Dict) -> float:
        """Calculate overall opportunity score for a keyword"""
        volume = keyword.get('volume', keyword.get('Search Volume', 0))
        difficulty = keyword.get('difficulty', keyword.get('Keyword Difficulty', 0))
        
        if difficulty >= 100:
            difficulty = 99
        
        if volume == 0:
            return 0
        
        # Opportunity = (Volume * (100 - Difficulty)) / 100
        return (volume * (100 - difficulty)) / 100
    
    def _calculate_priority_score(self, position: int, volume: int, difficulty: int) -> float:
        """Calculate priority score for quick win ranking"""
        # High priority: low position, high volume, low difficulty
        position_score = (20 - position) * 5  # Max 100
        volume_score = min(volume / 100, 50)  # Max 50
        difficulty_score = (100 - difficulty) / 2  # Max 50
        
        return position_score + volume_score + difficulty_score
    
    def _estimate_traffic_potential(self, current_position: int, volume: int) -> int:
        """Estimate potential traffic gain from position improvement"""
        # CTR model
        ctr_model = {1: 0.28, 2: 0.15, 3: 0.11, 4: 0.08, 5: 0.07}
        
        current_ctr = ctr_model.get(current_position, 0.02)
        target_ctr = ctr_model.get(3, 0.11)  # Assume we can get to position 3
        
        potential = int(volume * (target_ctr - current_ctr))
        return max(potential, 0)
    
    def _estimate_effort(self, position: int, difficulty: int) -> str:
        """Estimate optimization effort"""
        if position <= 5:
            return 'low'
        elif position <= 10:
            return 'low'
        elif position <= 20:
            return 'medium'
        else:
            return 'high'
    
    def _has_local_intent(self, keyword: str) -> bool:
        """Check if keyword has local search intent"""
        local_indicators = ['near me', 'in', 'near', 'local', 'location', 'where', 'closest']
        keyword_lower = keyword.lower()
        return any(indicator in keyword_lower for indicator in local_indicators)