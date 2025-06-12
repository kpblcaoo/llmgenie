"""
CLI Tool для командной строки и скриптов
"""

import asyncio
import json
import argparse
import sys
from typing import Dict, Any, Optional
from pathlib import Path

from ..enhancer import PromptEnhancer
from ..config import RAGConfig


class CLITool:
    """CLI инструмент для работы с RAG системой"""
    
    def __init__(self, config: Optional[RAGConfig] = None):
        self.config = config or RAGConfig()
        self.enhancer = PromptEnhancer(self.config)
    
    async def enhance_command(self, query: str, max_context: int = 2000, 
                            output_format: str = "text") -> str:
        """Команда enhance для улучшения промпта"""
        try:
            if max_context != self.config.max_context_length:
                self.config.max_context_length = max_context
            
            enhanced = await self.enhancer.enhance(query)
            
            if output_format == "json":
                result = {
                    "enhanced_query": enhanced,
                    "original_query": query,
                    "added_context_length": len(enhanced) - len(query),
                    "success": True
                }
                return json.dumps(result, indent=2, ensure_ascii=False)
            else:
                return enhanced
        
        except Exception as e:
            if output_format == "json":
                result = {
                    "error": str(e),
                    "original_query": query,
                    "success": False
                }
                return json.dumps(result, indent=2, ensure_ascii=False)
            else:
                return f"Error: {e}\n\nOriginal query: {query}"
    
    async def search_rules_command(self, query: str, max_rules: int = 3,
                                 output_format: str = "text") -> str:
        """Команда поиска релевантных правил"""
        try:
            # Инициализируем если нужно
            if not self.enhancer._initialized:
                await self.enhancer.initialize()
            
            results = self.enhancer.retriever.retrieve(query, max_rules)
            
            if output_format == "json":
                rules = []
                for result in results:
                    rule = {
                        "title": result.document.metadata.get("title", "Untitled"),
                        "content": result.document.content,
                        "source": result.document.source,
                        "score": round(result.score, 3),
                        "type": result.document.doc_type
                    }
                    rules.append(rule)
                
                return json.dumps({
                    "rules": rules,
                    "total_found": len(rules),
                    "success": True
                }, indent=2, ensure_ascii=False)
            
            else:
                # Текстовый формат
                if not results:
                    return f"No relevant rules found for: {query}"
                
                output = [f"Found {len(results)} relevant rules for: {query}\n"]
                
                for i, result in enumerate(results, 1):
                    title = result.document.metadata.get("title", "Untitled")
                    score = result.score
                    source = result.document.source
                    content_preview = result.document.content[:200] + "..." if len(result.document.content) > 200 else result.document.content
                    
                    output.append(f"{i}. {title} (score: {score:.3f})")
                    output.append(f"   Source: {source}")
                    output.append(f"   Preview: {content_preview}")
                    output.append("")
                
                return "\n".join(output)
        
        except Exception as e:
            if output_format == "json":
                return json.dumps({
                    "error": str(e),
                    "success": False
                }, indent=2, ensure_ascii=False)
            else:
                return f"Error searching rules: {e}"
    
    async def stats_command(self, output_format: str = "text") -> str:
        """Команда для получения статистики системы"""
        try:
            stats = self.enhancer.get_stats()
            
            if output_format == "json":
                return json.dumps(stats, indent=2, ensure_ascii=False)
            else:
                # Текстовый формат
                output = ["RAG System Statistics:", ""]
                output.append(f"Initialized: {stats['initialized']}")
                
                if stats['initialized']:
                    output.append(f"Max context length: {stats['config']['max_context_length']}")
                    output.append(f"Similarity threshold: {stats['config']['similarity_threshold']}")
                    output.append(f"Max chunks: {stats['config']['max_chunks']}")
                    
                    if 'embedder' in stats:
                        output.append(f"\nEmbedder cache:")
                        output.append(f"  Cached items: {stats['embedder'].get('cached_items', 0)}")
                        output.append(f"  Cache size: {stats['embedder'].get('cache_size_mb', 0):.2f} MB")
                    
                    if 'retriever' in stats:
                        output.append(f"\nRetriever:")
                        output.append(f"  Indexed documents: {stats['retriever'].get('indexed_documents', 0)}")
                        output.append(f"  Total embeddings: {stats['retriever'].get('total_embeddings', 0)}")
                
                return "\n".join(output)
        
        except Exception as e:
            if output_format == "json":
                return json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
            else:
                return f"Error getting stats: {e}"
    
    async def refresh_command(self, output_format: str = "text") -> str:
        """Команда для обновления индекса"""
        try:
            success = await self.enhancer.refresh_index()
            
            if output_format == "json":
                return json.dumps({
                    "success": success,
                    "message": "Index refreshed successfully" if success else "Failed to refresh index"
                }, indent=2, ensure_ascii=False)
            else:
                return "Index refreshed successfully" if success else "Failed to refresh index"
        
        except Exception as e:
            if output_format == "json":
                return json.dumps({"error": str(e), "success": False}, indent=2, ensure_ascii=False)
            else:
                return f"Error refreshing index: {e}"
    
    async def struct_command(self, output_format: str = "text") -> str:
        """Команда для получения структуры проекта"""
        try:
            # Проверяем поддержку struct.json
            if not self.config.has_struct_support:
                message = {
                    "warning": "struct.json not available",
                    "suggestion": "Run 'lmstruct parse src/ -o struct.json' to generate project structure",
                    "fallback": "Using basic project information instead"
                }
                
                if output_format == "json":
                    return json.dumps(message, indent=2, ensure_ascii=False)
                else:
                    return f"⚠️  {message['warning']}\n💡 {message['suggestion']}\n📝 {message['fallback']}"
            
            with open(self.config.struct_json, 'r', encoding='utf-8') as f:
                struct_data = json.load(f)
            
            if output_format == "json":
                return json.dumps(struct_data, indent=2, ensure_ascii=False)
            else:
                # Простое текстовое представление
                output = ["Project Structure:", ""]
                
                if "name" in struct_data:
                    output.append(f"Name: {struct_data['name']}")
                if "description" in struct_data:
                    output.append(f"Description: {struct_data['description']}")
                if "version" in struct_data:
                    output.append(f"Version: {struct_data['version']}")
                
                # Можно добавить более детальное отображение структуры
                output.append(f"\nFull structure available in JSON format (use --json flag)")
                
                return "\n".join(output)
        
        except Exception as e:
            if output_format == "json":
                return json.dumps({"error": str(e)}, indent=2, ensure_ascii=False)
            else:
                return f"Error reading struct.json: {e}"


