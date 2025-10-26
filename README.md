# Telegram LLM Bot (OpenAI)

Бот на Python (`python-telegram-bot` v20+) с интеграцией OpenAI.

## Быстрый старт (локально или в Codespaces)

1. Создайте `.env` по образцу `.env.example`:
TELEGRAM_BOT_TOKEN=ваш_токен_бота
OPENAI_API_KEY=ваш_openai_api_key

r
Копировать код

2. Установите зависимости и запустите:
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .\venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python bot.py
В репозитории лежит Yandex-версия (наследие). Этот файл описывает конфигурацию OpenAI. При желании можно полностью мигрировать на OpenAI, удалив Yandex-зависимости.

yaml
Копировать код

---

## Утилиты (опционально)

### `setup.sh`
```bash
#!/usr/bin/env bash
set -e
python -m venv .venv
if [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
fi
pip install --upgrade pip
pip install -r requirements.txt
echo
echo "✅ Готово. Запуск: python bot.py"
