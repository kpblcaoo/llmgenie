"""
MCP Server для интеграции с Cursor, VSCode, Claude Desktop
Объединяет RAG (5 инструментов) + Struct Tools (6 инструментов)
Использует официальный MCP Python SDK
"""

import asyncio
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

try:
    from mcp.server.models import InitializationOptions
    from mcp.server import NotificationOptions, Server
    import mcp.server.stdio
    import mcp.types as types
    MCP_AVAILABLE = True
except ImportError:
    print("Warning: MCP library not installed. Install with: pip install mcp")
    MCP_AVAILABLE = False

from ..enhancer import PromptEnhancer
from ..config import RAGConfig

# Импорт auto_logger для автоматического логирования
try:
    from .auto_logger import auto_logger, detect_and_log_model_context
    AUTO_LOGGING_AVAILABLE = True
except ImportError:
    AUTO_LOGGING_AVAILABLE = False
    auto_logger = None

# Импорт struct_tools для архитектурного анализа
try:
    from ...struct_tools.structure_analyzer import StructureAnalyzer, StructureConfig
    STRUCT_TOOLS_AVAILABLE = True
except ImportError:
    # Пробуем абсолютный импорт как fallback
    try:
        from struct_tools.structure_analyzer import StructureAnalyzer, StructureConfig
        STRUCT_TOOLS_AVAILABLE = True
    except ImportError:
        STRUCT_TOOLS_AVAILABLE = False
        StructureAnalyzer = None
        StructureConfig = None

# Импорт Phase 4A компонентов
try:
    from ..knowledge_extractor import create_knowledge_extractor
    from ..code_discovery import create_discovery_system
    from ..session_context_manager import create_session_context_manager
    from ..cursor_intelligence import create_cursor_intelligence
    PHASE4A_AVAILABLE = True
    print("✅ Phase 4A knowledge_extractor available")
    print("✅ Phase 4A code_discovery available")
    print("✅ Phase 4A session_context_manager available")
    print("✅ Phase 4A cursor_intelligence available")
except ImportError as e:
    PHASE4A_AVAILABLE = False
    print(f"⚠️ Phase 4A components not available: {e}")
    create_knowledge_extractor = None
    create_discovery_system = None
    create_session_context_manager = None
    create_cursor_intelligence = None


