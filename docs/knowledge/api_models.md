# API коммерческих моделей: особенности, best practices и ограничения

## Описание
- Доступ к LLM через API (OpenAI, Anthropic, Google, Cohere и др.).
- Требует API-ключа, соблюдения политики безопасности.

## Особенности
- Ограничения по rate limit, стоимости, SLA.
- Различия в поддержке функций (function calling, streaming, system prompts).

## Best practices
- Использовать официальную документацию.
- Следить за лимитами и стоимостью.
- Для production — реализовать обработку ошибок и fallback.

## Типовые ошибки
- Превышение лимитов API.
- Неправильная обработка ошибок.
- Утечка API-ключа.

## Ссылки
- https://platform.openai.com/docs
- https://docs.anthropic.com/
- https://cloud.google.com/vertex-ai/docs/generative-ai
- https://docs.cohere.com/ 