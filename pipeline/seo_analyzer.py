"""
Python-based SEO Analyzer for Static Sites
Analyzes HTML/Markdown files and provides SEO suggestions
(inspired by Rank Math but for static sites)
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
from ..utils.logger import get_logger


class StaticSiteSEOAnalyzer:
    """SEO analyzer for static sites (Astro, HTML, Markdown)"""
    
    def __init__(self):
        self.logger = get_logger()
        self.suggestions = []
        self.errors = []
        self.warnings = []
        
    def analyze_directory(
        self,
        directory: str,
        file_patterns: List[str] = None
    ) -> Dict:
        """
        Analyze all HTML files in a directory.
        
        Args:
            directory: Path to directory containing HTML files
            file_patterns: List of file patterns to match (default: ['*.html', '*.astro', '*.md'])
        
        Returns:
            Analysis results with suggestions
        """
        if file_patterns is None:
            file_patterns = ['*.html', '*.astro', '*.md']
        
        dir_path = Path(directory)
        if not dir_path.exists():
            self.logger.error(f"Directory not found: {directory}")
            return {'error': 'Directory not found'}
        
        results = {
            'directory': str(dir_path),
            'total_files': 0,
            'analyzed_files': 0,
            'suggestions': [],
            'scores': {
                'overall': 0,
                'title_tags': 0,
                'meta_descriptions': 0,
                'headings': 0,
                'content': 0,
                'images': 0,
                'links': 0
            }
        }
        
        # Find all matching files
        files_found = []
        for pattern in file_patterns:
            files_found.extend(dir_path.rglob(pattern))
        
        results['total_files'] = len(files_found)
        
        self.logger.info(f"Found {len(files_found)} files to analyze")
        
        # Analyze each file
        all_scores = {
            'title_tags': [],
            'meta_descriptions': [],
            'headings': [],
            'content': [],
            'images': [],
            'links': []
        }
        
        for file_path in files_found:
            try:
                file_analysis = self.analyze_file(str(file_path))
                
                if file_analysis:
                    results['analyzed_files'] += 1
                    results['suggestions'].extend(file_analysis.get('suggestions', []))
                    
                    # Collect scores
                    for category in all_scores.keys():
                        if category in file_analysis.get('scores', {}):
                            all_scores[category].append(file_analysis['scores'][category])
                            
            except Exception as e:
                self.logger.error(f"Error analyzing {file_path}: {e}")
                results['suggestions'].append({
                    'file': str(file_path),
                    'type': 'error',
                    'severity': 'high',
                    'category': 'File Error',
                    'message': f"Failed to analyze: {str(e)}",
                    'suggestion': f"Check if file is valid: {file_path}"
                })
        
        # Calculate average scores
        for category in all_scores.keys():
            scores = all_scores[category]
            if scores:
                results['scores'][category] = round(sum(scores) / len(scores), 1)
        
        # Calculate overall score
        valid_scores = [s for s in results['scores'].values() if s > 0]
        if valid_scores:
            results['scores']['overall'] = round(sum(valid_scores) / len(valid_scores), 1)
        
        # Sort suggestions by severity
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        results['suggestions'].sort(key=lambda x: severity_order.get(x.get('severity', 'medium'), 2))
        
        self.logger.success(f"Analyzed {results['analyzed_files']}/{results['total_files']} files")
        self.logger.info(f"Overall SEO Score: {results['scores']['overall']}/100")
        
        return results
    
    def analyze_file(self, file_path: str) -> Optional[Dict]:
        """
        Analyze a single file.
        
        Args:
            file_path: Path to file
        
        Returns:
            File analysis results
        """
        file_ext = Path(file_path).suffix
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                self.logger.error(f"Failed to read {file_path}: {e}")
                return None
        
        # Parse HTML
        if file_ext in ['.html', '.htm']:
            soup = BeautifulSoup(content, 'html.parser')
            return self._analyze_html(soup, file_path)
        elif file_ext == '.astro':
            # Astro files have frontmatter - extract HTML part
            html_content = self._extract_html_from_astro(content)
            if html_content:
                soup = BeautifulSoup(html_content, 'html.parser')
                return self._analyze_html(soup, file_path)
        elif file_ext == '.md':
            # Markdown analysis
            return self._analyze_markdown(content, file_path)
        
        return None
    
    def _extract_html_from_astro(self, content: str) -> str:
        """Extract HTML part from Astro file"""
        # Astro files have --- frontmatter --- then HTML
        lines = content.split('\n')
        html_started = False
        html_lines = []
        
        for line in lines:
            if html_started:
                html_lines.append(line)
            elif line.strip() == '<':
                # HTML starts
                html_started = True
                html_lines.append(line)
        
        return '\n'.join(html_lines) if html_lines else content
    
    def _analyze_html(self, soup: BeautifulSoup, file_path: str) -> Dict:
        """Analyze HTML content"""
        suggestions = []
        scores = {}
        
        # 1. Title Tag Analysis
        title_score, title_suggs = self._check_title_tag(soup, file_path)
        suggestions.extend(title_suggs)
        scores['title_tags'] = title_score
        
        # 2. Meta Description Analysis
        meta_score, meta_suggs = self._check_meta_description(soup, file_path)
        suggestions.extend(meta_suggs)
        scores['meta_descriptions'] = meta_score
        
        # 3. Heading Structure
        heading_score, heading_suggs = self._check_heading_structure(soup, file_path)
        suggestions.extend(heading_suggs)
        scores['headings'] = heading_score
        
        # 4. Content Analysis
        content_score, content_suggs = self._check_content_quality(soup, file_path)
        suggestions.extend(content_suggs)
        scores['content'] = content_score
        
        # 5. Image Optimization
        image_score, image_suggs = self._check_images(soup, file_path)
        suggestions.extend(image_suggs)
        scores['images'] = image_score
        
        # 6. Link Analysis
        link_score, link_suggs = self._check_links(soup, file_path)
        suggestions.extend(link_suggs)
        scores['links'] = link_score
        
        return {
            'file': file_path,
            'suggestions': suggestions,
            'scores': scores
        }
    
    def _check_title_tag(self, soup: BeautifulSoup, file_path: str) -> tuple:
        """Check title tag"""
        score = 0
        suggestions = []
        
        title = soup.find('title')
        
        if not title or not title.text.strip():
            suggestions.append({
                'file': file_path,
                'type': 'error',
                'severity': 'critical',
                'category': 'Title Tag',
                'message': 'Missing or empty title tag',
                'suggestion': 'Add a <title> tag with 50-60 characters including your main keyword'
            })
            return score, suggestions
        
        title_text = title.text.strip()
        title_length = len(title_text)
        
        # Length check
        if title_length < 30:
            score += 20
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Title Tag',
                'message': 'Title too short',
                'detail': f'Title is {title_length} characters (recommended: 50-60)',
                'suggestion': 'Consider expanding title to include more context and keywords',
                'current_title': title_text
            })
        elif title_length > 60:
            score += 60
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'medium',
                'category': 'Title Tag',
                'message': 'Title too long',
                'detail': f'Title is {title_length} characters (recommended: 50-60)',
                'suggestion': 'Consider shortening title under 60 characters to avoid truncation in SERP',
                'current_title': title_text
            })
        else:
            score += 100
        
        # Title uniqueness (would need to check across all pages)
        # Placeholder for now
        
        return score, suggestions
    
    def _check_meta_description(self, soup: BeautifulSoup, file_path: str) -> tuple:
        """Check meta description"""
        score = 0
        suggestions = []
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        
        if not meta_desc or not meta_desc.get('content'):
            suggestions.append({
                'file': file_path,
                'type': 'error',
                'severity': 'critical',
                'category': 'Meta Description',
                'message': 'Missing meta description',
                'suggestion': 'Add a <meta name="description"> tag with 150-160 characters describing the page'
            })
            return score, suggestions
        
        desc_text = meta_desc.get('content', '')
        desc_length = len(desc_text)
        
        # Length check
        if desc_length < 120:
            score += 30
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Meta Description',
                'message': 'Meta description too short',
                'detail': f'Description is {desc_length} characters (recommended: 150-160)',
                'suggestion': 'Expand description to include more context and clear value proposition',
                'current_description': desc_text
            })
        elif desc_length > 160:
            score += 70
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'medium',
                'category': 'Meta Description',
                'message': 'Meta description too long',
                'detail': f'Description is {desc_length} characters (recommended: 150-160)',
                'suggestion': 'Shorten description to avoid truncation in SERP',
                'current_description': desc_text
            })
        else:
            score += 100
        
        return score, suggestions
    
    def _check_heading_structure(self, soup: BeautifulSoup, file_path: str) -> tuple:
        """Check heading structure"""
        score = 100
        suggestions = []
        
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        if not headings:
            score = 20
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Headings',
                'message': 'No heading tags found',
                'suggestion': 'Add H1, H2, H3 tags to structure your content and improve SEO'
            })
            return score, suggestions
        
        # Check for multiple H1s
        h1_count = len(soup.find_all('h1'))
        if h1_count == 0:
            score -= 30
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Headings',
                'message': 'Missing H1 tag',
                'suggestion': 'Add one H1 tag as the main page heading'
            })
        elif h1_count > 1:
            score -= 40
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Headings',
                'message': f'Multiple H1 tags found ({h1_count})',
                'suggestion': 'Use only one H1 tag per page, use H2-H6 for subheadings'
            })
        
        # Check heading hierarchy
        last_level = None
        for heading in headings:
            level = int(heading.name[1])  # h1 -> 1, h2 -> 2, etc.
            
            if last_level is not None and level > last_level + 1:
                score -= 10
                suggestions.append({
                    'file': file_path,
                    'type': 'info',
                    'severity': 'low',
                    'category': 'Headings',
                    'message': f'Heading jump: H{last_level} → H{level}',
                    'detail': f"Consider adding H{last_level + 1} between {last_level} and {level}",
                    'suggestion': 'Maintain logical heading hierarchy (H1 → H2 → H3)'
                })
            
            last_level = level
        
        return max(score, 0), suggestions
    
    def _check_content_quality(self, soup: BeautifulSoup, file_path: str) -> tuple:
        """Check content quality"""
        score = 100
        suggestions = []
        
        # Get text content
        text = soup.get_text(separator=' ', strip=True)
        word_count = len(text.split())
        
        if word_count < 300:
            score -= 50
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Content Quality',
                'message': 'Content too short',
                'detail': f'Page has {word_count} words (recommended: 500+)',
                'suggestion': 'Add more content to provide comprehensive information on the topic',
                'word_count': word_count
            })
        elif word_count < 500:
            score -= 20
            suggestions.append({
                'file': file_path,
                'type': 'info',
                'severity': 'medium',
                'category': 'Content Quality',
                'message': 'Consider longer content',
                'detail': f'Page has {word_count} words (recommended: 500+)',
                'suggestion': 'More comprehensive content tends to perform better in search rankings',
                'word_count': word_count
            })
        
        # Check for paragraphs
        paragraphs = soup.find_all('p')
        if len(paragraphs) < 3:
            score -= 10
            suggestions.append({
                'file': file_path,
                'type': 'info',
                'severity': 'low',
                'category': 'Content Quality',
                'message': 'Few paragraphs found',
                'detail': f'Found {len(paragraphs)} paragraphs',
                'suggestion': 'Break content into more paragraphs for better readability'
            })
        
        return max(score, 0), suggestions
    
    def _check_images(self, soup: BeautifulSoup, file_path: str) -> tuple:
        """Check image optimization"""
        score = 100
        suggestions = []
        
        images = soup.find_all('img')
        
        if not images:
            return score, suggestions
        
        for img in images:
            # Check alt text
            alt = img.get('alt', '')
            if not alt:
                score -= 5
                suggestions.append({
                    'file': file_path,
                    'type': 'warning',
                    'severity': 'medium',
                    'category': 'Images',
                    'message': 'Image missing alt text',
                    'detail': f'Image: {img.get("src", "unknown")}',
                    'suggestion': 'Add descriptive alt text for accessibility and SEO'
                })
            
            # Check for empty alt (ok for decorative, but worth noting)
            if alt and len(alt) < 5:
                suggestions.append({
                    'file': file_path,
                    'type': 'info',
                    'severity': 'low',
                    'category': 'Images',
                    'message': 'Image alt text very short',
                    'detail': f'Alt text: "{alt}"',
                    'suggestion': 'Use more descriptive alt text (at least 5 characters)'
                })
        
        return max(score, 0), suggestions
    
    def _check_links(self, soup: BeautifulSoup, file_path: str) -> tuple:
        """Check internal/external links"""
        score = 100
        suggestions = []
        
        links = soup.find_all('a')
        
        internal_count = 0
        external_count = 0
        no_follow_count = 0
        
        for link in links:
            href = link.get('href', '')
            
            if not href:
                continue
            
            # Count link types
            if href.startswith('http'):
                external_count += 1
                
                # Check for nofollow
                rel = link.get('rel', '')
                if 'nofollow' in rel.lower():
                    no_follow_count += 1
            else:
                internal_count += 1
        
        if len(links) > 0:
            # Check internal link ratio
            internal_ratio = internal_count / len(links)
            
            if internal_ratio < 0.3:
                score -= 15
                suggestions.append({
                    'file': file_path,
                    'type': 'info',
                    'severity': 'low',
                    'category': 'Links',
                    'message': 'Low internal link ratio',
                    'detail': f'Internal: {internal_count}/{len(links)} ({internal_ratio:.1%})',
                    'suggestion': 'Add more internal links to improve site structure and user experience'
                })
        
        return max(score, 0), suggestions
    
    def _analyze_markdown(self, content: str, file_path: str) -> Dict:
        """Analyze Markdown content"""
        suggestions = []
        scores = {}
        
        # Count headings
        h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
        h2_count = len(re.findall(r'^## ', content, re.MULTILINE))
        
        # Check for H1
        if h1_count == 0:
            scores['headings'] = 50
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Headings',
                'message': 'Missing H1 in Markdown',
                'suggestion': 'Add a top-level heading (# Title) to your Markdown'
            })
        elif h1_count > 1:
            scores['headings'] = 60
            suggestions.append({
                'file': file_path,
                'type': 'warning',
                'severity': 'high',
                'category': 'Headings',
                'message': f'Multiple H1s in Markdown ({h1_count})',
                'suggestion': 'Use only one H1 (#) in Markdown'
            })
        else:
            scores['headings'] = 100
        
        # Word count
        word_count = len(content.split())
        if word_count < 300:
            scores['content'] = 50
            suggestions.append({
                'file': file_path,
                'type': 'info',
                'severity': 'medium',
                'category': 'Content Quality',
                'message': 'Content seems short',
                'detail': f'Word count: {word_count}',
                'suggestion': 'Consider expanding content for better SEO'
            })
        else:
            scores['content'] = 100
        
        return {
            'file': file_path,
            'suggestions': suggestions,
            'scores': scores
        }
    
    def generate_report(self, results: Dict) -> str:
        """Generate a readable report"""
        report = []
        
        report.append("=" * 80)
        report.append("Static Site SEO Analysis Report")
        report.append("=" * 80)
        report.append("")
        
        # Summary
        report.append(f"Directory: {results['directory']}")
        report.append(f"Files Analyzed: {results['analyzed_files']}/{results['total_files']}")
        report.append("")
        report.append("SEO SCORES:")
        report.append("-" * 40)
        
        scores = results['scores']
        report.append(f"Overall:     {scores['overall']}/100")
        report.append(f"Title Tags: {scores['title_tags']}/100")
        report.append(f"Meta Descriptions: {scores['meta_descriptions']}/100")
        report.append(f"Headings:    {scores['headings']}/100")
        report.append(f"Content:     {scores['content']}/100")
        report.append(f"Images:      {scores['images']}/100")
        report.append(f"Links:       {scores['links']}/100")
        report.append("")
        
        # Suggestions
        if results['suggestions']:
            report.append("SUGGESTIONS:")
            report.append("-" * 80)
            
            # Group by severity
            critical = [s for s in results['suggestions'] if s.get('severity') == 'critical']
            high = [s for s in results['suggestions'] if s.get('severity') == 'high']
            medium = [s for s in results['suggestions'] if s.get('severity') == 'medium']
            low = [s for s in results['suggestions'] if s.get('severity') == 'low']
            
            if critical:
                report.append("\n🔴 CRITICAL ISSUES:")
                for sugg in critical[:10]:  # Top 10
                    report.append(f"  • {sugg['category']}: {sugg['message']}")
                    report.append(f"    File: {Path(sugg['file']).name}")
                    report.append(f"    {sugg['suggestion']}")
                    report.append("")
            
            if high:
                report.append(f"\n🟠 HIGH PRIORITY ({len(high)}):")
                for sugg in high[:10]:
                    report.append(f"  • {sugg['category']}: {sugg['message']}")
                    report.append(f"    {sugg['suggestion']}")
                    report.append("")
            
            if medium:
                report.append(f"\n🟡 MEDIUM PRIORITY ({len(medium)}):")
                for sugg in medium[:5]:
                    report.append(f"  • {sugg['category']}: {sugg['message']}")
                    report.append("")
            
            if low:
                report.append(f"\n🟢 LOW PRIORITY ({len(low)}):")
                for sugg in low[:5]:
                    report.append(f"  • {sugg['category']}: {sugg['message']}")
                    report.append("")
        
        report.append("\n" + "=" * 80)
        report.append("End of Report")
        report.append("=" * 80)
        
        return "\n".join(report)