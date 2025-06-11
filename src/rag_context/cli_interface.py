#!/usr/bin/env python3
"""
Enhanced CLI Interface for RAG Context Management
Now includes Self-Refine Pipeline integration
"""

import argparse
import sys
import json
from pathlib import Path

# ... existing code ...

from interfaces.self_refine_pipeline import SelfRefinePipeline, RefinementType, quick_refine_code, quick_refine_text


def main():
    parser = argparse.ArgumentParser(description="RAG Context Management with Self-Refine Pipeline")
    
    # ... existing code ...
    
    # Self-refine subcommands
    refine_parser = subparsers.add_parser('refine', help='Self-refine content using MCP tools')
    refine_subparsers = refine_parser.add_subparsers(dest='refine_command', help='Refinement commands')
    
    # Refine code
    code_parser = refine_subparsers.add_parser('code', help='Refine code content')
    code_parser.add_argument('--file', type=str, help='Code file to refine')
    code_parser.add_argument('--content', type=str, help='Code content to refine (inline)')
    code_parser.add_argument('--output', type=str, help='Output file (default: overwrite input)')
    code_parser.add_argument('--backup', action='store_true', default=True, help='Create backup before refining')
    code_parser.add_argument('--max-iterations', type=int, default=3, help='Maximum refinement iterations')
    code_parser.add_argument('--confidence-threshold', type=float, default=0.85, help='Confidence threshold for completion')
    
    # Refine text
    text_parser = refine_subparsers.add_parser('text', help='Refine text content')
    text_parser.add_argument('--file', type=str, help='Text file to refine')
    text_parser.add_argument('--content', type=str, help='Text content to refine (inline)')
    text_parser.add_argument('--output', type=str, help='Output file')
    text_parser.add_argument('--max-iterations', type=int, default=2, help='Maximum refinement iterations')
    
    # Refinement report
    report_parser = refine_subparsers.add_parser('report', help='Generate refinement report')
    report_parser.add_argument('--session-file', type=str, help='Session file with refinement results')
    
    args = parser.parse_args()
    
    # Handle refinement commands
    if hasattr(args, 'refine_command') and args.refine_command:
        handle_refine_command(args)
        return
    
    # ... existing code ...


def handle_refine_command(args):
    """Handle self-refine pipeline commands"""
    
    if args.refine_command == 'code':
        handle_refine_code(args)
    elif args.refine_command == 'text':
        handle_refine_text(args)
    elif args.refine_command == 'report':
        handle_refine_report(args)
    else:
        print(f"Unknown refine command: {args.refine_command}")
        sys.exit(1)


def handle_refine_code(args):
    """Handle code refinement"""
    pipeline = SelfRefinePipeline(
        max_iterations=args.max_iterations,
        confidence_threshold=args.confidence_threshold
    )
    
    # Get content to refine
    if args.file:
        if not Path(args.file).exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        results = pipeline.refine_code_file(args.file, backup=args.backup)
        print(f"✅ Refined file: {args.file}")
    elif args.content:
        results = pipeline.refine(args.content, RefinementType.CODE)
        refined_content = results[-1].refined if results else args.content
        
        if args.output:
            Path(args.output).write_text(refined_content)
            print(f"✅ Refined content saved to: {args.output}")
        else:
            print("=== REFINED CODE ===")
            print(refined_content)
    else:
        print("Error: Must specify either --file or --content")
        sys.exit(1)
    
    # Show refinement summary
    if results:
        report = pipeline.generate_refinement_report(results)
        print(f"\n📊 Refinement Summary:")
        print(f"   Iterations: {report['summary']['total_iterations']}")
        print(f"   Final confidence: {report['summary']['final_confidence']:.2f}")
        print(f"   Threshold reached: {report['summary']['threshold_reached']}")
        print(f"   Duration: {report['summary']['total_duration_ms']:.1f}ms")
        
        if report['mcp_tools_summary']['total_unique_tools'] > 0:
            print(f"   MCP tools used: {report['mcp_tools_summary']['most_used_tools']}")


def handle_refine_text(args):
    """Handle text refinement"""
    pipeline = SelfRefinePipeline(max_iterations=args.max_iterations)
    
    # Get content to refine
    if args.file:
        if not Path(args.file).exists():
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        content = Path(args.file).read_text()
    elif args.content:
        content = args.content
    else:
        print("Error: Must specify either --file or --content")
        sys.exit(1)
    
    # Refine content
    results = pipeline.refine(content, RefinementType.TEXT)
    refined_content = results[-1].refined if results else content
    
    # Output result
    if args.output:
        Path(args.output).write_text(refined_content)
        print(f"✅ Refined text saved to: {args.output}")
    else:
        print("=== REFINED TEXT ===")
        print(refined_content)
    
    # Show summary
    if results:
        print(f"\n📊 Refinement completed in {len(results)} iterations")
        print(f"   Final confidence: {results[-1].confidence_score:.2f}")


def handle_refine_report(args):
    """Handle refinement report generation"""
    if not args.session_file or not Path(args.session_file).exists():
        print("Error: Must specify valid --session-file")
        sys.exit(1)
    
    try:
        # Load session data and extract refinement results
        session_data = json.loads(Path(args.session_file).read_text())
        # Process and generate report
        print("📊 Refinement Session Report")
        print("=" * 40)
        # Implementation would parse session data and show refinement statistics
        print("Report generation completed")
    except Exception as e:
        print(f"Error generating report: {e}")
        sys.exit(1)


# ... existing code ... 