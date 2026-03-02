#!/usr/bin/env python
"""
CLI for Static Site SEO Analyzer
Run: python analyze_site.py --directory /path/to/site
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pipeline.seo_analyzer import StaticSiteSEOAnalyzer


def main():
    parser = argparse.ArgumentParser(description='Analyze SEO of static site (Astro, HTML, Markdown)')
    parser.add_argument('--directory', '-d', required=True, help='Path to directory containing site files')
    parser.add_argument('--output', '-o', help='Output report file (default: print to console)')
    parser.add_argument('--format', '-f', choices=['text', 'json'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = StaticSiteSEOAnalyzer()
    
    # Analyze directory
    print(f"🔍 Analyzing {args.directory}...")
    results = analyzer.analyze_directory(args.directory)
    
    # Output results
    if args.format == 'text':
        report = analyzer.generate_report(results)
        print(report)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"\n📄 Report saved to: {args.output}")
    
    elif args.format == 'json':
        import json
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 JSON report saved to: {args.output}")
        else:
            print(json.dumps(results, indent=2))
    
    return 0 if results.get('scores', {}).get('overall', 0) > 70 else 1


if __name__ == '__main__':
    sys.exit(main())