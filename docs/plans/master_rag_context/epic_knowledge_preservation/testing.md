# Phase 4A.2 Testing Strategy

## Test Architecture Overview

```
Unit Tests (Component Level)
    ├── SafeKnowledgeExtractor Tests
    ├── SmartCodeDiscovery Tests  
    ├── SessionContextManager Tests
    └── ActiveKnowledgeIntegrator Tests

Integration Tests (Multi-Component)
    ├── Knowledge Extraction → Discovery Pipeline
    ├── Context Preservation → Restoration Flow
    └── Full System Integration

End-to-End Tests (User Scenarios)
    ├── "Have I solved this?" Workflows
    ├── Active Session Management
    └── Solution Auto-tagging

Regression Tests (Safety)
    ├── Existing RAG Functionality
    ├── No Breaking Changes Verification
    └── Performance Benchmarks
```

---

## Unit Test Specifications

### SafeKnowledgeExtractor Tests

**File**: `tests/test_knowledge_extractor.py`

```python
class TestSafeKnowledgeExtractor:
    def test_component_initialization()
    def test_extraction_with_valid_documents()
    def test_extraction_with_empty_documents()
    def test_extraction_with_malformed_documents()
    def test_pattern_extraction_from_code()
    def test_pattern_extraction_from_rules()
    def test_safe_json_storage()
    def test_disable_enable_functionality()
    def test_graceful_fallback_on_error()
```

**Test Data Requirements**:
- Sample rule documents with code patterns
- Malformed/invalid document content
- Empty document sets
- Large document sets (performance testing)

**Expected Results**:
```python
# Valid extraction
result = extractor.extract_code_knowledge()
assert result["success"] == True
assert result["patterns_found"] > 0

# Graceful fallback
extractor.disable()
result = extractor.extract_code_knowledge()
assert result["success"] == False
assert "disabled" in result["reason"]
```

### SmartCodeDiscovery Tests

**File**: `tests/test_code_discovery.py`

```python
class TestSmartCodeDiscovery:
    def test_search_solutions_with_valid_query()
    def test_search_solutions_with_empty_knowledge_base()
    def test_quick_search_functionality()
    def test_pattern_scoring_algorithm()
    def test_suggestion_generation()
    def test_search_performance_limits()
    def test_similarity_scoring_accuracy()
```

**Test Scenarios**:
```python
# Successful search
discovery = SmartCodeDiscovery()
result = discovery.search_solutions("validation pattern")
assert len(result.patterns_found) > 0
assert len(result.suggestions) > 0

# Empty knowledge base
discovery_empty = SmartCodeDiscovery()
# Mock empty patterns file
result = discovery_empty.search_solutions("test")
assert len(result.patterns_found) == 0
assert "No patterns found" in result.suggestions
```

### SessionContextManager Tests

**File**: `tests/test_session_context_manager.py`

```python
class TestSessionContextManager:
    def test_session_context_extraction()
    def test_malformed_session_file_handling()
    def test_context_restoration_prompt_generation()
    def test_problem_type_classification()
    def test_session_snapshot_creation()
    def test_context_file_storage_safety()
```

**Test Data**:
- Valid JSONL session files
- Malformed session files
- Empty session files
- Large session files

### ActiveKnowledgeIntegrator Tests

**File**: `tests/test_active_integration.py`

```python
class TestActiveKnowledgeIntegrator:
    def test_active_session_startup()
    def test_contextual_suggestions_generation()
    def test_solution_auto_tagging()
    def test_related_session_discovery()
    def test_proactive_suggestions()
    def test_component_coordination()
    def test_performance_under_load()
```

---

## Integration Test Specifications

### Knowledge Pipeline Integration

**File**: `tests/test_knowledge_pipeline.py`

```python
class TestKnowledgePipeline:
    def test_extraction_to_discovery_flow():
        """Test full pipeline: extract → store → discover"""
        # 1. Extract knowledge
        extractor = SafeKnowledgeExtractor()
        extraction_result = extractor.extract_code_knowledge()
        
        # 2. Verify storage
        assert Path("data/knowledge/code_patterns.json").exists()
        
        # 3. Test discovery on extracted knowledge
        discovery = SmartCodeDiscovery()
        search_result = discovery.search_solutions("test pattern")
        
        # 4. Verify consistency
        assert len(search_result.patterns_found) <= extraction_result["patterns_found"]
    
    def test_context_preservation_restoration_flow():
        """Test context preservation and restoration"""
        # 1. Extract session context
        manager = SessionContextManager()
        extraction_result = manager.extract_session_context()
        
        # 2. Test restoration
        if extraction_result.session_snapshots > 0:
            # Get first session ID from snapshots
            snapshots_file = Path("data/sessions/context_snapshots/session_contexts.json")
            with open(snapshots_file) as f:
                snapshots = json.load(f)
            
            session_id = snapshots[0]["session_id"]
            restoration_prompt = manager.restore_session_context(session_id)
            
            assert restoration_prompt is not None
            assert "Context Restoration" in restoration_prompt
```

