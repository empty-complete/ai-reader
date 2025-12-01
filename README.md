# ai-reader

Минималистичный инструмент для извлечения структурированной информации с помощью LLM.

## Быстрый старт

```python
from ai_reader import ExtractorAI

extractor = ExtractorAI()
extractor.load_prepromt("Ты информационный ассистент.")
extractor.load_dict(["имя", "телефон"])
result = extractor.extract("Меня зовут Ольга. Мой телефон: +7-900-555-55-55.")
print(result)
```

Если `ExtractorAI` создан без `llm_client`, то метод `extract` просто вернёт словарь с указанными ключами и пустыми значениями — это удобный fallback, когда LLM недоступна.
