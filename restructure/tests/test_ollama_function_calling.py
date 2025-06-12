#!/usr/bin/env python3
"""
Test script for Ollama function calling capability
Part of Epic 5: MCP-Ollama Integration

This script tests:
1. Basic function calling with different models
2. Performance measurement
3. Quality validation
"""

import json
import time
import requests
from typing import Dict, Any, List
import ollama


def get_current_weather(city: str) -> Dict[str, Any]:
    """
    Get the current weather for a city (mock function for testing)
    
    Args:
        city: The name of the city
        
    Returns:
        dict: Weather information
    """
    # Mock weather data for testing
    weather_data = {
        "Toronto": {"temperature": "22°C", "condition": "Sunny", "humidity": "45%"},
        "Moscow": {"temperature": "-5°C", "condition": "Snow", "humidity": "78%"},
        "London": {"temperature": "15°C", "condition": "Cloudy", "humidity": "60%"},
        "New York": {"temperature": "18°C", "condition": "Rainy", "humidity": "55%"}
    }
    
    return weather_data.get(city, {"temperature": "Unknown", "condition": "Unknown", "humidity": "Unknown"})


def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers together
    
    Args:
        a: The first integer number
        b: The second integer number
        
    Returns:
        int: The sum of the two numbers
    """
    return a + b


def test_model_function_calling(model_name: str) -> Dict[str, Any]:
    """
    Test function calling capability for a specific model
    
    Args:
        model_name: Name of the Ollama model to test
        
    Returns:
        dict: Test results including performance metrics
    """
    print(f"\n🧪 Testing {model_name} function calling...")
    
    # Test 1: Simple math function
    start_time = time.time()
    
    try:
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': 'What is 15 + 27?'}],
            tools=[add_two_numbers]
        )
        
        math_latency = time.time() - start_time
        
        # Execute function if tool call present
        math_result = None
        if response.message.tool_calls:
            tool_call = response.message.tool_calls[0]
            if tool_call.function.name == 'add_two_numbers':
                args = tool_call.function.arguments
                math_result = add_two_numbers(**args)
        
        # Test 2: Weather function
        start_time = time.time()
        
        response2 = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': 'What is the weather in Toronto?'}],
            tools=[get_current_weather]
        )
        
        weather_latency = time.time() - start_time
        
        # Execute weather function if tool call present
        weather_result = None
        if response2.message.tool_calls:
            tool_call = response2.message.tool_calls[0]
            if tool_call.function.name == 'get_current_weather':
                args = tool_call.function.arguments
                weather_result = get_current_weather(**args)
        
        return {
            "model": model_name,
            "status": "success",
            "math_test": {
                "latency": math_latency,
                "tool_calls": len(response.message.tool_calls or []),
                "result": math_result,
                "expected": 42
            },
            "weather_test": {
                "latency": weather_latency,
                "tool_calls": len(response2.message.tool_calls or []),
                "result": weather_result
            },
            "average_latency": (math_latency + weather_latency) / 2
        }
        
    except Exception as e:
        return {
            "model": model_name,
            "status": "failed",
            "error": str(e),
            "latency": None
        }


def test_openai_compatible_endpoint() -> Dict[str, Any]:
    """
    Test OpenAI compatible endpoint functionality
    
    Returns:
        dict: Test results for OpenAI compatibility
    """
    print("\n🔗 Testing OpenAI compatible endpoint...")
    
    try:
        start_time = time.time()
        
        # Test basic completion
        response = requests.post(
            'http://localhost:11434/v1/chat/completions',
            headers={'Content-Type': 'application/json'},
            json={
                'model': 'mistral:7b-instruct',
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': 'Hello! How are you?'}
                ]
            }
        )
        
        latency = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "latency": latency,
                "response_length": len(data.get('choices', [{}])[0].get('message', {}).get('content', '')),
                "model_used": data.get('model', 'unknown')
            }
        else:
            return {
                "status": "failed",
                "error": f"HTTP {response.status_code}: {response.text}",
                "latency": latency
            }
            
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "latency": None
        }


def main():
    """
    Main test execution function
    """
    print("🚀 Epic 5 Phase 1: Ollama Function Calling Tests")
    print("=" * 50)
    
    # List of models to test (will test those that are available)
    models_to_test = [
        'llama3.1:70b-instruct',
        'codellama:34b-instruct', 
        'mistral:7b-instruct'
    ]
    
    # Check which models are available
    try:
        models_response = ollama.list()
        # Handle different response formats
        if hasattr(models_response, 'models'):
            models_list = models_response.models
        elif isinstance(models_response, dict) and 'models' in models_response:
            models_list = models_response['models']
        else:
            models_list = models_response
            
        available_models = [model.name if hasattr(model, 'name') else model['name'] for model in models_list]
        print(f"📦 Available models: {available_models}")
    except Exception as e:
        print(f"❌ Failed to get models list: {e}")
        print("🔄 Trying alternative approach...")
        # Fallback: test with known models
        available_models = ['mistral:7b-instruct', 'codellama:7b', 'mistral:latest']
    
    # Test results storage
    test_results = {}
    
    # Test each available model
    for model in models_to_test:
        if model in available_models:
            result = test_model_function_calling(model)
            test_results[model] = result
        else:
            print(f"⏳ Model {model} not yet available (still downloading?)")
            test_results[model] = {"status": "not_available", "reason": "downloading"}
    
    # Test OpenAI compatibility
    openai_result = test_openai_compatible_endpoint()
    test_results['openai_compatibility'] = openai_result
    
    # Print summary
    print("\n📊 Test Results Summary:")
    print("=" * 50)
    
    for test_name, result in test_results.items():
        print(f"\n🔍 {test_name}:")
        if result['status'] == 'success':
            if 'average_latency' in result:
                print(f"  ✅ Status: {result['status']}")
                print(f"  ⚡ Average Latency: {result['average_latency']:.2f}s")
                print(f"  🧮 Math Result: {result['math_test']['result']} (expected: 42)")
                print(f"  🌤️  Weather Tool Calls: {result['weather_test']['tool_calls']}")
            else:
                print(f"  ✅ Status: {result['status']}")
                print(f"  ⚡ Latency: {result['latency']:.2f}s")
        else:
            print(f"  ❌ Status: {result['status']}")
            if 'error' in result:
                print(f"  🚨 Error: {result['error']}")
    
    # Save results to file
    with open('data/logs/sessions/epic5_ollama_test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n💾 Results saved to: data/logs/sessions/epic5_ollama_test_results.json")
    
    # Performance baseline for future comparison
    successful_models = [name for name, result in test_results.items() 
                        if result.get('status') == 'success' and 'average_latency' in result]
    
    if successful_models:
        avg_latency = sum(test_results[model]['average_latency'] for model in successful_models) / len(successful_models)
        print(f"\n📈 Performance Baseline: {avg_latency:.2f}s average latency")
        print(f"🎯 Ready for Epic 5 Phase 1 completion!")
    else:
        print(f"\n⏳ Models still downloading, will test when ready")


if __name__ == "__main__":
    main() 