### Multi-Component Integration

**File**: `tests/test_multi_component_integration.py`

```python
class TestMultiComponentIntegration:
    def test_all_components_working_together():
        """Verify all components can work simultaneously"""
        extractor = SafeKnowledgeExtractor()
        discovery = SmartCodeDiscovery()
        context_manager = SessionContextManager()
        integrator = ActiveKnowledgeIntegrator(extractor, discovery, context_manager)
        
        # Test integration functionality
        session_result = integrator.start_active_session("test integration task")
        assert session_result["enabled"] == True
        
        # Test component coordination
        suggestions = integrator.get_contextual_suggestions("test code", "test.py")
        assert isinstance(suggestions, list)
    
    def test_component_independence():
        """Verify components can work independently"""
        # Each component should work even if others fail
        extractor = SafeKnowledgeExtractor()
        discovery = SmartCodeDiscovery()
        
        # Disable one component
        extractor.disable()
        
        # Other should still work
        result = discovery.search_solutions("test")
        assert isinstance(result, DiscoveryResult)
```

---

## End-to-End Test Scenarios

### User Workflow Tests

**File**: `tests/test_e2e_workflows.py`

```python
class TestEndToEndWorkflows:
    def test_have_i_solved_this_workflow():
        """Complete 'Have I solved this before?' workflow"""
        # 1. User starts with a problem
        integrator = ActiveKnowledgeIntegrator()
        
        # 2. Start active session
        session_result = integrator.start_active_session(
            "implement validation system for user input"
        )
        
        # 3. Get suggestions
        suggestions = integrator.get_contextual_suggestions(
            "class ValidationSystem:", 
            "validation.py"
        )
        
        # 4. Implement solution and tag it
        solution_result = integrator.notify_solution_implemented(
            "Implemented input validation with regex patterns",
            "def validate_input(input_str): return bool(re.match(pattern, input_str))"
        )
        
        # 5. Verify workflow completion
        assert session_result["enabled"] == True
        assert solution_result["auto_tagged"] == True
        
        # 6. Verify solution is now discoverable
        discovery = SmartCodeDiscovery()
        search_result = discovery.search_solutions("validation system")
        
        # Should find the newly tagged solution
        found_new_solution = any("validation" in p.description.lower() 
                               for p in search_result.patterns_found)
        assert found_new_solution
    
    def test_session_context_restoration_workflow():
        """Complete session context restoration workflow"""
        # 1. Extract contexts from existing sessions
        manager = SessionContextManager()
        extraction_result = manager.extract_session_context()
        
        # 2. Find related sessions for current problem
        integrator = ActiveKnowledgeIntegrator(context_manager=manager)
        related_sessions = integrator.suggest_related_sessions("implementation problem")
        
        # 3. Restore context if related sessions found
        if related_sessions:
            session_id = related_sessions[0]["session_id"]
            restoration_prompt = manager.restore_session_context(session_id)
            
            assert restoration_prompt is not None
            assert len(restoration_prompt) > 100  # Meaningful content
```

---

## Regression Test Specifications

### Existing Functionality Safety

**File**: `tests/test_regression_safety.py`

