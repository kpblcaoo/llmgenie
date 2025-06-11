"""
MCP интерфейс для структурного анализа проекта
Интеграция struct_tools с Model Context Protocol для Cursor IDE
"""

import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    from mcp import types
    from mcp.server import Server
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # Заглушки для типов
    class types:
        class Tool:
            def __init__(self, **kwargs): pass
        class TextContent:
            def __init__(self, **kwargs): pass
        class CallToolRequest:
            def __init__(self, **kwargs): pass
        class CallToolResult:
            def __init__(self, **kwargs): pass

from .structure_analyzer import StructureAnalyzer, StructureConfig


class StructureMCPServer:
    """MCP сервер для структурного анализа"""
    
    def __init__(self, config: StructureConfig = None):
        if not MCP_AVAILABLE:
            raise ImportError("MCP not available. Install with: pip install mcp")
        
        self.config = config or StructureConfig()
        self.analyzer = StructureAnalyzer(self.config)
        self.server = Server("struct-tools")
        self.logger = logging.getLogger(__name__)
        
        self._setup_tools()
        self._setup_handlers()
    
    def _setup_tools(self):
        """Настройка инструментов MCP"""
        
        # Генерация структуры
        self.server.tool(
            name="struct_generate",
            description="Generate struct.json and modular index for project analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "target_dir": {
                        "type": "string",
                        "description": "Directory to analyze (default: src)",
                        "default": "src"
                    },
                    "force": {
                        "type": "boolean",
                        "description": "Force regeneration even if files are fresh",
                        "default": False
                    }
                }
            }
        )
        
        # Обзор проекта
        self.server.tool(
            name="struct_overview",
            description="Get project structure overview with statistics",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
        
        # Анализ модуля
        self.server.tool(
            name="struct_analyze_module",
            description="Analyze specific module: dependencies, complexity, refactoring impact",
            inputSchema={
                "type": "object",
                "properties": {
                    "module_path": {
                        "type": "string",
                        "description": "Path to module to analyze"
                    },
                    "include_dependencies": {
                        "type": "boolean",
                        "description": "Include dependency analysis",
                        "default": True
                    },
                    "include_complexity": {
                        "type": "boolean",
                        "description": "Include complexity metrics",
                        "default": True
                    },
                    "include_impact": {
                        "type": "boolean",
                        "description": "Include refactoring impact analysis",
                        "default": True
                    }
                },
                "required": ["module_path"]
            }
        )
        
        # Поиск функций
        self.server.tool(
            name="struct_search_functions",
            description="Search for functions by pattern in their names",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Pattern to search for in function names"
                    }
                },
                "required": ["pattern"]
            }
        )
        
        # Поиск вызывающих функций
        self.server.tool(
            name="struct_find_callers",
            description="Find all functions that call a specific function",
            inputSchema={
                "type": "object",
                "properties": {
                    "function_name": {
                        "type": "string",
                        "description": "Name of function to find callers for"
                    },
                    "module_filter": {
                        "type": "string",
                        "description": "Optional module to limit search to"
                    }
                },
                "required": ["function_name"]
            }
        )
        
        # Генерация отчёта
        self.server.tool(
            name="struct_generate_report",
            description="Generate comprehensive architecture report",
            inputSchema={
                "type": "object",
                "properties": {
                    "output_file": {
                        "type": "string",
                        "description": "Output file path",
                        "default": "architecture_report.md"
                    }
                }
            }
        )
    
    def _setup_handlers(self):
        """Настройка обработчиков"""
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
            """Обработка вызовов инструментов"""
            
            try:
                if name == "struct_generate":
                    return await self._handle_generate(arguments)
                elif name == "struct_overview":
                    return await self._handle_overview(arguments)
                elif name == "struct_analyze_module":
                    return await self._handle_analyze_module(arguments)
                elif name == "struct_search_functions":
                    return await self._handle_search_functions(arguments)
                elif name == "struct_find_callers":
                    return await self._handle_find_callers(arguments)
                elif name == "struct_generate_report":
                    return await self._handle_generate_report(arguments)
                else:
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
                    )]
                    
            except Exception as e:
                self.logger.error(f"Tool {name} failed: {e}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]
    
    async def _handle_generate(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка генерации структуры"""
        target_dir = args.get("target_dir", "src")
        force = args.get("force", False)
        
        success = self.analyzer.generate_structure(target_dir, force)
        
        result = {
            "action": "generate_structure",
            "success": success,
            "target_dir": target_dir
        }
        
        if success:
            # Загружаем и добавляем обзор
            if self.analyzer.load_structure():
                overview = self.analyzer.get_project_overview()
                result.update({
                    "overview": overview,
                    "message": f"Generated structure with {overview['total_modules']} modules, "
                              f"{overview['total_functions']} functions, {overview['total_classes']} classes"
                })
            else:
                result["message"] = "Structure generated but failed to load for overview"
        else:
            result["message"] = "Failed to generate structure"
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def _handle_overview(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка обзора проекта"""
        if not self.analyzer.load_structure():
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": "Failed to load structure. Run struct_generate first."
                }, indent=2)
            )]
        
        overview = self.analyzer.get_project_overview()
        overview["action"] = "project_overview"
        
        return [types.TextContent(type="text", text=json.dumps(overview, indent=2))]
    
    async def _handle_analyze_module(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка анализа модуля"""
        if not self.analyzer.load_structure():
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": "Failed to load structure. Run struct_generate first."
                }, indent=2)
            )]
        
        module_path = args["module_path"]
        result = {
            "action": "analyze_module",
            "module_path": module_path
        }
        
        # Анализ зависимостей
        if args.get("include_dependencies", True):
            deps = self.analyzer.analyze_module_dependencies(module_path)
            result["dependencies"] = deps
        
        # Метрики сложности
        if args.get("include_complexity", True):
            complexity = self.analyzer.get_module_complexity_metrics(module_path)
            result["complexity"] = complexity
        
        # Анализ влияния рефакторинга
        if args.get("include_impact", True):
            impact = self.analyzer.get_refactoring_impact(module_path)
            result["refactoring_impact"] = impact
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def _handle_search_functions(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка поиска функций"""
        if not self.analyzer.load_structure():
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": "Failed to load structure. Run struct_generate first."
                }, indent=2)
            )]
        
        pattern = args["pattern"]
        results = self.analyzer.search_functions_by_pattern(pattern)
        
        response = {
            "action": "search_functions",
            "pattern": pattern,
            "found_count": len(results),
            "results": results
        }
        
        return [types.TextContent(type="text", text=json.dumps(response, indent=2))]
    
    async def _handle_find_callers(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка поиска вызывающих функций"""
        if not self.analyzer.load_structure():
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": "Failed to load structure. Run struct_generate first."
                }, indent=2)
            )]
        
        function_name = args["function_name"]
        module_filter = args.get("module_filter")
        
        callers = self.analyzer.find_function_callers(function_name, module_filter)
        
        response = {
            "action": "find_callers",
            "function_name": function_name,
            "module_filter": module_filter,
            "callers_count": len(callers),
            "callers": callers
        }
        
        return [types.TextContent(type="text", text=json.dumps(response, indent=2))]
    
    async def _handle_generate_report(self, args: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка генерации отчёта"""
        if not self.analyzer.load_structure():
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": "Failed to load structure. Run struct_generate first."
                }, indent=2)
            )]
        
        output_file = args.get("output_file", "architecture_report.md")
        success = self.analyzer.generate_architecture_report(output_file)
        
        result = {
            "action": "generate_report",
            "success": success,
            "output_file": output_file,
            "message": f"Report generated: {output_file}" if success else "Failed to generate report"
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    async def run_stdio(self):
        """Запуск MCP сервера в stdio режиме"""
        if not MCP_AVAILABLE:
            raise ImportError("MCP not available")
        
        # Импортируем stdio transport
        from mcp.server.stdio import stdio_server
        
        self.logger.info("Starting Struct Tools MCP Server in stdio mode...")
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream)


# Функция для создания и запуска MCP сервера
async def run_struct_mcp_server():
    """Запуск MCP сервера для struct_tools"""
    server = StructureMCPServer()
    await server.run_stdio()


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_struct_mcp_server()) 