def create_parser() -> argparse.ArgumentParser:
    """Создает парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(
        prog="rag-cli",
        description="LLMGenie RAG Context Enhancement CLI Tool"
    )
    
    # Глобальные опции
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--config", type=str, help="Path to custom RAG config file")
    
    # Подкоманды
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # enhance command
    enhance_parser = subparsers.add_parser("enhance", help="Enhance prompt with relevant context")
    enhance_parser.add_argument("query", help="Query to enhance")
    enhance_parser.add_argument("--max-context", type=int, default=2000, 
                               help="Maximum context length (default: 2000)")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search relevant rules")
    search_parser.add_argument("query", help="Query to search rules")
    search_parser.add_argument("--max-rules", type=int, default=3,
                              help="Maximum number of rules (default: 3)")
    
    # stats command
    subparsers.add_parser("stats", help="Show system statistics")
    
    # refresh command
    subparsers.add_parser("refresh", help="Refresh document index")
    
    # struct command
    subparsers.add_parser("struct", help="Show project structure")
    
    return parser


async def main():
    """Главная функция CLI"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Создаем CLI инструмент
    # Можно добавить загрузку кастомной конфигурации из args.config
    cli = CLITool()
    
    # Определяем формат вывода
    output_format = "json" if args.json else "text"
    
    # Выполняем команду
    try:
        if args.command == "enhance":
            result = await cli.enhance_command(
                args.query, 
                args.max_context, 
                output_format
            )
        elif args.command == "search":
            result = await cli.search_rules_command(
                args.query,
                args.max_rules,
                output_format
            )
        elif args.command == "stats":
            result = await cli.stats_command(output_format)
        elif args.command == "refresh":
            result = await cli.refresh_command(output_format)
        elif args.command == "struct":
            result = await cli.struct_command(output_format)
        else:
            parser.print_help()
            sys.exit(1)
        
        print(result)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        if args.json:
            error_result = json.dumps({"error": str(e), "success": False}, indent=2, ensure_ascii=False)
            print(error_result)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 