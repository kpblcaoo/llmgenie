# AI Model Evaluation Framework

## Overview
This framework provides structured guidelines for evaluating different AI models (Claude 3.5 Sonnet, Claude 3.7 Sonnet, Claude 4) within our workflow. The goal is to optimize model selection based on specific task requirements and context handling capabilities.

## Evaluation Criteria

### 1. Context Handling
- **Long Context Retention**: Ability to maintain relevant information across long conversations
- **Context Switching**: Performance when moving between different topics or modes
- **Information Retrieval**: Accuracy in recalling previously mentioned information
- **Session Recovery**: Ability to restore focus after interruptions

### 2. Reasoning Quality
- **Logical Consistency**: Maintaining coherent reasoning across complex tasks
- **Trade-off Analysis**: Identifying and evaluating decision trade-offs
- **Error Detection**: Self-monitoring and correction capabilities
- **Hypothesis Generation**: Quality of suggested approaches and solutions

### 3. Task Completion Efficiency
- **Time to Completion**: Speed of task execution
- **Resource Usage**: Token consumption and computational efficiency
- **Accuracy**: Correctness of task outputs
- **Autonomy**: Level of human intervention required

## Methodology

### Test Cases
1. **Context Retention Test**: Introduce information early in conversation and test recall later
2. **Task Switching Test**: Move between different modes ([code], [meta], [discuss]) and evaluate adaptation
3. **Complex Reasoning Test**: Present multi-step problems requiring trade-off analysis
4. **Workflow Integration Test**: Evaluate adherence to established workflow rules and protocols

### Scoring System
- Each criterion is scored on a 1-5 scale
- Weighted scoring based on task importance
- Comparative analysis across models for the same tasks

## Implementation Guidelines

### For Session Logging
```json
{
  "model_evaluation": {
    "model": "<model_name>",
    "task_id": "<task_identifier>",
    "metrics": {
      "context_handling": {
        "score": <1-5>,
        "notes": "<observations>"
      },
      "reasoning_quality": {
        "score": <1-5>,
        "notes": "<observations>"
      },
      "task_completion": {
        "score": <1-5>,
        "notes": "<observations>"
      }
    },
    "overall_performance": "<summary>"
  }
}
```

### Best Practices
1. **Consistent Testing Environment**: Use the same tasks and conditions across models
2. **Regular Benchmarking**: Re-evaluate models after significant updates
3. **Task-Specific Selection**: Match model capabilities to task requirements
4. **Cost-Benefit Analysis**: Consider token usage and performance trade-offs

## Model Selection Guidelines

### When to Use Claude 3.5 Sonnet
- Simpler tasks with limited context requirements
- Cost-sensitive operations
- Quick iterations during development

### When to Use Claude 3.7 Sonnet
- Balance of performance and efficiency
- Medium-complexity tasks
- Regular workflow operations

### When to Use Claude 4
- Complex reasoning tasks
- Large context windows
- Critical decision-making processes
- Architectural planning

## Documentation Requirements
All evaluation results should be added to:
1. Session logs with the "model_evaluation" tag
2. insights.json with lessons learned
3. This framework document (updated with new findings)

## Integration with Workflow
- Model selection should be documented in session logs
- Context transfer protocol should include model information
- Performance observations should inform future task planning

---

*This framework is a living document and should be updated as new models are tested and new insights are gained.* 