```python
class TestRegressionSafety:
    def test_existing_rag_functionality_unchanged():
        """Verify existing RAG system still works"""
        from src.rag_context.enhancer import PromptEnhancer
        
        # Test original RAG functionality
        enhancer = PromptEnhancer()
        
        # This should work exactly as before
        stats = enhancer.get_stats()
        assert "initialized" in stats
        
        # Initialize and test enhancement (if possible in test environment)
        # initialization_result = enhancer.initialize()
        # Enhanced functionality should remain unchanged
    
    def test_no_breaking_changes_to_imports():
        """Verify all imports still work"""
        # Test that all existing imports still work
        from src.rag_context.enhancer import PromptEnhancer
        from src.rag_context.config import RAGConfig
        from src.rag_context.retriever import ContextRetriever
        from src.rag_context.embedder import SimpleEmbedder
        
        # New imports should also work
        from src.rag_context.knowledge_extractor import SafeKnowledgeExtractor
        from src.rag_context.code_discovery import SmartCodeDiscovery
        from src.rag_context.session_context_manager import SessionContextManager
        from src.rag_context.active_knowledge_integration import ActiveKnowledgeIntegrator
        
        # All imports successful
        assert True
    
    def test_file_system_safety():
        """Verify no unwanted file system changes"""
        # Test that components don't create files in wrong locations
        # Test that disable mechanisms work
        # Test that no temp files are left behind
        pass
```

### Performance Regression Tests

**File**: `tests/test_performance_regression.py`

```python
class TestPerformanceRegression:
    def test_component_loading_performance():
        """Verify component loading stays under 2 seconds"""
        import time
        
        # Test individual component loading times
        start_time = time.time()
        extractor = SafeKnowledgeExtractor()
        extractor_time = time.time() - start_time
        
        start_time = time.time()
        discovery = SmartCodeDiscovery()
        discovery_time = time.time() - start_time
        
        start_time = time.time()
        context_manager = SessionContextManager()
        context_time = time.time() - start_time
        
        start_time = time.time()
        integrator = ActiveKnowledgeIntegrator()
        integrator_time = time.time() - start_time
        
        # Performance requirements
        assert extractor_time < 1.0
        assert discovery_time < 1.0
        assert context_time < 1.0
        assert integrator_time < 1.0
        
        total_time = extractor_time + discovery_time + context_time + integrator_time
        assert total_time < 2.0
    
    def test_search_performance():
        """Verify search operations stay under 5 seconds"""
        discovery = SmartCodeDiscovery()
        
        start_time = time.time()
        result = discovery.search_solutions("test query with multiple words")
        search_time = time.time() - start_time
        
        assert search_time < 5.0
        assert result.search_time < 5.0
```

---

## Test Execution Strategy

### Automated Test Pipeline

```bash
# 1. Unit Tests (fast feedback)
pytest tests/test_*_unit.py -v

# 2. Integration Tests (component interaction)
pytest tests/test_*_integration.py -v

# 3. End-to-End Tests (user scenarios)  
pytest tests/test_e2e_*.py -v

# 4. Regression Tests (safety verification)
pytest tests/test_regression_*.py -v

# 5. Performance Tests (benchmarking)
pytest tests/test_performance_*.py -v --benchmark
```

### Test Data Management

```
tests/
├── fixtures/
│   ├── sample_documents/          # For knowledge extraction tests
│   ├── sample_sessions/           # For context management tests
│   ├── sample_patterns/           # For discovery tests
│   └── performance_data/          # For benchmark tests
├── mocks/
│   ├── mock_rag_components.py     # RAG system mocks
│   └── mock_file_system.py       # File system mocks
└── utils/
    ├── test_helpers.py            # Common test utilities
    └── assertions.py              # Custom assertions
```

### Continuous Integration

```yaml
# .github/workflows/phase_4A2_tests.yml
name: Phase 4A.2 Tests

on: [push, pull_request]

jobs:
  test-phase-4a2:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-benchmark
        pip install -r requirements.txt
    
    - name: Run Unit Tests
      run: pytest tests/test_*_unit.py -v
    
    - name: Run Integration Tests  
      run: pytest tests/test_*_integration.py -v
    
    - name: Run Regression Tests
      run: pytest tests/test_regression_*.py -v
    
    - name: Run Performance Tests
      run: pytest tests/test_performance_*.py -v --benchmark-only
```

---

## Success Criteria

### Test Coverage Requirements
- **Unit Tests**: >90% code coverage for all new components
- **Integration Tests**: All component interactions tested
- **End-to-End Tests**: All major user workflows covered
- **Regression Tests**: All existing functionality verified

### Performance Requirements
- **Component Loading**: <1s per component
- **Search Operations**: <5s response time
- **Memory Usage**: <100MB additional memory
- **Storage Growth**: <10MB per 1000 patterns

### Safety Requirements
- **Zero Breaking Changes**: All existing tests pass
- **Graceful Failures**: No crashes on component failures
- **Clean Rollback**: All components can be disabled cleanly
- **Data Integrity**: No data corruption on errors 