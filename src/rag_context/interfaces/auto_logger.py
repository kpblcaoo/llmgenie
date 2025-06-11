"""
Auto Logger for MCP Server Integration
Automatic workflow logging without efficiency loss
Part of Phase 4A.2: Agent-as-a-Judge Enhanced
"""

import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import hashlib
import re

class AutoLogger:
    """Automatic logging system for MCP workflow events"""
    
    def __init__(self, session_log_path: str = "data/logs/sessions/"):
        self.session_log_path = Path(session_log_path)
        self.session_log_path.mkdir(parents=True, exist_ok=True)
        self.current_session = None
        self.model_patterns = {
            'claude_sonnet': ['claude', 'sonnet', 'anthropic'],
            'gemini_flash': ['gemini', 'flash', 'google'],
            'gpt': ['gpt', 'openai', 'chatgpt']
        }
        
    def detect_model(self, context: str = "") -> str:
        """Detect current model based on context clues"""
        context_lower = context.lower()
        
        for model_name, patterns in self.model_patterns.items():
            if any(pattern in context_lower for pattern in patterns):
                return model_name
                
        return "unknown"
    
    def ensure_session(self, session_name: str = None) -> str:
        """Ensure active session exists, create if needed"""
        if not session_name:
            session_name = f"auto_session_{datetime.now().strftime('%Y-%m-%d_%H-%M')}"
            
        self.current_session = session_name
        return session_name
    
    def log_tool_call(self, tool_name: str, arguments: Dict[str, Any], 
                      model: str = "unknown", session: str = None) -> None:
        """Log MCP tool call with automatic metadata"""
        session = session or self.ensure_session()
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "tool_call_auto",
            "tool": tool_name,
            "model": model,
            "session": session,
            "automatic": True,
            "args_hash": self._hash_args(arguments),
            "args_summary": self._summarize_args(arguments)
        }
        
        self._append_to_log(event, session)
    
    def log_tool_result(self, tool_name: str, result: Any, 
                       duration_ms: float = 0, model: str = "unknown") -> None:
        """Log tool result with performance metrics"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "tool_result_auto",
            "tool": tool_name,
            "model": model,
            "session": self.current_session,
            "automatic": True,
            "duration_ms": duration_ms,
            "result_size": len(str(result)) if result else 0,
            "success": result is not None
        }
        
        self._append_to_log(event, self.current_session)
    
    def log_model_switch(self, from_model: str, to_model: str, 
                        context: str = "") -> None:
        """Log model switches for continuity tracking"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "model_switch_auto",
            "from_model": from_model,
            "to_model": to_model,
            "context": context,
            "session": self.current_session,
            "automatic": True
        }
        
        self._append_to_log(event, self.current_session)
    
    def log_workflow_phase(self, phase: str, detected_by: str = "auto") -> None:
        """Log workflow phase transitions"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "workflow_phase_auto",
            "phase": phase,
            "detected_by": detected_by,
            "session": self.current_session,
            "automatic": True
        }
        
        self._append_to_log(event, self.current_session)
    
    def analyze_activity_pattern(self, recent_events: List[Dict]) -> Dict[str, Any]:
        """Analyze recent activity to detect workflow patterns"""
        if not recent_events:
            return {"pattern": "no_activity", "confidence": 1.0}
        
        # Constants for pattern detection
        STRUCT_TOOLS_PREFIX = "struct_"
        CONTEXT_TOOLS = {"enhance_prompt", "get_relevant_rules"}
        
        tool_usage = {}
        models_used = set()
        event_timespan = self._calculate_timespan(recent_events)
        
        for event in recent_events:
            if event.get("tool"):
                tool_usage[event["tool"]] = tool_usage.get(event["tool"], 0) + 1
            if event.get("model"):
                models_used.add(event["model"])
        
        # Improved pattern detection with confidence calculation
        pattern, confidence = self._detect_pattern_with_confidence(
            tool_usage, models_used, event_timespan
        )
        
        return {
            "pattern": pattern,
            "confidence": confidence,
            "tools_used": list(tool_usage.keys()),
            "models_involved": list(models_used),
            "activity_level": len(recent_events),
            "timespan_minutes": event_timespan.total_seconds() / 60 if event_timespan else 0
        }

    def _detect_pattern_with_confidence(self, tool_usage: Dict, models_used: set, timespan) -> tuple:
        """Detect patterns with evidence-based confidence scoring"""
        CONTEXT_TOOLS = {"enhance_prompt", "get_relevant_rules"}
        
        struct_tool_count = sum(1 for tool in tool_usage.keys() if tool.startswith("struct_"))
        context_tool_count = sum(tool_usage.get(tool, 0) for tool in CONTEXT_TOOLS)
        
        # Evidence-based pattern detection
        if struct_tool_count >= 2:
            confidence = min(0.9, 0.6 + (struct_tool_count * 0.1))
            return "architecture_analysis", confidence
        elif context_tool_count >= 3:
            confidence = min(0.85, 0.5 + (context_tool_count * 0.1))
            return "context_enhancement", confidence
        elif len(models_used) > 1:
            confidence = 0.75 if len(models_used) > 2 else 0.6
            return "model_collaboration", confidence
        else:
            confidence = 0.5 + min(0.3, len(tool_usage) * 0.05)
            return "focused_work", confidence

    def _calculate_timespan(self, events: List[Dict]) -> Optional[Any]:
        """Calculate time span of events"""
        if len(events) < 2:
            return None
        
        try:
            start_time = datetime.fromisoformat(events[0]["timestamp"].replace('Z', '+00:00'))
            end_time = datetime.fromisoformat(events[-1]["timestamp"].replace('Z', '+00:00'))
            return end_time - start_time
        except (KeyError, ValueError):
            return None
    
    def generate_session_summary(self, session: str = None) -> Dict[str, Any]:
        """Generate automatic session summary"""
        session = session or self.current_session
        if not session:
            return {"error": "No active session"}
        
        log_file = self.session_log_path / f"{session}.jsonl"
        if not log_file.exists():
            return {"error": "Session log not found"}
        
        events = []
        with open(log_file, 'r') as f:
            for line in f:
                try:
                    events.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        
        if not events:
            return {"summary": "empty_session"}
        
        # Analyze session
        tools_used = set()
        models_used = set()
        phases = set()
        auto_events = 0
        
        for event in events:
            if event.get("tool"):
                tools_used.add(event["tool"])
            if event.get("model"):
                models_used.add(event["model"])
            if event.get("phase"):
                phases.add(event["phase"])
            if event.get("automatic"):
                auto_events += 1
        
        return {
            "session": session,
            "total_events": len(events),
            "automatic_events": auto_events,
            "manual_events": len(events) - auto_events,
            "tools_used": list(tools_used),
            "models_used": list(models_used),
            "phases_detected": list(phases),
            "start_time": events[0].get("timestamp"),
            "end_time": events[-1].get("timestamp"),
            "coverage_score": auto_events / len(events) if events else 0
        }
    
    def _hash_args(self, args: Dict[str, Any]) -> str:
        """Create hash of arguments for deduplication"""
        args_str = json.dumps(args, sort_keys=True)
        return hashlib.md5(args_str.encode()).hexdigest()[:8]
    
    def _summarize_args(self, args: Dict[str, Any]) -> str:
        """Create human-readable summary of arguments"""
        if not args:
            return "no_args"
        
        summary_parts = []
        for key, value in args.items():
            if isinstance(value, str) and len(value) > 50:
                summary_parts.append(f"{key}={value[:47]}...")
            else:
                summary_parts.append(f"{key}={value}")
        
        return ", ".join(summary_parts[:3])  # Limit to first 3 args
    
    def _append_to_log(self, event: Dict[str, Any], session: str) -> None:
        """Append event to session log file"""
        if not session:
            return
        
        log_file = self.session_log_path / f"{session}.jsonl"
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(event, ensure_ascii=False) + '\n')
        except Exception as e:
            # Fallback to stderr if file writing fails
            print(f"AutoLogger error: {e}", file=__import__('sys').stderr)

# Global instance for easy integration
auto_logger = AutoLogger()

def log_mcp_tool_call(tool_name: str, arguments: Dict[str, Any], 
                      model: str = "unknown") -> None:
    """Convenience function for MCP tool call logging"""
    auto_logger.log_tool_call(tool_name, arguments, model)

def log_mcp_tool_result(tool_name: str, result: Any, 
                       duration_ms: float = 0, model: str = "unknown") -> None:
    """Convenience function for MCP tool result logging"""
    auto_logger.log_tool_result(tool_name, result, duration_ms, model)

def detect_and_log_model_context(context: str = "") -> str:
    """Detect model from context and log if switch detected"""
    detected_model = auto_logger.detect_model(context)
    
    # If we have a previous model and it's different, log the switch
    if (hasattr(auto_logger, '_last_model') and 
        auto_logger._last_model != detected_model and 
        detected_model != "unknown"):
        auto_logger.log_model_switch(auto_logger._last_model, detected_model, context)
    
    auto_logger._last_model = detected_model
    return detected_model 