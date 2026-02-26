#!/usr/bin/env python3
"""
AutoSEO Pipeline CLI Entry Point

Usage:
    python run.py                    # Run full pipeline
    python run.py --stage ingest     # Run specific stage
    python run.py --dry-run          # Preview changes without deploying
    python run.py --input file.csv   # Process specific CSV file
"""

import argparse
import json
import sys
from pathlib import Path

from pipeline import Pipeline
from pipeline.utils.config import get_config, reload_config
from pipeline.utils.logger import get_logger


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser"""
    parser = argparse.ArgumentParser(
        prog="autoseo",
        description="AutoSEO Pipeline - Automated SEO content generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                         Run full pipeline
  python run.py --stage ingest          Run only ingest stage
  python run.py --stage generate        Run only generate stage
  python run.py --stage transform       Run only transform stage
  python run.py --stage deploy          Run only deploy stage
  python run.py --dry-run               Preview without deploying
  python run.py --no-deploy             Skip git push
  python run.py --input keywords.csv    Process specific CSV
  python run.py --status                Show pipeline status
  python run.py -v                      Verbose output
"""
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=None,
        help="Path to config.yaml file"
    )
    
    parser.add_argument(
        "--stage", "-s",
        type=str,
        choices=["ingest", "generate", "transform", "deploy", "all"],
        default="all",
        help="Run specific stage only"
    )
    
    parser.add_argument(
        "--input", "-i",
        type=str,
        default=None,
        help="Path to input CSV file"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Path to output seo.json file"
    )
    
    parser.add_argument(
        "--max-keywords", "-m",
        type=int,
        default=None,
        help="Maximum number of keywords to process"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Run without making actual changes"
    )
    
    parser.add_argument(
        "--no-deploy",
        action="store_true",
        help="Skip the deploy stage"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show pipeline status and exit"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    
    return parser


def print_status(pipeline: Pipeline, as_json: bool = False):
    """Print pipeline status"""
    status = pipeline.get_status()
    
    if as_json:
        print(json.dumps(status, indent=2))
        return
    
    print("\nPipeline Status")
    print("=" * 40)
    print(f"Config Loaded: {status['config_loaded']}")
    print(f"Input Directory: {status['input_directory']}")
    print(f"SEO JSON Path: {status['seo_json_path']}")
    print(f"LLM Endpoint: {status['llm_endpoint'][:50]}...")
    
    git = status['git_status']
    print(f"\nGit Status:")
    print(f"  Is Repo: {git['is_repo']}")
    if git['is_repo']:
        print(f"  Branch: {git['branch']}")
        print(f"  Has Changes: {git['has_changes']}")
        print(f"  Modified Files: {len(git['modified_files'])}")
    print()


def print_result(result, as_json: bool = False):
    """Print pipeline result"""
    from pipeline.stages.deploy import DeployResult
    from pipeline.stages.generate import GenerateResult
    from pipeline.stages.ingest import IngestResult
    from pipeline.stages.transform import TransformResult
    
    if as_json:
        output = {
            "success": result.success,
            "errors": result.errors if hasattr(result, 'errors') else []
        }
        if hasattr(result, 'duration_seconds'):
            output["duration_seconds"] = result.duration_seconds
        if hasattr(result, 'summary'):
            output["summary"] = result.summary
        print(json.dumps(output, indent=2))
        return
    
    print("\n" + "=" * 60)
    if result.success:
        print("SUCCESS")
    else:
        print("FAILED")
    print("=" * 60)
    
    if hasattr(result, 'duration_seconds'):
        print(f"Duration: {result.duration_seconds:.2f}s")
    
    if isinstance(result, IngestResult):
        print(f"\nKeywords processed: {result.total_keywords}")
        print(f"CSV files processed: {len(result.processed_files)}")
        if result.data_path:
            print(f"Output: {result.data_path}")
    
    elif isinstance(result, GenerateResult):
        print(f"\nBatches processed: {result.successful_batches}/{result.total_batches}")
        if result.output_path:
            print(f"Output: {result.output_path}")
    
    elif isinstance(result, TransformResult):
        print(f"\nChanges made: {len(result.changes)}")
        if result.seo_json_path:
            print(f"Updated: {result.seo_json_path}")
        if result.backup_path:
            print(f"Backup: {result.backup_path}")
    
    elif isinstance(result, DeployResult):
        if result.commit_hash:
            print(f"\nCommit: {result.commit_hash}")
        print(f"Committed: {result.committed}")
        print(f"Pushed: {result.pushed}")
    
    elif hasattr(result, 'summary') and result.summary:
        print("\nSummary:")
        for key, value in result.summary.items():
            if key != "errors":
                print(f"  {key}: {value}")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"  - {error}")
    
    print()


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    config_path = args.config
    if config_path and not Path(config_path).exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    
    pipeline = Pipeline(config_path=config_path)
    logger = get_logger()
    
    if args.status:
        print_status(pipeline, args.json)
        sys.exit(0)
    
    if args.stage == "all":
        result = pipeline.run(
            input_csv=args.input,
            max_keywords=args.max_keywords,
            dry_run=args.dry_run,
            no_deploy=args.no_deploy
        )
    elif args.stage == "ingest":
        result = pipeline.run_ingest_only(
            input_csv=args.input,
            max_keywords=args.max_keywords
        )
    elif args.stage == "generate":
        result = pipeline.run_generate_only()
    elif args.stage == "transform":
        result = pipeline.run_transform_only()
    elif args.stage == "deploy":
        result = pipeline.run_deploy_only(dry_run=args.dry_run)
    else:
        print(f"Unknown stage: {args.stage}", file=sys.stderr)
        sys.exit(1)
    
    print_result(result, args.json)
    
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