class MCPServer:
    """MCP Server для универсального доступа к RAG системе + Struct Tools"""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        if not MCP_AVAILABLE:
            raise ImportError("MCP library required: pip install mcp")
        
        self.config = config or RAGConfig()
        self.enhancer = PromptEnhancer(self.config)
        
        # Инициализируем struct_tools если доступны
        if STRUCT_TOOLS_AVAILABLE:
            struct_config = StructureConfig(
                project_root=Path("."),
                struct_json_path=self.config.struct_json or Path("struct.json")
            )
            self.struct_analyzer = StructureAnalyzer(struct_config)
        else:
            self.struct_analyzer = None
        
        # Инициализируем Phase 4A компоненты если доступны
        self.phase4a_components = {}
        if PHASE4A_AVAILABLE:
            try:
                self.phase4a_components = {
                    'knowledge_extractor': create_knowledge_extractor(self.enhancer),
                    'code_discovery': create_discovery_system(),
                    'session_context_manager': create_session_context_manager(),
                    'cursor_intelligence': create_cursor_intelligence()
                }
                print("✅ Phase 4A components initialized")
            except Exception as e:
                print(f"⚠️ Phase 4A initialization failed: {e}")
                self.phase4a_components = {}
        
        # Создаем MCP сервер
        self.server = Server("llmgenie-rag-struct")
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Настройка MCP handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """Список доступных инструментов"""
            tools = [
                types.Tool(
                    name="enhance_prompt",
                    description="Улучшает промпт добавлением релевантного контекста из правил проекта",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Исходный запрос/задача"
                            },
                            "max_context": {
                                "type": "integer", 
                                "description": "Максимальная длина добавляемого контекста",
                                "default": 2000
                            }
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="get_relevant_rules",
                    description="Возвращает релевантные правила для запроса",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Запрос для поиска правил"
                            },
                            "max_rules": {
                                "type": "integer",
                                "description": "Максимальное количество правил",
                                "default": 3
                            }
                        },
                        "required": ["query"]
                    }
                ),
                types.Tool(
                    name="get_project_structure",
                    description="Возвращает структуру проекта из struct.json",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "random_string": {
                                "type": "string",
                                "description": "Dummy parameter for no-parameter tools"
                            }
                        },
                        "required": ["random_string"]
                    }
                ),
                types.Tool(
                    name="get_system_stats",
                    description="Возвращает статистику RAG системы",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="refresh_index",
                    description="Обновляет индекс документов RAG системы",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                types.Tool(
                    name="discover_code",
                    description="Discover code patterns and knowledge from project",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]
            
            # Добавляем struct_tools если доступны
            if STRUCT_TOOLS_AVAILABLE and self.struct_analyzer:
                tools.extend([
                    types.Tool(
                        name="struct_generate",
                        description="Generate project structure analysis (struct.json + modular index)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "target_dir": {
                                    "type": "string",
                                    "description": "Directory to analyze",
                                    "default": "src"
                                },
                                "force": {
                                    "type": "boolean",
                                    "description": "Force regeneration even if files are fresh",
                                    "default": False
                                }
                            }
                        }
                    ),
                    types.Tool(
                        name="struct_overview",
                        description="Get project statistics and overview",
                        inputSchema={
                            "type": "object",
                            "properties": {},
                            "required": []
                        }
                    ),
                    types.Tool(
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
                    ),
                    types.Tool(
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
                    ),
                    types.Tool(
                        name="struct_find_callers",
                        description="Find functions that call a specific function",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "function_name": {
                                    "type": "string",
                                    "description": "Name of function to find callers for"
                                },
                                "module_filter": {
                                    "type": "string",
                                    "description": "Optional module filter",
                                    "default": None
                                }
                            },
                            "required": ["function_name"]
                        }
                    ),
                    types.Tool(
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
                ])
            
            # Добавляем Phase 4A tools если доступны (начинаем с одного)
            if PHASE4A_AVAILABLE and self.phase4a_components:
                tools.extend([
                    types.Tool(
                        name="extract_code_knowledge", 
                        description="Extract code patterns and knowledge from project for 'Have I solved this before?' functionality",
                        inputSchema={
                            "type": "object", 
                            "properties": {},
                            "required": []
                        }
                    ),
                    types.Tool(
                        name="discover_similar_solutions",
                        description="Find similar solutions to current problem ('Have I solved this before?' functionality)",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string", 
                                    "description": "Problem description to search for"
                                },
                                "max_results": {
                                    "type": "integer",
                                    "description": "Maximum number of results to return",
                                    "default": 5
                                }
                            },
                            "required": ["query"]
                        }
                    ),
                    types.Tool(
                        name="preserve_session_context",
                        description="Extract and preserve session context for future restoration",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "session_file": {
                                    "type": "string",
                                    "description": "Optional specific session file to process"
                                }
                            }
                        }
                    ),
                    types.Tool(
                        name="get_workflow_suggestions", 
                        description="Get workflow intelligence and suggestions for current task context",
                        inputSchema={
                            "type": "object",
                            "properties": {
                                "task_description": {
                                    "type": "string",
                                    "description": "Description of current task/context for analysis"
                                },
                                "session_state": {
                                    "type": "object",
                                    "description": "Current session state for proactive suggestions",
                                    "default": {}
                                }
                            },
                            "required": ["task_description"]
                        }
                    ),
                    types.Tool(
                        name="get_cursor_intelligence",
                        description="Get comprehensive Cursor Intelligence including architectural patterns and development guidance",
                        inputSchema={
                            "type": "object", 
                            "properties": {
                                "functionality_description": {
                                    "type": "string",
                                    "description": "Description of functionality to analyze for architectural patterns"
                                },
                                "analysis_type": {
                                    "type": "string",
                                    "description": "Type of analysis: 'architectural', 'workflow', or 'combined'",
                                    "default": "combined"
                                }
                            },
                            "required": ["functionality_description"]
                        }
                    )
                ])
            
            return tools
        
        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: dict) -> List[types.TextContent]:
            """Обработка вызовов инструментов с автоматическим логированием"""
            import time
            start_time = time.time()
            
            # Автоматическое логирование вызова инструмента
            if AUTO_LOGGING_AVAILABLE and auto_logger:
                # Определяем модель по контексту (если возможно)
                detected_model = detect_and_log_model_context()
                auto_logger.log_tool_call(name, arguments, detected_model)
            
            try:
                result = None
                
                if name == "enhance_prompt":
                    query = arguments["query"]
                    max_context = arguments.get("max_context", 2000)
                    
                    # Обновляем конфигурацию если нужно
                    if max_context != self.config.max_context_length:
                        self.config.max_context_length = max_context
                    
                    enhanced = await self.enhancer.enhance(query)
                    result = [types.TextContent(type="text", text=enhanced)]
                
                elif name == "get_relevant_rules":
                    query = arguments["query"]
                    max_rules = arguments.get("max_rules", 3)
                    
                    # Инициализируем если нужно
                    if not self.enhancer._initialized:
                        await self.enhancer.initialize()
                    
                    # Получаем результаты поиска
                    results = self.enhancer.retriever.retrieve(query, max_rules)
                    
                    rules = []
                    for result_item in results:
                        rule = {
                            "title": result_item.document.metadata.get("title", "Untitled"),
                            "content": result_item.document.content[:500] + "..." if len(result_item.document.content) > 500 else result_item.document.content,
                            "source": result_item.document.source,
                            "score": round(result_item.score, 3),
                            "type": result_item.document.doc_type
                        }
                        rules.append(rule)
                    
                    response = {
                        "rules": rules,
                        "total_found": len(rules)
                    }
                    result = [types.TextContent(type="text", text=json.dumps(response, indent=2, ensure_ascii=False))]
                
                elif name == "get_project_structure":
                    try:
                        if not self.config.has_struct_support:
                            result = [types.TextContent(type="text", text=json.dumps({
                                "warning": "struct.json not available",
                                "suggestion": "Run 'lmstruct parse src/ -o struct.json' to generate project structure",
                                "status": "struct features disabled"
                            }, indent=2, ensure_ascii=False))]
                        else:
                            with open(self.config.struct_json, 'r', encoding='utf-8') as f:
                                struct_data = json.load(f)
                            
                            result = [types.TextContent(type="text", text=json.dumps(struct_data, indent=2, ensure_ascii=False))]
                    except Exception as e:
                        result = [types.TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2, ensure_ascii=False))]
                
                elif name == "get_system_stats":
                    stats = self.enhancer.get_stats()
                    result = [types.TextContent(type="text", text=json.dumps(stats, indent=2, ensure_ascii=False))]
                
                elif name == "refresh_index":
                    success = await self.enhancer.refresh_index()
                    result_data = {
                        "status": "success" if success else "error",
                        "message": "Index refreshed successfully" if success else "Failed to refresh index"
                    }
                    result = [types.TextContent(type="text", text=json.dumps(result_data, indent=2, ensure_ascii=False))]
                
                # Обработчики struct_tools
                elif name.startswith("struct_") and self.struct_analyzer:
                    result = await self._handle_struct_tool(name, arguments)
                
                # Обработчики Phase 4A tools
                elif name == "extract_code_knowledge" and PHASE4A_AVAILABLE and self.phase4a_components:
                    extractor = self.phase4a_components.get('knowledge_extractor')
                    if not extractor:
                        result = [types.TextContent(type="text", text=json.dumps({
                            "error": "Knowledge extractor not available"
                        }, indent=2))]
                    else:
                        extraction_result = extractor.extract_code_knowledge()
                        result = [types.TextContent(type="text", text=json.dumps(extraction_result, indent=2))]
                
                elif name == "discover_similar_solutions" and PHASE4A_AVAILABLE and self.phase4a_components:
                    discovery_system = self.phase4a_components.get('code_discovery')
                    if not discovery_system:
                        result = [types.TextContent(type="text", text=json.dumps({
                            "error": "Discovery system not available"
                        }, indent=2))]
                    else:
                        query = arguments["query"]
                        max_results = arguments.get("max_results", 5)
                        
                        discovery_result = discovery_system.search_solutions(query, max_results)
                        
                        # Convert result to JSON-serializable format
                        response = {
                            "query": discovery_result.query,
                            "patterns_found": len(discovery_result.patterns_found),
                            "search_time": round(discovery_result.search_time, 3),
                            "suggestions": discovery_result.suggestions,
                            "patterns": [
                                {
                                    "name": p.name,
                                    "description": p.description,
                                    "code_snippet": p.code_snippet[:100] + "..." if len(p.code_snippet) > 100 else p.code_snippet,
                                    "source_file": p.source_file,
                                    "pattern_id": p.pattern_id
                                } for p in discovery_result.patterns_found
                            ],
                            "similarity_scores": discovery_result.similarity_scores
                        }
                        result = [types.TextContent(type="text", text=json.dumps(response, indent=2))]
                
                elif name == "preserve_session_context" and PHASE4A_AVAILABLE and self.phase4a_components:
                    session_context_manager = self.phase4a_components.get('session_context_manager')
                    if not session_context_manager:
                        result = [types.TextContent(type="text", text=json.dumps({
                            "error": "Session context manager not available"
                        }, indent=2))]
                    else:
                        session_file = arguments.get("session_file")
                        session_file_path = Path(session_file) if session_file else None
                        
                        extraction_result = session_context_manager.extract_session_context(session_file_path)
                        
                        # Convert dataclass to dict
                        response = {
                            "session_snapshots": extraction_result.session_snapshots,
                            "decisions_extracted": extraction_result.decisions_extracted,
                            "reasoning_chains": extraction_result.reasoning_chains,
                            "extraction_time": round(extraction_result.extraction_time, 3),
                            "success": extraction_result.success,
                            "errors": extraction_result.errors
                        }
                        result = [types.TextContent(type="text", text=json.dumps(response, indent=2))]
                
                elif name == "get_workflow_suggestions" and PHASE4A_AVAILABLE and self.phase4a_components:
                    cursor_intelligence = self.phase4a_components.get('cursor_intelligence')
                    if not cursor_intelligence:
                        result = [types.TextContent(type="text", text=json.dumps({
                            "error": "Cursor intelligence not available"
                        }, indent=2))]
                    else:
                        task_description = arguments["task_description"]
                        session_state = arguments.get("session_state", {})
                        
                        # Analyze workflow context
                        context = {"task_description": task_description}
                        workflow_analysis = cursor_intelligence.analyze_workflow_context(context)
                        
                        # Get proactive suggestions
                        proactive_suggestions = cursor_intelligence.get_proactive_suggestions(session_state)
                        
                        response = {
                            "workflow_analysis": workflow_analysis,
                            "proactive_suggestions": proactive_suggestions,
                            "task_description": task_description,
                            "analysis_timestamp": workflow_analysis.get("timestamp")
                        }
                        suggestions = suggestions_system.get_workflow_suggestions(task_description, session_state)
                        result = [types.TextContent(type="text", text=json.dumps(suggestions, indent=2))]
                
                elif name == "get_cursor_intelligence" and PHASE4A_AVAILABLE and self.phase4a_components:
                    cursor_intelligence = self.phase4a_components.get('cursor_intelligence')
                    if not cursor_intelligence:
                        result = [types.TextContent(type="text", text=json.dumps({
                            "error": "Cursor intelligence not available"
                        }, indent=2))]
                    else:
                        functionality_description = arguments["functionality_description"]
                        analysis_type = arguments.get("analysis_type", "combined")
                        
                        response = {
                            "functionality_description": functionality_description,
                            "analysis_type": analysis_type
                        }
                        
                        if analysis_type in ["architectural", "combined"]:
                            # Get architectural insights
                            arch_insights = cursor_intelligence.architectural_intelligence.suggest_module_placement(functionality_description)
                            response["architectural_insights"] = [cursor_intelligence._insight_to_dict(insight) for insight in arch_insights]
                        
                        if analysis_type in ["workflow", "combined"]:
                            # Get workflow analysis
                            context = {"task_description": functionality_description}
                            workflow_analysis = cursor_intelligence.analyze_workflow_context(context)
                            response["workflow_analysis"] = workflow_analysis
                        
                        response["timestamp"] = datetime.now().isoformat()
                        result = [types.TextContent(type="text", text=json.dumps(response, indent=2))]
                
                else:
                    result = [types.TextContent(type="text", text=f'Error: Unknown tool "{name}"')]
                
                # Автоматическое логирование результата
                if AUTO_LOGGING_AVAILABLE and auto_logger:
                    duration_ms = (time.time() - start_time) * 1000
                    auto_logger.log_tool_result(name, result, duration_ms, detected_model if 'detected_model' in locals() else "unknown")
                
                return result
            
            except Exception as e:
                error_result = [types.TextContent(type="text", text=f'Error: {str(e)}')]
                
                # Логируем ошибку
                if AUTO_LOGGING_AVAILABLE and auto_logger:
                    duration_ms = (time.time() - start_time) * 1000
                    auto_logger.log_tool_result(name, error_result, duration_ms, detected_model if 'detected_model' in locals() else "unknown")
                
                return error_result
    
    async def _handle_struct_tool(self, name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
        """Обработка struct_tools инструментов"""
        try:
            if name == "struct_generate":
                target_dir = arguments.get("target_dir", "src")
                force = arguments.get("force", False)
                
                success = self.struct_analyzer.generate_structure(target_dir, force)
                
                result = {
                    "action": "generate_structure",
                    "success": success,
                    "target_dir": target_dir
                }
                
                if success:
                    # Загружаем и добавляем обзор
                    if self.struct_analyzer.load_structure():
                        overview = self.struct_analyzer.get_project_overview()
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
            
            elif name == "struct_overview":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                overview = self.struct_analyzer.get_project_overview()
                overview["action"] = "project_overview"
                
                return [types.TextContent(type="text", text=json.dumps(overview, indent=2))]
            
            elif name == "struct_analyze_module":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                module_path = arguments["module_path"]
                result = {
                    "action": "analyze_module",
                    "module_path": module_path
                }
                
                # Анализ зависимостей
                if arguments.get("include_dependencies", True):
                    deps = self.struct_analyzer.analyze_module_dependencies(module_path)
                    result["dependencies"] = deps
                
                # Метрики сложности
                if arguments.get("include_complexity", True):
                    complexity = self.struct_analyzer.get_module_complexity_metrics(module_path)
                    result["complexity"] = complexity
                
                # Анализ влияния рефакторинга
                if arguments.get("include_impact", True):
                    impact = self.struct_analyzer.get_refactoring_impact(module_path)
                    result["refactoring_impact"] = impact
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            elif name == "struct_search_functions":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                pattern = arguments["pattern"]
                results = self.struct_analyzer.search_functions_by_pattern(pattern)
                
                response = {
                    "action": "search_functions",
                    "pattern": pattern,
                    "found_count": len(results),
                    "results": results
                }
                
                return [types.TextContent(type="text", text=json.dumps(response, indent=2))]
            
            elif name == "struct_find_callers":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                function_name = arguments["function_name"]
                module_filter = arguments.get("module_filter")
                
                callers = self.struct_analyzer.find_function_callers(function_name, module_filter)
                
                response = {
                    "action": "find_callers",
                    "function_name": function_name,
                    "module_filter": module_filter,
                    "callers_count": len(callers),
                    "callers": callers
                }
                
                return [types.TextContent(type="text", text=json.dumps(response, indent=2))]
            
            elif name == "struct_generate_report":
                if not self.struct_analyzer.load_structure():
                    return [types.TextContent(
                        type="text",
                        text=json.dumps({
                            "error": "Failed to load structure. Run struct_generate first."
                        }, indent=2)
                    )]
                
                output_file = arguments.get("output_file", "architecture_report.md")
                success = self.struct_analyzer.generate_architecture_report(output_file)
                
                result = {
                    "action": "generate_report",
                    "success": success,
                    "output_file": output_file,
                    "message": f"Report generated: {output_file}" if success else "Failed to generate report"
                }
                
                return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
            
            else:
                return [types.TextContent(
                    type="text", 
                    text=json.dumps({"error": f"Unknown struct tool: {name}"}, indent=2)
                )]
                
        except Exception as e:
            return [types.TextContent(
                type="text",
                text=json.dumps({"error": f"Struct tool {name} failed: {str(e)}"}, indent=2)
            )]
    
    async def run_stdio(self):
        """Запуск MCP сервера в stdio режиме (для Cursor)"""
        print("Starting MCP Server in stdio mode...")
        await self.enhancer.initialize()
        
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="llmgenie-rag",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                ),
            )
    
    def get_cursor_config(self) -> Dict[str, Any]:
        """Генерирует конфигурацию для Cursor"""
        return {
            "mcpServers": {
                "llmgenie-rag": {
                    "command": "python",
                    "args": ["-m", "rag_context.interfaces.mcp_server"],
                    "env": {
                        "PYTHONPATH": "."
                    }
                }
            }
        }
    
    def get_vscode_config(self) -> Dict[str, Any]:
        """Генерирует конфигурацию для VSCode"""
        # VSCode может использовать тот же формат что и Cursor
        return self.get_cursor_config()
    
    def save_cursor_config(self, config_path: Optional[Path] = None):
        """Сохраняет конфигурацию для Cursor"""
        if config_path is None:
            config_path = Path.cwd() / ".cursor" / "mcp.json"
        
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(self.get_cursor_config(), f, indent=2)
        
        print(f"Cursor MCP config saved to: {config_path}")


async def main():
    """Главная функция для запуска MCP сервера"""
    import sys
    
    # Создаем и запускаем сервер
    server = MCPServer()
    
    # Сохраняем конфигурацию если нужно
    if "--save-config" in sys.argv:
        server.save_cursor_config()
        print("Configuration saved. Exiting.")
        return
    
    # Запускаем сервер
    await server.run_stdio()


if __name__ == "__main__":
    asyncio.run(main()) 