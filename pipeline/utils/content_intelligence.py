"""
Content Intelligence Engine
Advanced NLP-based content analysis (better than WordPress plugins)
"""

import re
from typing import Dict, List, Tuple
from collections import Counter
from ..utils.logger import get_logger


class ContentIntelligenceEngine:
    """NLP-powered content analysis"""
    
    POWER_WORDS = [
        'amazing', 'ultimate', 'proven', 'exclusive', 'limited', 'free',
        'guaranteed', 'instant', 'powerful', 'effective', 'best', 'top',
        'secret', 'revolutionary', 'uncovered', 'discover', 'breakthrough',
        'essential', 'critical', 'must-have', 'incredible', 'extraordinary'
    ]
    
    STOP_WORDS_EN = [
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'it', 'its', 'i', 'you', 'he', 'she', 'we', 'they', 'what', 'which', 'who'
    ]
    
    def __init__(self):
        self.logger = get_logger()
    
    def analyze_content(self, content: str, target_keywords: List[str] = None) -> Dict:
        """
        Comprehensive content analysis.
        
        Args:
            content: Text content to analyze
            target_keywords: Target keywords to check for
        
        Returns:
            Comprehensive content intelligence
        """
        target_keywords = target_keywords or []
        
        analysis = {
            'readability': self.calculate_readability_scores(content),
            'keyword_analysis': self.analyze_keywords(content, target_keywords),
            'sentiment': self.analyze_sentiment(content),
            'entities': self.extract_entities(content),
            'content_structure': self.analyze_structure(content),
            'suggestions': self.generate_suggestions(content, target_keywords)
        }
        
        return analysis
    
    def calculate_readability_scores(self, content: str) -> Dict:
        """Calculate multiple readability metrics"""
        text = re.sub(r'[^\w\s]', '', content)
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = text.split()
        
        # Word counts
        total_words = len(words)
        sentences_count = len(sentences)
        syllables = sum(self._count_syllables(word) for word in words)
        
        # Handle edge cases
        if total_words == 0 or sentences_count == 0:
            return {
                'flesch_kincaid': 0,
                'gunning_fog': 0,
                'smog': 0,
                'coleman_liau': 0,
                'readability_level': 'Unknown',
                'word_count': 0,
                'sentence_count': 0,
                'avg_sentence_length': 0
            }
        
        avg_sentence_length = total_words / sentences_count
        
        # Flesch-Kincaid (requires syllables)
        if total_words > 0:
            # Approximate syllable counting without extensive library
            # Flesch Reading Ease = 206.835 - (1.015 * total_words) - (84.6 * syllables / total_words)
            # But for simplicity, we'll use a simplified version
            chars = sum(len(word) for word in words)
            avg_chars_per_word = chars / total_words if total_words > 0 else 0
            flesch_kincaid = 206.835 - (1.015 * avg_sentence_length) - (84.6 * (syllables / total_words if total_words > 0 else 0))
        else:
            flesch_kincaid = 0
        
        # Gunning Fog Index
        complex_words = sum(1 for word in words if len(word) >= 7 or self._has_three_syllables(word))
        complex_words_ratio = complex_words / total_words if total_words > 0 else 0
        gunning_fog = 0.4 * (avg_sentence_length + 100 * complex_words_ratio)
        
        # SMOG Index (simplified)
        smog = 3 + (syllables / sentences_count ** 0.5) if sentences_count > 0 else 0
        
        # Coleman-Liau Index (based on characters and sentences)
        chars_per_word = chars / total_words if total_words > 0 else 0
        sentences_per_word = sentences_count / total_words if total_words > 0 else 0
        coleman_liau = 0.0588 * chars_per_word - 0.296 * (100 * sentences_per_word) - 15.8
        
        # Determine readability level
        level = self._get_readability_level(flesch_kincaid)
        
        return {
            'flesch_kincaid': round(flesch_kincaid, 1),
            'flesch_reading_ease': min(100, max(0, flesch_kincaid)),
            'gunning_fog': round(gunning_fog, 1),
            'smog': round(smog, 1),
            'coleman_liau': round(coleman_liau, 1),
            'readability_level': level,
            'word_count': total_words,
            'sentence_count': sentences_count,
            'avg_sentence_length': round(avg_sentence_length, 1),
            'syllable_count': syllables
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)"""
        word = word.lower()
        if len(word) <= 3:
            return 1
        
        word = re.sub(r'[^a-z]', '', word)
        
        # Vowel groups
        vowels = 'aeiouy'
        count = 0
        prev_char_is_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_char_is_vowel:
                    count += 1
                prev_char_is_vowel = True
            else:
                prev_char_is_vowel = False
        
        # Silent 'e' at end
        if word.endswith('e'):
            count -= 1
        
        return max(1, count)
    
    def _has_three_syllables(self, word: str) -> bool:
        """Check if word has 3+ syllables"""
        return self._count_syllables(word) >= 3
    
    def _get_readability_level(self, score: float) -> str:
        """Get readability level from Flesch score"""
        if score >= 90:
            return 'Very Easy (5th grade)'
        elif score >= 80:
            return 'Easy (6th grade)'
        elif score >= 70:
            return 'Fairly Easy (7th grade)'
        elif score >= 60:
            return 'Standard (8th-9th grade)'
        elif score >= 50:
            return 'Fairly Difficult (10th-12th grade)'
        elif score >= 30:
            return 'Difficult (College)'
        else:
            return 'Very Difficult (Graduate)'
    
    def analyze_keywords(self, content: str, target_keywords: List[str]) -> Dict:
        """Analyze keyword usage"""
        words = re.findall(r'\b\w+\b', content.lower())
        
        # Remove stop words
        filtered_words = [w for w in words if w not in self.STOP_WORDS_EN]
        
        # Count word frequency
        word_freq = Counter(filtered_words)
        
        # Calculate keyword density
        total_words = len(words)
        keyword_analysis = {}
        
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            count = content.lower().count(keyword_lower)
            density = (count / total_words * 100) if total_words > 0 else 0
            
            keyword_analysis[keyword] = {
                'count': count,
                'density': round(density, 2),
                'optimal_density': self._is_optimal_density(density),
                'positions': self._find_keyword_positions(content, keyword),
                'suggestion': self._get_keyword_suggestion(density, count)
            }
        
        # Extract top phrases
        phrases = self._extract_phrases(filtered_words, n=2)
        top_phrases = phrases[:10] if phrases else []
        
        return {
            'total_words': total_words,
            'unique_words': len(set(filtered_words)),
            'target_keywords': keyword_analysis,
            'top_phrases': [{'phrase': p[0], 'count': p[1]} for p in top_phrases],
            'keyword_density_summary': self._analyze_density_summary(keyword_analysis, total_words)
        }
    
    def _is_optimal_density(self, density: float) -> bool:
        """Check if keyword density is optimal (1-3%)"""
        return 1.0 <= density <= 3.0
    
    def _find_keyword_positions(self, content: str, keyword: str) -> List[int]:
        """Find all positions of keyword in content"""
        keyword_lower = keyword.lower()
        content_lower = content.lower()
        positions = []
        
        start = 0
        while True:
            pos = content_lower.find(keyword_lower, start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1
        
        return positions[:20]  # Top 20 positions
    
    def _get_keyword_suggestion(self, density: float, count: int) -> str:
        """Get suggestion for keyword density"""
        if count == 0:
            return 'Keyword not found - consider adding naturally'
        elif density < 1.0:
            return 'Low density - could add more naturally'
        elif density > 3.0:
            return 'High density - risk of keyword stuffing, reduce slightly'
        else:
            return 'Optimal density - good natural placement'
    
    def _extract_phrases(self, words: List[str], n: int = 2) -> List[Tuple[str, int]]:
        """Extract n-grams/phrases from text"""
        phrases = Counter()
        
        for i in range(len(words) - n + 1):
            phrase = ' '.join(words[i:i+n])
            phrases[phrase] += 1
        
        return phrases.most_common(20)
    
    def _analyze_density_summary(self, keyword_analysis: Dict, total_words: int) -> Dict:
        """Analyze overall keyword density summary"""
        total_keyword_count = sum(ka['count'] for ka in keyword_analysis.values())
        overall_density = (total_keyword_count / total_words * 100) if total_words > 0 else 0
        
        return {
            'total_keyword_occurrences': total_keyword_count,
            'overall_density': round(overall_density, 2),
            'keyword_count': len(keyword_analysis),
            'is_optimal': 1.0 <= overall_density <= 5.0,
            'suggestion': self._get_keyword_suggestion(overall_density, total_keyword_count)
        }
    
    def analyze_sentiment(self, content: str) -> Dict:
        """Simple sentiment analysis"""
        # Simple dictionary-based sentiment
        positive_words = [
            'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
            'awesome', 'outstanding', 'superb', 'brilliant', 'love', 'like',
            'best', 'happy', 'pleased', 'satisfied', 'perfect', 'incredible'
        ]
        
        negative_words = [
            'bad', 'poor', 'terrible', 'awful', 'horrible', 'worst',
            'hate', 'dislike', 'disappointed', 'frustrated', 'angry', 'sad',
            'ugly', 'broken', 'fail', 'failure', 'problem', 'issue', 'error'
        ]
        
        words = re.findall(r'\b\w+\b', content.lower())
        
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            return {
                'sentiment': 'Neutral',
                'positive_ratio': 0,
                'negative_ratio': 0,
                'positive_count': 0,
                'negative_count': 0,
                'suggestion': 'Content is neutral - consider adding more engaging language'
            }
        
        positive_ratio = positive_count / total_sentiment_words
        negative_ratio = negative_count / total_sentiment_words
        
        if positive_ratio > negative_ratio + 0.2:
            sentiment = 'Very Positive'
        elif positive_ratio > negative_ratio:
            sentiment = 'Positive'
        elif negative_ratio > positive_ratio + 0.2:
            sentiment = 'Very Negative'
        elif negative_ratio > positive_ratio:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return {
            'sentiment': sentiment,
            'positive_ratio': round(positive_ratio * 100, 1),
            'negative_ratio': round(negative_ratio * 100, 1),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'suggestion': self._get_sentiment_suggestion(sentiment)
        }
    
    def _get_sentiment_suggestion(self, sentiment: str) -> str:
        """Get suggestion for sentiment"""
        suggestions = {
            'Very Positive': 'Great positive tone! Keep engaging.',
            'Positive': 'Good positive tone. Consider adding specific benefits.',
            'Neutral': 'Content is neutral. Add more engaging, benefit-focused language.',
            'Negative': 'Negative tone detected. Consider rewording to be more positive.',
            'Very Negative': 'Very negative tone. Significantly revise to be more constructive.'
        }
        return suggestions.get(sentiment, 'Tone is neutral.')
    
    def extract_entities(self, content: str) -> Dict:
        """Simple entity extraction (regex-based)"""
        entities = {
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content),
            'urls': re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', content),
            'phone_numbers': re.findall(r'\+?1?\s*\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}', content),
            'currency': re.findall(r'\$\d+(?:,\d+)*(?:\.\d{2})?', content),
            'numbers': re.findall(r'\b\d+(?:,\d+)*(?:\.\d+)?\b', content),
            'dates': re.findall(r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s,]*\d{1,2}[\s,]*\d{4}\b', content),
        }
        
        # Count unique entities
        unique_entities = {k: len(set(v)) for k, v in entities.items()}
        
        return {
            'entities': entities,
            'unique_counts': unique_entities,
            'total_entities': sum(unique_entities.values())
        }
    
    def analyze_structure(self, content: str) -> Dict:
        """Analyze content structure"""
        # Sentence analysis
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths) if sentence_lengths else 0
        
        # Paragraph analysis
        paragraphs = re.split(r'\n\n+', content)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        paragraph_lengths = [len(p.split()) for p in paragraphs]
        avg_paragraph_length = sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0
        
        # Heading structure (if HTML)
        h1_count = len(re.findall(r'<h1[^>]*>', content, re.I))
        h2_count = len(re.findall(r'<h2[^>]*>', content, re.I))
        h3_count = len(re.findall(r'<h3[^>]*>', content, re.I))
        
        return {
            'sentence_analysis': {
                'total_sentences': len(sentences),
                'avg_sentence_length': round(avg_sentence_length, 1),
                'max_sentence_length': max(sentence_lengths) if sentence_lengths else 0,
                'min_sentence_length': min(sentence_lengths) if sentence_lengths else 0,
                'long_sentences': len([l for l in sentence_lengths if l > 25])
            },
            'paragraph_analysis': {
                'total_paragraphs': len(paragraphs),
                'avg_paragraph_length': round(avg_paragraph_length, 1),
                'max_paragraph_length': max(paragraph_lengths) if paragraph_lengths else 0,
                'short_paragraphs': len([l for l in paragraph_lengths if l < 50])
            },
            'heading_structure': {
                'h1_count': h1_count,
                'h2_count': h2_count,
                'h3_count': h3_count,
                'has_proper_structure': h1_count == 1 and h2_count > 0
            }
        }
    
    def generate_suggestions(self, content: str, target_keywords: List[str]) -> List:
        """Generate improvement suggestions"""
        suggestions = []
        
        readability = self.calculate_readability_scores(content)
        keyword_analysis = self.analyze_keywords(content, target_keywords)
        sentiment = self.analyze_sentiment(content)
        structure = self.analyze_structure(content)
        
        # Readability suggestions
        if readability['readability_level'] in ['Difficult (College)', 'Very Difficult (Graduate)']:
            suggestions.append({
                'category': 'Readability',
                'type': 'improvement',
                'message': f"Content is {readability['readability_level']}",
                'suggestion': 'Use shorter sentences and simpler words to improve readability'
            })
        
        # Keyword suggestions
        for keyword, data in keyword_analysis['target_keywords'].items():
            if data['count'] == 0:
                suggestions.append({
                    'category': 'Keywords',
                    'type': 'missing',
                    'message': f'Target keyword "{keyword}" not found',
                    'suggestion': 'Add this keyword naturally in your content'
                })
            elif data['density'] > 3.0:
                suggestions.append({
                    'category': 'Keywords',
                    'type': 'over-optimization',
                    'message': f'Keyword "{keyword}" has high density ({data["density"]}%)',
                    'suggestion': 'Reduce keyword usage to avoid over-optimization'
                })
        
        # Sentiment suggestions
        if sentiment['sentiment'] in ['Negative', 'Very Negative']:
            suggestions.append({
                'category': 'Tone',
                'type': 'improvement',
                'message': f'Content has {sentiment["sentiment"]} tone',
                'suggestion': 'Consider rewording to be more positive and constructive'
            })
        
        # Structure suggestions
        if structure['sentence_analysis']['long_sentences'] > 3:
            suggestions.append({
                'category': 'Structure',
                'type': 'improvement',
                'message': f'Found {structure["sentence_analysis"]["long_sentences"]} long sentences',
                'suggestion': 'Break long sentences into shorter, more readable ones'
            })
        
        if structure['heading_structure']['h1_count'] == 0:
            suggestions.append({
                'category': 'Structure',
                'type': 'missing',
                'message': 'No H1 heading found',
                'suggestion': 'Add one H1 tag as the main page heading'
            })
        
        return suggestions
    
    def extract_power_words(self, content: str) -> List[str]:
        """Extract power words from content"""
        words = re.findall(r'\b\w+\b', content.lower())
        found_power_words = [w for w in words if w in self.POWER_WORDS]
        return list(set(found_power_words))
    
    def score_content_quality(self, content: str, target_keywords: List[str]) -> Dict:
        """Calculate overall content quality score"""
        readability = self.calculate_readability_scores(content)
        keywords = self.analyze_keywords(content, target_keywords)
        sentiment = self.analyze_sentiment(content)
        structure = self.analyze_structure(content)
        
        scores = {}
        
        # Readability score (0-100)
        fk_score = readability.get('flesch_kincaid', 0)
        scores['readability'] = min(100, max(0, fk_score))
        
        # Keyword score (0-100)
        keyword_score = 100
        for kw_data in keywords['target_keywords'].values():
            if kw_data['count'] == 0:
                keyword_score -= 20
            elif not kw_data['optimal_density']:
                keyword_score -= 10
        scores['keywords'] = max(0, keyword_score)
        
        # Sentiment score (0-100)
        if sentiment['sentiment'] in ['Very Positive', 'Positive']:
            scores['sentiment'] = 100
        elif sentiment['sentiment'] == 'Neutral':
            scores['sentiment'] = 70
        else:
            scores['sentiment'] = 40
        
        # Structure score (0-100)
        structure_score = 100
        if structure['heading_structure']['h1_count'] != 1:
            structure_score -= 30
        if structure['heading_structure']['h2_count'] < 2:
            structure_score -= 20
        if structure['sentence_analysis']['long_sentences'] > 3:
            structure_score -= 20
        scores['structure'] = max(0, structure_score)
        
        # Content length score
        word_count = readability['word_count']
        if word_count < 300:
            scores['length'] = 50
        elif 300 <= word_count <= 1500:
            scores['length'] = 100
        else:
            scores['length'] = 80
        
        # Overall score
        overall = round(sum(scores.values()) / len(scores), 1)
        
        return {
            'overall': overall,
            'breakdown': scores,
            'grade': self._get_quality_grade(overall)
        }
    
    def _get_quality_grade(self, score: float) -> str:
        """Get letter grade for quality score"""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'