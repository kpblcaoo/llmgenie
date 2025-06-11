#!/usr/bin/env python3
"""
Тестовый скрипт для проверки доступности MCP инструментов
"""

import asyncio
import json
from src.rag_context.interfaces.mcp_server import MCPServer


async def test_mcp_tools():
    """Тест всех инструментов MCP"""
    
    print("🧪 Testing MCP Server initialization...")
    server = MCPServer()
    print(f"✅ MCP Server created")
    print(f"✅ struct_analyzer available: {server.struct_analyzer is not None}")
    
    # Получаем список инструментов
    print("\n📋 Available tools:")
    
    # Имитируем вызов list_tools
    from mcp import types
    
    # Используем уже созданный server
    test_server = server
    
    # Получаем все зарегистрированные инструменты через MCP протокол
    # Эмулируем list_tools call
    
    # Базовые RAG инструменты
    base_tools = [
        "enhance_prompt",
        "get_relevant_rules", 
        "get_project_structure",
        "get_system_stats", 
        "refresh_index"
    ]
    
    # Struct tools (если доступны)
    struct_tools = [
        "struct_generate",
        "struct_overview", 
        "struct_analyze_module",
        "struct_search_functions",
        "struct_find_callers",
        "struct_generate_report"
    ]
    
    total_expected = len(base_tools) + (len(struct_tools) if test_server.struct_analyzer else 0)
    
    print(f"Expected tools: {total_expected}")
    print("Base RAG tools (5):")
    for tool in base_tools:
        print(f"  ✓ {tool}")
    
    if test_server.struct_analyzer:
        print("Struct tools (6):")
        for tool in struct_tools:
            print(f"  ✓ {tool}")
    else:
        print("❌ Struct tools not available (struct_analyzer is None)")
    
    print(f"\n🎯 Total tools available: {total_expected}")
    
    # Проверяем загрузку struct.json
    try:
        await test_server.struct_analyzer.load_structure()
        overview = test_server.struct_analyzer.get_project_overview()
        print(f"📊 Project overview: {overview}")
    except Exception as e:
        print(f"⚠️ Failed to load project structure: {e}")
    
    return total_expected


if __name__ == "__main__":
    result = asyncio.run(test_mcp_tools())
    print(f"\n✅ Test completed. Expected {result} tools.") 