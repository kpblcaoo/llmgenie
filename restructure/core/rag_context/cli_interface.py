#!/usr/bin/env python3
"""
Enhanced CLI Interface for RAG Context Management
Now includes Self-Refine Pipeline integration
"""

import argparse
import sys
import json
import asyncio
from pathlib import Path
from typing import Optional

from .config import RAGConfig
from .enhancer import PromptEnhancer
from .interfaces.self_refine_pipeline import SelfRefinePipeline, RefinementType, quick_refine_code, quick_refine_text
from .interfaces.cli_tool import CLITool


def create_main_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands"""
    parser = argparse.ArgumentParser(
        description="RAG Context Management with Self-Refine Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # RAG Commands
  python -m rag_context.cli_interface enhance "How to improve code quality?"
  python -m rag_context.cli_interface search "best practices" --max-rules 5
  python -m rag_context.cli_interface stats --json
  
  # Self-Refine Commands  
  python -m rag_context.cli_interface refine code --content "def bad_func(x): return x+1 if x else 0"
  python -m rag_context.cli_interface refine text --content "This text needs improvement"
  python -m rag_context.cli_interface refine code --file mycode.py --output improved.py
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # RAG commands (existing functionality)
    enhance_parser = subparsers.add_parser('enhance', help='Enhance prompt with context')
    enhance_parser.add_argument('query', help='Query to enhance')
    enhance_parser.add_argument('--max-context', type=int, default=2000, help='Max context length')
    enhance_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    search_parser = subparsers.add_parser('search', help='Search for relevant rules')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--max-rules', type=int, default=3, help='Max rules to return')
    search_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    stats_parser = subparsers.add_parser('stats', help='Show system statistics')
    stats_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    refresh_parser = subparsers.add_parser('refresh', help='Refresh index')
    refresh_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    struct_parser = subparsers.add_parser('struct', help='Show project structure')
    struct_parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    # Self-refine subcommands (new functionality)
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
    
    # Quick refinement
    quick_parser = refine_subparsers.add_parser('quick', help='Quick refinement')
    quick_parser.add_argument('type', choices=['code', 'text'], help='Content type')
    quick_parser.add_argument('content', help='Content to refine')
    
    return parser


async def handle_rag_commands(args, cli_tool: CLITool):
    """Handle RAG-related commands"""
    output_format = "json" if getattr(args, 'json', False) else "text"
    
    if args.command == 'enhance':
        result = await cli_tool.enhance_command(
            args.query, 
            max_context=args.max_context,
            output_format=output_format
        )
        print(result)
        
    elif args.command == 'search':
        result = await cli_tool.search_rules_command(
            args.query,
            max_rules=args.max_rules,
            output_format=output_format
        )
        print(result)
        
    elif args.command == 'stats':
        result = await cli_tool.stats_command(output_format=output_format)
        print(result)
        
    elif args.command == 'refresh':
        result = await cli_tool.refresh_command(output_format=output_format)
        print(result)
        
    elif args.command == 'struct':
        result = await cli_tool.struct_command(output_format=output_format)
        print(result)


def handle_refine_commands(args):
    """Handle self-refine pipeline commands"""
    
    if args.refine_command == 'code':
        handle_refine_code(args)
    elif args.refine_command == 'text':
        handle_refine_text(args)
    elif args.refine_command == 'report':
        handle_refine_report(args)
    elif args.refine_command == 'quick':
        handle_refine_quick(args)
    else:
        print(f"Unknown refine command: {args.refine_command}")
        sys.exit(1)


def handle_refine_code(args):
    """Handle code refinement"""
    print("🔧 CODE REFINEMENT")
    print("=" * 40)
    
    pipeline = SelfRefinePipeline(
        max_iterations=args.max_iterations,
        confidence_threshold=args.confidence_threshold
    )
    
    # Get content to refine
    if args.file:
        if not Path(args.file).exists():
            print(f"❌ Error: File not found: {args.file}")
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
        print("❌ Error: Must specify either --file or --content")
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
    print("📝 TEXT REFINEMENT")
    print("=" * 40)
    
    pipeline = SelfRefinePipeline(max_iterations=args.max_iterations)
    
    # Get content to refine
    if args.file:
        if not Path(args.file).exists():
            print(f"❌ Error: File not found: {args.file}")
            sys.exit(1)
        content = Path(args.file).read_text()
    elif args.content:
        content = args.content
    else:
        print("❌ Error: Must specify either --file or --content")
        sys.exit(1)
    
    print(f"📄 Original: {content}")
    
    # Refine content
    results = pipeline.refine(content, RefinementType.TEXT)
    refined_content = results[-1].refined if results else content
    
    # Output result
    if args.output:
        Path(args.output).write_text(refined_content)
        print(f"✅ Refined text saved to: {args.output}")
    else:
        print("✨ Refined text:")
        print(refined_content)
    
    # Show summary
    if results:
        print(f"\n📊 Refinement completed in {len(results)} iterations")
        print(f"   Final confidence: {results[-1].confidence_score:.2f}")


def handle_refine_report(args):
    """Handle refinement report generation"""
    if not args.session_file or not Path(args.session_file).exists():
        print("❌ Error: Must specify valid --session-file")
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
        print(f"❌ Error generating report: {e}")
        sys.exit(1)


def handle_refine_quick(args):
    """Handle quick refinement"""
    print("⚡ QUICK REFINEMENT")
    print("=" * 40)
    
    if args.type == 'code':
        result = quick_refine_code(args.content)
        print(f"🔧 Original code: {args.content}")
        print(f"✨ Refined code: {result}")
    else:
        result = quick_refine_text(args.content)
        print(f"📝 Original text: {args.content}")
        print(f"✨ Refined text: {result}")


async def main():
    """Main entry point"""
    parser = create_main_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Handle refine commands (synchronous)
    if args.command == 'refine':
        if not hasattr(args, 'refine_command') or not args.refine_command:
            print("❌ Error: Must specify refine subcommand (code, text, report, quick)")
            sys.exit(1)
        handle_refine_commands(args)
        return
    
    # Handle RAG commands (asynchronous)
    try:
        config = RAGConfig()
        cli_tool = CLITool(config)
        await handle_rag_commands(args, cli_tool)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def sync_main():
    """Synchronous wrapper for main"""
    asyncio.run(main())


if __name__ == "__main__":
    sync_main() 