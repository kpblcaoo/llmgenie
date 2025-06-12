"""
Структурный анализатор проекта - специализированная тулза для работы со struct.json
и modular index (.llmstruct_index/)

Цель: Предоставить мощные инструменты для анализа архитектуры проекта,
понимания зависимостей, call graphs, и планирования изменений.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime
import subprocess


@dataclass
class StructureConfig:
    """Конфигурация для структурного анализа"""
    
    project_root: Path = Path(".")
    struct_json_path: Path = Path("struct.json")
    modular_index_path: Path = Path("src/.llmstruct_index")
    
    # Опции для генерации
    include_ranges: bool = True
    include_hashes: bool = True
    exclude_dirs: List[str] = None
    include_dirs: List[str] = None
    
    def __post_init__(self):
        if self.exclude_dirs is None:
            self.exclude_dirs = ["tests", "__pycache__", ".git", "venv", "node_modules"]
        if self.include_dirs is None:
            self.include_dirs = ["src"]


class StructureAnalyzer:
    """Анализатор структуры проекта на основе struct.json и modular index"""
    
    def __init__(self, config: StructureConfig = None):
        self.config = config or StructureConfig()
        self.struct_data: Optional[Dict] = None
        self.modular_data: Dict[str, Dict] = {}
        self.logger = logging.getLogger(__name__)
    
    def generate_structure(self, target_dir: str = "src", force: bool = False) -> bool:
        """Генерация struct.json и modular index с помощью llmstruct"""
        
        # Проверяем наличие существующих файлов
        if not force and self.config.struct_json_path.exists():
            age_hours = (datetime.now().timestamp() - self.config.struct_json_path.stat().st_mtime) / 3600
            if age_hours < 1:  # Файл свежий (меньше часа)
                self.logger.info(f"struct.json is fresh ({age_hours:.1f}h old), use force=True to regenerate")
                return True
        
        try:
            # Формируем команду llmstruct
            cmd = [
                "lmstruct", "parse",
                "--modular-index",
                "--include-ranges" if self.config.include_ranges else "--no-include-ranges",
                "--include-hashes" if self.config.include_hashes else "--no-include-hashes",
                target_dir,
                "-o", str(self.config.struct_json_path)
            ]
            
            # Добавляем исключения
            for exclude_dir in self.config.exclude_dirs:
                cmd.extend(["--exclude-dir", exclude_dir])
            
            # Добавляем включения
            for include_dir in self.config.include_dirs:
                cmd.extend(["--include-dir", include_dir])
            
            self.logger.info(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.config.project_root)
            
            if result.returncode == 0:
                self.logger.info("struct.json and modular index generated successfully")
                return True
            else:
                self.logger.error(f"llmstruct failed: {result.stderr}")
                return False
                
        except FileNotFoundError:
            self.logger.error("lmstruct command not found. Please install llmstruct.")
            return False
        except Exception as e:
            self.logger.error(f"Failed to generate structure: {e}")
            return False
    
    def load_structure(self) -> bool:
        """Загрузка struct.json и modular index в память"""
        
        # Загружаем основной struct.json
        if not self.config.struct_json_path.exists():
            self.logger.warning(f"struct.json not found at {self.config.struct_json_path}")
            return False
        
        try:
            with open(self.config.struct_json_path, 'r', encoding='utf-8') as f:
                self.struct_data = json.load(f)
            self.logger.info(f"Loaded struct.json with {len(self.struct_data.get('modules', []))} modules")
        except Exception as e:
            self.logger.error(f"Failed to load struct.json: {e}")
            return False
        
        # Загружаем modular index
        if self.config.modular_index_path.exists():
            self._load_modular_index()
        
        return True
    
    def _load_modular_index(self):
        """Загрузка modular index"""
        try:
            # Найдем все .struct.json файлы в индексе
            struct_files = list(self.config.modular_index_path.rglob("*.struct.json"))
            
            for struct_file in struct_files:
                try:
                    with open(struct_file, 'r', encoding='utf-8') as f:
                        module_data = json.load(f)
                    
                    # Ключ - относительный путь модуля
                    module_path = module_data.get("path", str(struct_file.stem))
                    self.modular_data[module_path] = module_data
                    
                except Exception as e:
                    self.logger.warning(f"Failed to load modular data from {struct_file}: {e}")
            
            self.logger.info(f"Loaded modular index with {len(self.modular_data)} modules")
            
        except Exception as e:
            self.logger.error(f"Failed to load modular index: {e}")
    
    def get_project_overview(self) -> Dict[str, Any]:
        """Получить обзор проекта"""
        if not self.struct_data:
            return {"error": "Structure not loaded"}
        
        overview = {
            "project_name": self.struct_data.get("name", "Unknown"),
            "timestamp": self.struct_data.get("timestamp"),
            "total_modules": len(self.struct_data.get("modules", [])),
            "total_functions": sum(len(mod.get("functions", [])) for mod in self.struct_data.get("modules", [])),
            "total_classes": sum(len(mod.get("classes", [])) for mod in self.struct_data.get("modules", [])),
            "call_edges": len(self.struct_data.get("call_graph", {}).get("edges", [])),
            "dependencies": len(self.struct_data.get("dependencies", [])),
            "modular_index_available": len(self.modular_data) > 0,
            "modular_modules_count": len(self.modular_data)
        }
        
        return overview
    
    def analyze_module_dependencies(self, module_path: str) -> Dict[str, Any]:
        """Анализ зависимостей конкретного модуля"""
        if not self.struct_data:
            return {"error": "Structure not loaded"}
        
        # Ищем модуль в данных
        target_module = None
        for module in self.struct_data.get("modules", []):
            if module.get("path") == module_path:
                target_module = module
                break
        
        if not target_module:
            return {"error": f"Module {module_path} not found"}
        
        # Анализ зависимостей
        imports = target_module.get("imports", [])
        functions = target_module.get("functions", [])
        classes = target_module.get("classes", [])
        
        # Получаем детальные данные из modular index если доступно
        modular_detail = self.modular_data.get(module_path, {})
        
        analysis = {
            "module_path": module_path,
            "imports_count": len(imports),
            "imports": imports,
            "functions_count": len(functions),
            "functions": [f.get("name") for f in functions],
            "classes_count": len(classes),
            "classes": [c.get("name") for c in classes],
            "has_modular_detail": module_path in self.modular_data,
            "modular_detail": modular_detail if modular_detail else None
        }
        
        return analysis
    
    def find_function_callers(self, function_name: str, module_path: str = None) -> List[Dict]:
        """Найти все места вызова функции"""
        if not self.struct_data:
            return []
        
        callers = []
        call_graph = self.struct_data.get("call_graph", {})
        edges = call_graph.get("edges", [])
        
        for edge in edges:
            target = edge.get("target", {})
            if target.get("name") == function_name:
                if module_path is None or target.get("module") == module_path:
                    callers.append({
                        "caller_function": edge.get("source", {}).get("name"),
                        "caller_module": edge.get("source", {}).get("module"),
                        "target_function": target.get("name"),
                        "target_module": target.get("module"),
                        "call_type": edge.get("type", "unknown")
                    })
        
        return callers
    
    def get_module_complexity_metrics(self, module_path: str) -> Dict[str, Any]:
        """Получить метрики сложности модуля"""
        if module_path not in self.modular_data:
            return {"error": f"Modular data for {module_path} not available"}
        
        module_data = self.modular_data[module_path]
        functions = module_data.get("functions", [])
        classes = module_data.get("classes", [])
        
        # Подсчет метрик
        total_lines = 0
        function_lines = []
        class_lines = []
        
        for func in functions:
            if "start_line" in func and "end_line" in func:
                lines = func["end_line"] - func["start_line"] + 1
                function_lines.append(lines)
                total_lines += lines
        
        for cls in classes:
            if "start_line" in cls and "end_line" in cls:
                lines = cls["end_line"] - cls["start_line"] + 1
                class_lines.append(lines)
                total_lines += lines
        
        return {
            "module_path": module_path,
            "total_functions": len(functions),
            "total_classes": len(classes),
            "total_code_lines": total_lines,
            "avg_function_length": sum(function_lines) / len(function_lines) if function_lines else 0,
            "max_function_length": max(function_lines) if function_lines else 0,
            "avg_class_length": sum(class_lines) / len(class_lines) if class_lines else 0,
            "max_class_length": max(class_lines) if class_lines else 0,
            "complexity_score": self._calculate_complexity_score(functions, classes)
        }
    
    def _calculate_complexity_score(self, functions: List[Dict], classes: List[Dict]) -> float:
        """Простая метрика сложности модуля"""
        score = 0.0
        
        # Базовые очки за количество
        score += len(functions) * 1.0  # 1 очко за функцию
        score += len(classes) * 3.0    # 3 очка за класс
        
        # Дополнительные очки за параметры функций
        for func in functions:
            params = func.get("parameters", [])
            score += len(params) * 0.5
        
        # Дополнительные очки за методы классов
        for cls in classes:
            methods = cls.get("methods", [])
            score += len(methods) * 1.5
        
        return round(score, 2)
    
    def generate_architecture_report(self, output_path: str = "architecture_report.md") -> bool:
        """Генерация отчёта об архитектуре проекта"""
        if not self.struct_data:
            self.logger.error("Structure not loaded")
            return False
        
        overview = self.get_project_overview()
        
        # Анализ топ модулей по сложности
        complexity_analysis = []
        for module_path in self.modular_data.keys():
            metrics = self.get_module_complexity_metrics(module_path)
            if "error" not in metrics:
                complexity_analysis.append(metrics)
        
        # Сортируем по complexity_score
        complexity_analysis.sort(key=lambda x: x["complexity_score"], reverse=True)
        
        # Генерируем отчёт
        report_lines = [
            f"# Architecture Report - {overview['project_name']}",
            f"",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
            f"**Based on:** {overview['timestamp']}  ",
            f"",
            f"## Project Overview",
            f"",
            f"- **Total Modules:** {overview['total_modules']}",
            f"- **Total Functions:** {overview['total_functions']}",
            f"- **Total Classes:** {overview['total_classes']}",
            f"- **Call Edges:** {overview['call_edges']}",
            f"- **Dependencies:** {overview['dependencies']}",
            f"- **Modular Index:** {'✅ Available' if overview['modular_index_available'] else '❌ Not Available'}",
            f"",
            f"## Top 10 Most Complex Modules",
            f""
        ]
        
        for i, module in enumerate(complexity_analysis[:10]):
            report_lines.extend([
                f"### {i+1}. {module['module_path']}",
                f"",
                f"- **Functions:** {module['total_functions']}",
                f"- **Classes:** {module['total_classes']}",
                f"- **Code Lines:** {module['total_code_lines']}",
                f"- **Complexity Score:** {module['complexity_score']}",
                f"- **Avg Function Length:** {module['avg_function_length']:.1f} lines",
                f"- **Max Function Length:** {module['max_function_length']} lines",
                f""
            ])
        
        # Записываем отчёт
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_lines))
            
            self.logger.info(f"Architecture report generated: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to write report: {e}")
            return False
    
    def search_functions_by_pattern(self, pattern: str) -> List[Dict]:
        """Поиск функций по паттерну в названии"""
        if not self.struct_data:
            return []
        
        results = []
        for module in self.struct_data.get("modules", []):
            for function in module.get("functions", []):
                if pattern.lower() in function.get("name", "").lower():
                    results.append({
                        "function_name": function.get("name"),
                        "module_path": module.get("path"),
                        "line_range": f"{function.get('start_line', '?')}-{function.get('end_line', '?')}",
                        "parameters": function.get("parameters", [])
                    })
        
        return results
    
    def get_refactoring_impact(self, module_path: str) -> Dict[str, Any]:
        """Анализ влияния изменений в модуле на остальной проект"""
        if not self.struct_data:
            return {"error": "Structure not loaded"}
        
        # Находим кто импортирует этот модуль
        importers = []
        for module in self.struct_data.get("modules", []):
            for import_item in module.get("imports", []):
                if module_path in import_item.get("module", ""):
                    importers.append({
                        "importer_module": module.get("path"),
                        "import_type": import_item.get("type"),
                        "imported_names": import_item.get("names", [])
                    })
        
        # Находим функции этого модуля, которые вызываются извне
        called_functions = []
        call_graph = self.struct_data.get("call_graph", {})
        for edge in call_graph.get("edges", []):
            target = edge.get("target", {})
            source = edge.get("source", {})
            
            if target.get("module") == module_path and source.get("module") != module_path:
                called_functions.append({
                    "function_name": target.get("name"),
                    "called_from_module": source.get("module"),
                    "called_from_function": source.get("name")
                })
        
        return {
            "module_path": module_path,
            "direct_importers": len(importers),
            "importers_detail": importers,
            "externally_called_functions": len(called_functions),
            "called_functions_detail": called_functions,
            "risk_level": self._assess_refactoring_risk(len(importers), len(called_functions))
        }
    
    def _assess_refactoring_risk(self, importers_count: int, called_functions_count: int) -> str:
        """Оценка риска рефакторинга"""
        total_usage = importers_count + called_functions_count
        
        if total_usage == 0:
            return "LOW - No external dependencies"
        elif total_usage <= 3:
            return "MEDIUM - Few external dependencies"
        elif total_usage <= 10:
            return "HIGH - Multiple external dependencies"
        else:
            return "CRITICAL - Heavily used module" 