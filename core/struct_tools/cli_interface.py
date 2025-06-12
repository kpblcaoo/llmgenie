"""
CLI интерфейс для структурного анализа проекта
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from .structure_analyzer import StructureAnalyzer, StructureConfig


class StructureCLI:
    """CLI интерфейс для работы со структурным анализом"""
    
    def __init__(self):
        self.analyzer: Optional[StructureAnalyzer] = None
        self.logger = logging.getLogger(__name__)
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Создание парсера аргументов командной строки"""
        
        parser = argparse.ArgumentParser(
            prog="struct-tools",
            description="Powerful tools for project structure analysis using struct.json and modular index"
        )
        
        parser.add_argument(
            "--project-root", 
            type=Path, 
            default=Path("."),
            help="Project root directory (default: current directory)"
        )
        
        parser.add_argument(
            "--struct-json",
            type=Path,
            default=Path("struct.json"),
            help="Path to struct.json file (default: struct.json)"
        )
        
        parser.add_argument(
            "--modular-index",
            type=Path,
            default=Path("src/.llmstruct_index"),
            help="Path to modular index directory (default: src/.llmstruct_index)"
        )
        
        parser.add_argument(
            "--verbose", "-v",
            action="store_true",
            help="Enable verbose logging"
        )
        
        # Подкоманды
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Generate command
        gen_parser = subparsers.add_parser(
            "generate", 
            help="Generate struct.json and modular index"
        )
        gen_parser.add_argument(
            "target_dir",
            nargs="?",
            default="src",
            help="Directory to analyze (default: src)"
        )
        gen_parser.add_argument(
            "--force", "-f",
            action="store_true",
            help="Force regeneration even if files are fresh"
        )
        gen_parser.add_argument(
            "--exclude-dir",
            action="append",
            default=[],
            help="Directories to exclude from analysis"
        )
        
        # Overview command
        subparsers.add_parser(
            "overview",
            help="Show project structure overview"
        )
        
        # Module command
        mod_parser = subparsers.add_parser(
            "module",
            help="Analyze specific module"
        )
        mod_parser.add_argument(
            "module_path",
            help="Path to module to analyze"
        )
        mod_parser.add_argument(
            "--dependencies", "-d",
            action="store_true",
            help="Show module dependencies"
        )
        mod_parser.add_argument(
            "--complexity", "-c",
            action="store_true",
            help="Show complexity metrics"
        )
        mod_parser.add_argument(
            "--impact", "-i",
            action="store_true",
            help="Show refactoring impact analysis"
        )
        
        # Search command
        search_parser = subparsers.add_parser(
            "search",
            help="Search for functions by pattern"
        )
        search_parser.add_argument(
            "pattern",
            help="Pattern to search for in function names"
        )
        
        # Report command
        report_parser = subparsers.add_parser(
            "report",
            help="Generate architecture report"
        )
        report_parser.add_argument(
            "--output", "-o",
            default="architecture_report.md",
            help="Output file for report (default: architecture_report.md)"
        )
        
        # Find callers command
        callers_parser = subparsers.add_parser(
            "callers",
            help="Find all callers of a function"
        )
        callers_parser.add_argument(
            "function_name",
            help="Name of function to find callers for"
        )
        callers_parser.add_argument(
            "--module",
            help="Limit search to specific module"
        )
        
        return parser
    
    def setup_logging(self, verbose: bool = False):
        """Настройка логирования"""
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
    
    def initialize_analyzer(self, args) -> bool:
        """Инициализация анализатора"""
        config = StructureConfig(
            project_root=args.project_root,
            struct_json_path=args.struct_json,
            modular_index_path=args.modular_index
        )
        
        # Добавляем исключения если указаны
        if hasattr(args, 'exclude_dir') and args.exclude_dir:
            config.exclude_dirs.extend(args.exclude_dir)
        
        self.analyzer = StructureAnalyzer(config)
        return True
    
    def cmd_generate(self, args) -> int:
        """Команда генерации структуры"""
        if not self.analyzer.generate_structure(args.target_dir, args.force):
            print("❌ Failed to generate structure", file=sys.stderr)
            return 1
        
        print("✅ Structure generated successfully")
        
        # Загружаем и показываем краткий обзор
        if self.analyzer.load_structure():
            overview = self.analyzer.get_project_overview()
            print(f"📊 Generated structure with {overview['total_modules']} modules, "
                  f"{overview['total_functions']} functions, {overview['total_classes']} classes")
        
        return 0
    
    def cmd_overview(self, args) -> int:
        """Команда обзора проекта"""
        if not self.analyzer.load_structure():
            print("❌ Failed to load structure. Run 'generate' command first.", file=sys.stderr)
            return 1
        
        overview = self.analyzer.get_project_overview()
        
        print(f"# Project Overview: {overview['project_name']}")
        print(f"")
        print(f"📊 **Statistics:**")
        print(f"- Modules: {overview['total_modules']}")
        print(f"- Functions: {overview['total_functions']}")
        print(f"- Classes: {overview['total_classes']}")
        print(f"- Call Edges: {overview['call_edges']}")
        print(f"- Dependencies: {overview['dependencies']}")
        print(f"")
        print(f"🔍 **Modular Index:** {'✅ Available' if overview['modular_index_available'] else '❌ Not Available'}")
        if overview['modular_index_available']:
            print(f"- Modular modules: {overview['modular_modules_count']}")
        print(f"")
        print(f"📅 **Generated:** {overview['timestamp']}")
        
        return 0
    
    def cmd_module(self, args) -> int:
        """Команда анализа модуля"""
        if not self.analyzer.load_structure():
            print("❌ Failed to load structure. Run 'generate' command first.", file=sys.stderr)
            return 1
        
        module_path = args.module_path
        
        print(f"# Module Analysis: {module_path}")
        print(f"")
        
        if args.dependencies:
            deps = self.analyzer.analyze_module_dependencies(module_path)
            if "error" in deps:
                print(f"❌ {deps['error']}", file=sys.stderr)
                return 1
            
            print(f"## Dependencies")
            print(f"- Imports: {deps['imports_count']}")
            for imp in deps['imports']:
                print(f"  - {imp}")
            print(f"- Functions: {deps['functions_count']}")
            for func in deps['functions']:
                print(f"  - {func}")
            print(f"- Classes: {deps['classes_count']}")
            for cls in deps['classes']:
                print(f"  - {cls}")
            print(f"")
        
        if args.complexity:
            metrics = self.analyzer.get_module_complexity_metrics(module_path)
            if "error" in metrics:
                print(f"❌ {metrics['error']}", file=sys.stderr)
                return 1
            
            print(f"## Complexity Metrics")
            print(f"- Total Functions: {metrics['total_functions']}")
            print(f"- Total Classes: {metrics['total_classes']}")
            print(f"- Total Code Lines: {metrics['total_code_lines']}")
            print(f"- Avg Function Length: {metrics['avg_function_length']:.1f} lines")
            print(f"- Max Function Length: {metrics['max_function_length']} lines")
            print(f"- Avg Class Length: {metrics['avg_class_length']:.1f} lines")
            print(f"- Max Class Length: {metrics['max_class_length']} lines")
            print(f"- **Complexity Score: {metrics['complexity_score']}**")
            print(f"")
        
        if args.impact:
            impact = self.analyzer.get_refactoring_impact(module_path)
            if "error" in impact:
                print(f"❌ {impact['error']}", file=sys.stderr)
                return 1
            
            print(f"## Refactoring Impact")
            print(f"- **Risk Level: {impact['risk_level']}**")
            print(f"- Direct Importers: {impact['direct_importers']}")
            print(f"- Externally Called Functions: {impact['externally_called_functions']}")
            print(f"")
            
            if impact['importers_detail']:
                print(f"### Modules that import this:")
                for imp in impact['importers_detail']:
                    print(f"- {imp['importer_module']} (type: {imp['import_type']})")
                print(f"")
            
            if impact['called_functions_detail']:
                print(f"### Functions called from outside:")
                for call in impact['called_functions_detail']:
                    print(f"- {call['function_name']} ← {call['called_from_module']}::{call['called_from_function']}")
                print(f"")
        
        return 0
    
    def cmd_search(self, args) -> int:
        """Команда поиска функций"""
        if not self.analyzer.load_structure():
            print("❌ Failed to load structure. Run 'generate' command first.", file=sys.stderr)
            return 1
        
        results = self.analyzer.search_functions_by_pattern(args.pattern)
        
        print(f"# Search Results for: '{args.pattern}'")
        print(f"")
        print(f"Found {len(results)} functions:")
        print(f"")
        
        for result in results:
            print(f"- **{result['function_name']}** in `{result['module_path']}`")
            print(f"  - Lines: {result['line_range']}")
            if result['parameters']:
                params = ", ".join(result['parameters'])
                print(f"  - Parameters: {params}")
            print(f"")
        
        return 0
    
    def cmd_callers(self, args) -> int:
        """Команда поиска вызывающих функций"""
        if not self.analyzer.load_structure():
            print("❌ Failed to load structure. Run 'generate' command first.", file=sys.stderr)
            return 1
        
        callers = self.analyzer.find_function_callers(args.function_name, args.module)
        
        print(f"# Callers of: {args.function_name}")
        if args.module:
            print(f"in module: {args.module}")
        print(f"")
        
        if not callers:
            print("No callers found.")
            return 0
        
        print(f"Found {len(callers)} callers:")
        print(f"")
        
        for caller in callers:
            print(f"- **{caller['caller_function']}** in `{caller['caller_module']}`")
            print(f"  - Calls: {caller['target_function']} (type: {caller['call_type']})")
            print(f"")
        
        return 0
    
    def cmd_report(self, args) -> int:
        """Команда генерации отчёта"""
        if not self.analyzer.load_structure():
            print("❌ Failed to load structure. Run 'generate' command first.", file=sys.stderr)
            return 1
        
        if self.analyzer.generate_architecture_report(args.output):
            print(f"✅ Architecture report generated: {args.output}")
            return 0
        else:
            print("❌ Failed to generate report", file=sys.stderr)
            return 1
    
    def run(self, argv=None) -> int:
        """Запуск CLI"""
        parser = self.create_parser()
        args = parser.parse_args(argv)
        
        if not args.command:
            parser.print_help()
            return 1
        
        self.setup_logging(args.verbose)
        
        if not self.initialize_analyzer(args):
            print("❌ Failed to initialize analyzer", file=sys.stderr)
            return 1
        
        # Выполняем команду
        if args.command == "generate":
            return self.cmd_generate(args)
        elif args.command == "overview":
            return self.cmd_overview(args)
        elif args.command == "module":
            return self.cmd_module(args)
        elif args.command == "search":
            return self.cmd_search(args)
        elif args.command == "callers":
            return self.cmd_callers(args)
        elif args.command == "report":
            return self.cmd_report(args)
        else:
            print(f"❌ Unknown command: {args.command}", file=sys.stderr)
            return 1


def main():
    """Точка входа для CLI"""
    cli = StructureCLI()
    return cli.run()


if __name__ == "__main__":
    sys.exit(main()) 