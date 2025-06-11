#!/usr/bin/env python3
"""
CLI Demonstration for Self-Refine Pipeline
Interactive demo for onboarding and pitching
"""

import argparse
import sys
import os
from pathlib import Path

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from rag_context.interfaces.self_refine_pipeline import (
    SelfRefinePipeline, 
    RefinementType, 
    quick_refine_code, 
    quick_refine_text
)

def main():
    parser = argparse.ArgumentParser(
        description="Self-Refine Pipeline CLI Demo",
        epilog="Examples:\n"
               "  python %(prog)s code --content 'def bad_func(x): return x+1 if x else 0'\n"
               "  python %(prog)s text --content 'This text needs improvement'\n"
               "  python %(prog)s quick code 'def calc(a,b):return a/b'\n"
               "  python %(prog)s code --file mycode.py --output improved_code.py",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Code refinement
    code_parser = subparsers.add_parser('code', help='Refine code')
    code_parser.add_argument('--file', type=str, help='Code file to refine')
    code_parser.add_argument('--content', type=str, help='Code content (inline)')
    code_parser.add_argument('--output', type=str, help='Output file')
    code_parser.add_argument('--iterations', type=int, default=2, help='Max iterations (default: 2)')
    code_parser.add_argument('--confidence', type=float, default=0.8, help='Confidence threshold (default: 0.8)')
    
    # Text refinement
    text_parser = subparsers.add_parser('text', help='Refine text')
    text_parser.add_argument('--file', type=str, help='Text file to refine')
    text_parser.add_argument('--content', type=str, help='Text content (inline)')
    text_parser.add_argument('--output', type=str, help='Output file')
    text_parser.add_argument('--iterations', type=int, default=2, help='Max iterations (default: 2)')
    
    # Quick functions
    quick_parser = subparsers.add_parser('quick', help='Quick refinement')
    quick_parser.add_argument('type', choices=['code', 'text'], help='Content type')
    quick_parser.add_argument('content', help='Content to refine')
    
    # Demo mode
    demo_parser = subparsers.add_parser('demo', help='Run interactive demo')
    demo_parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print("🎯 SELF-REFINE PIPELINE CLI DEMO")
    print("=" * 50)
    
    if args.command == 'code':
        handle_code_refinement(args)
    elif args.command == 'text':
        handle_text_refinement(args)
    elif args.command == 'quick':
        handle_quick_refinement(args)
    elif args.command == 'demo':
        handle_demo_mode(args)

def handle_code_refinement(args):
    """Handle code refinement"""
    print("🔧 CODE REFINEMENT")
    print("=" * 40)
    
    pipeline = SelfRefinePipeline(
        max_iterations=args.iterations,
        confidence_threshold=args.confidence
    )
    
    # Get content
    if args.file:
        if not Path(args.file).exists():
            print(f"❌ File not found: {args.file}")
            return
        content = Path(args.file).read_text()
        print(f"📁 Processing file: {args.file}")
    elif args.content:
        content = args.content
        print(f"✏️  Processing inline content")
    else:
        print("❌ Error: Must specify --file or --content")
        return
    
    print(f"\n📄 Original content ({len(content)} chars):")
    print("-" * 30)
    print(content[:200] + ("..." if len(content) > 200 else ""))
    
    # Refine
    print(f"\n🚀 Refining (max {args.iterations} iterations, confidence {args.confidence})...")
    results = pipeline.refine(content, RefinementType.CODE)
    
    if not results:
        print("❌ No refinement results")
        return
    
    refined = results[-1].refined
    
    print(f"\n✨ Refined content ({len(refined)} chars):")
    print("-" * 30)
    print(refined)
    
    # Show stats
    print(f"\n📊 Stats:")
    print(f"   Iterations: {len(results)}")
    print(f"   Final confidence: {results[-1].confidence_score:.2f}")
    print(f"   MCP tools used: {results[-1].mcp_tools_used}")
    print(f"   Improvements: {len(results[-1].improvements)}")
    
    # Save if requested
    if args.output:
        Path(args.output).write_text(refined)
        print(f"💾 Saved to: {args.output}")

def handle_text_refinement(args):
    """Handle text refinement"""
    print("📝 TEXT REFINEMENT")
    print("=" * 40)
    
    pipeline = SelfRefinePipeline(max_iterations=args.iterations)
    
    # Get content
    if args.file:
        if not Path(args.file).exists():
            print(f"❌ File not found: {args.file}")
            return
        content = Path(args.file).read_text()
    elif args.content:
        content = args.content
    else:
        print("❌ Error: Must specify --file or --content")
        return
    
    print(f"📄 Original: {content}")
    
    # Refine
    results = pipeline.refine(content, RefinementType.TEXT)
    
    if results:
        print(f"✨ Refined: {results[-1].refined}")
        print(f"📊 Confidence: {results[-1].confidence_score:.2f}")
        
        if args.output:
            Path(args.output).write_text(results[-1].refined)
            print(f"💾 Saved to: {args.output}")

def handle_quick_refinement(args):
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

def handle_demo_mode(args):
    """Handle interactive demo mode"""
    print("🎭 INTERACTIVE DEMO MODE")
    print("=" * 40)
    
    samples = [
        {
            "type": "code",
            "content": "def calc(a,b):return a/b",
            "description": "Simple function with potential division by zero"
        },
        {
            "type": "code", 
            "content": "for i in range(10):\n    print(i)",
            "description": "Basic loop that could be improved"
        },
        {
            "type": "text",
            "content": "This text needs improvement clarity and style",
            "description": "Simple text with redundant words"
        }
    ]
    
    for i, sample in enumerate(samples, 1):
        print(f"\n📋 Sample {i}: {sample['description']}")
        print("-" * 30)
        
        if sample["type"] == "code":
            result = quick_refine_code(sample["content"])
            print(f"🔧 Original: {sample['content']}")
            print(f"✨ Refined: {result}")
        else:
            result = quick_refine_text(sample["content"])
            print(f"📝 Original: {sample['content']}")
            print(f"✨ Refined: {result}")
        
        if args.verbose:
            print("   (Quick refinement used)")
    
    print(f"\n✅ Demo completed! Try the full CLI commands for more control.")

if __name__ == "__main__":
    main() 