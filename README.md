# ai-reader

Минималистичный инструмент для извлечения структурированной информации с помощью LLM.

## Быстрый старт

```python
from ai_reader import ExtractorAI, make_gigachat_client

llm_client = make_gigachat_client(credentials="...", scope="GIGACHAT_API_PERS")

extractor = ExtractorAI(llm_client=llm_client)
extractor.load_prepromt("Ты информационный ассистент.")
extractor.load_dict(["имя", "телефон"])
result = extractor.extract("Меня зовут Ольга. Мой телефон: +7-900-555-55-55.")
print(result)
```

`extract` требует корректно настроенный `llm_client`. Если LLM вернула ответ, который нельзя разобрать как JSON с указанными ключами, возбуждается `ValueError`.
