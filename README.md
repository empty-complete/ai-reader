 <p align="center">
  <img src="https://i.ibb.co/hJR0N0ht/logo-ai-reader.png" alt="logo-ai-reader" width="100">
</p>
<h1 align="center">AI Reader by kinesis</h1>
<p align="center">
  <i>Минималистичный инструмент для извлечения структурированной информации из текста с помощью <b>LLM</b></i>
</p>

<p align="center">
  <a href="https://github.com/empty-complete/ai-reader/commits">
    <img src="https://img.shields.io/github/commit-activity/m/empty-complete/ai-reader" alt="GitHub Release" />
  </a>
  <a href="https://github.com/empty-complete/ai-reader/blob/main/LICENSE">
    <img alt="MIT Licence" src="https://img.shields.io/badge/Licence-MIT-white?logo=keeweb&logoColor=white">
  </a>
  <a href="https://github.com/empty-complete/ai-reader">
    <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/empty-complete/gift-flipper">
  </a>
</p>

<p align="center">
  <a href="https://t.me/kinesis_lab">
    <img alt="Telegram follow" src="https://img.shields.io/badge/telegram-follow-white?logo=telegram&logoColor=blue&labelColor=white&color=gray">
  </a>
</p>



## Быстрый старт
Делал специально под [gigachat](https://github.com/ai-forever/gigachat)

```python
from ai_reader import ExtractorAI, make_gigachat_client

llm_client = make_gigachat_client(credentials="...", scope="GIGACHAT_API_PERS")

extractor = ExtractorAI(llm_client=llm_client)
extractor.load_prepromt("Ты информационный ассистентe")
extractor.load_dict("имя", "телефон")
result = extractor.extract("Меня зовут Ольга - я являюсь представителем компании LEOJOPA, мой телефон: +7-900-555-55-55.")
print(result)
```

`extract` требует корректно настроенный `llm_client`. Если LLM вернула ответ, который нельзя разобрать как JSON с указанными ключами, возбуждается `ValueError`. Правила извлечения смотри в [тут](https://github.com/empty-complete/ai-reader/blob/main/ai_reader/extractor.py)

## Работа с локальной LLM из LM Studio

LM Studio поднимает OpenAI-совместимый HTTP API (по умолчанию `http://localhost:1234/v1/chat/completions`) см. в [LLM Studio](https://lmstudio.ai/). Для подключения используейте `make_lmstudio_client`:

```python
from ai_reader import ExtractorAI, make_lmstudio_client

llm_client = make_lmstudio_client(
    model="YourModelNameInLMStudio",
    default_system_prompt="Ты информационный ассистент.",
    temperature=0,
)

extractor = ExtractorAI(llm_client=llm_client)
extractor.load_dict("company_name", "contact", "phone", "tags")
result = extractor.extract("Меня зовут Ольга - я являюсь представителем компании LEOJOPA, мой телефон: +7-900-555-55-55.")
print(result)
```

## Дополнительно
Пока не хочу ничего говорить, вариантов использования миллион



*AI-ассистент, ассистент, AI-assistan, LLM*