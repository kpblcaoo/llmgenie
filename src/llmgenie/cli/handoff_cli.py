#!/usr/bin/env python3
"""
CLI tool for handoff validation
Can be used in CI/CD pipelines and workflows
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

# Add parent directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.handoff_validator import HandoffValidator, HandoffPackage, HandoffFile

def load_handoff_config(config_path: str) -> Dict:
    """Load handoff configuration from JSON file"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        sys.exit(1)

def create_handoff_package_from_config(config: Dict) -> HandoffPackage:
    """Create HandoffPackage from configuration"""
    files = [
        HandoffFile(
            path=f['path'],
            type=f['type'], 
            priority=f['priority']
        ) for f in config['files']
    ]
    
    return HandoffPackage(
        from_role=config['from_role'],
        to_role=config['to_role'],
        epic_id=config['epic_id'],
        files=files,
        startup_prompt=config['startup_prompt'],
        control_questions=config['control_questions'],
        success_criteria=config.get('success_criteria', []),
        metadata=config.get('metadata', {})
    )

def print_validation_result(result, verbose: bool = False):
    """Print validation result to console"""
    
    # Overall status
    status_icon = "✅" if result.is_valid else "❌"
    print(f"\n{status_icon} Handoff Validation {'PASSED' if result.is_valid else 'FAILED'}")
    print(f"📊 Completeness Score: {result.completeness_score:.1%}")
    
    # File validation
    print(f"\n📁 Files ({len(result.file_validation)}):")
    for file_path, is_valid in result.file_validation.items():
        icon = "✅" if is_valid else "❌" 
        print(f"  {icon} {file_path}")
    
    # Warnings
    if result.warnings:
        print(f"\n⚠️  Warnings ({len(result.warnings)}):")
        for warning in result.warnings:
            print(f"   • {warning}")
    
    # Missing files
    if result.missing_files:
        print(f"\n🚫 Missing File Types ({len(result.missing_files)}):")
        for missing in result.missing_files:
            print(f"   • {missing}")
    
    # Recommendations
    if result.recommendations:
        print(f"\n💡 Recommendations ({len(result.recommendations)}):")
        for rec in result.recommendations:
            print(f"   • {rec}")
    
    # Detailed validation (verbose mode)
    if verbose:
        print(f"\n📋 Detailed Validation:")
        
        prompt = result.prompt_validation
        print(f"   Startup Prompt:")
        print(f"     Status: {'✅' if prompt.includes_status else '❌'}")
        print(f"     Infrastructure: {'✅' if prompt.includes_infrastructure else '❌'}")
        print(f"     Lessons: {'✅' if prompt.includes_lessons else '❌'}")
        print(f"     Constraints: {'✅' if prompt.includes_constraints else '❌'}")
        print(f"     Next Steps: {'✅' if prompt.includes_next_steps else '❌'}")
        
        questions = result.questions_validation
        print(f"   Control Questions ({questions.question_count}):")
        print(f"     Status Coverage: {'✅' if questions.covers_status else '❌'}")
        print(f"     Technical Coverage: {'✅' if questions.covers_technical else '❌'}")
        print(f"     Scope Coverage: {'✅' if questions.covers_scope else '❌'}")

def generate_template(output_path: str):
    """Generate handoff template configuration"""
    template = {
        "from_role": "coder",
        "to_role": "reviewer", 
        "epic_id": "epic3-standards-handoff",
        "files": [
            {"path": "docs/conversation_summary.md", "type": "summary", "priority": 1},
            {"path": "data/lessons_learned.md", "type": "lessons", "priority": 2},
            {"path": "docs/epic_checklist.md", "type": "checklist", "priority": 3},
            {"path": "data/audit/technical_report.md", "type": "audit", "priority": 4},
            {"path": "project_state.json", "type": "metadata", "priority": 5}
        ],
        "startup_prompt": "[review] Resuming Epic 3: standards and handoff automation. Status: automation phase complete, validation endpoints implemented. Infrastructure: FastAPI endpoints, CLI tools, atomic rules updated. Lessons: structured validation improves handoff quality. Next: integrate with CI/CD, test workflow.",
        "control_questions": [
            "What is the current epic status and what has been completed?",
            "What technical components are ready for testing and integration?",
            "What scope constraints must be maintained for the handoff?",
            "How should the validation workflow be integrated with existing CI/CD?",
            "What are the next steps for completing the epic?"
        ],
        "success_criteria": [
            "Handoff package validates with 80%+ completeness score",
            "All 5 required file types present and non-empty", 
            "Startup prompt includes status, infrastructure, lessons, constraints, next steps",
            "At least 3 control questions covering status, technical, and scope aspects",
            "Clear success criteria defined for continuation"
        ],
        "metadata": {
            "epic": "epic3-standards-handoff-automation",
            "phase": "automation",
            "branch": "epic3-standards-handoff-automation",
            "session_log": "data/logs/sessions/epic3_standards_handoff_2025-01-05.jsonl"
        }
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Template generated: {output_path}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Handoff validation CLI tool")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate handoff package')
    validate_parser.add_argument('config', help='Path to handoff configuration JSON file')
    validate_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    validate_parser.add_argument('--project-root', default='.', help='Project root directory')
    
    # Template command
    template_parser = subparsers.add_parser('template', help='Generate handoff template')
    template_parser.add_argument('output', help='Output path for template file')
    
    # Check command (for CI/CD)
    check_parser = subparsers.add_parser('check', help='Check handoff (CI/CD mode)')
    check_parser.add_argument('config', help='Path to handoff configuration JSON file')
    check_parser.add_argument('--fail-on-warnings', action='store_true', help='Fail on warnings')
    
    args = parser.parse_args()
    
    if args.command == 'validate':
        # Load configuration
        config = load_handoff_config(args.config)
        
        # Create package
        package = create_handoff_package_from_config(config)
        
        # Validate
        validator = HandoffValidator(args.project_root)
        result = validator.validate_package(package)
        
        # Print results
        print_validation_result(result, args.verbose)
        
        # Exit with error code if validation failed
        sys.exit(0 if result.is_valid else 1)
    
    elif args.command == 'template':
        generate_template(args.output)
    
    elif args.command == 'check':
        # CI/CD mode - minimal output
        config = load_handoff_config(args.config)
        package = create_handoff_package_from_config(config)
        validator = HandoffValidator()
        result = validator.validate_package(package)
        
        if result.is_valid:
            print("✅ HANDOFF_VALIDATION_PASSED")
        else:
            print("❌ HANDOFF_VALIDATION_FAILED")
            print(f"Score: {result.completeness_score:.1%}")
            if result.warnings:
                print("Warnings:", ", ".join(result.warnings))
        
        # Fail on warnings if requested
        if args.fail_on_warnings and result.warnings:
            sys.exit(1)
        
        sys.exit(0 if result.is_valid else 1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 