# Переделать

- [x] тексты
- [x] апи
- [x] посмотреть арх
- [x] редис
- [x] подключить редис в старт поллинг
- [x] шедуляр
- [x] set ui commands
- [x] еще раз все проверить
- [x] кеширование запросов
- [x] расставить ttl и обработать ошибки
- [x] gitignore
- [x] расставить логи
- [x] название в pyproject.toml и src/<name>
- [x] докерфайл с volumes
- [x] докер-компоуз
- [ ] подготовить сервер
- [x] в гит
- [ ] почитать про логгирование
- [ ] прокси на Беларусь?
- [ ] на следующий проект посмотреть KeyBuilder
- 
# ПОКА РАБОТАЕТ!!!

# Деплой

- $env:PYTHONPATH="src"
- uv run python src/bot/__main__.py

# Для uv sync

```
[project]
name = "horoscope-bot"
version = "0.1.0"
```
```
[tool.setuptools.packages.find]
where = ["src"]
```

tgbot
botbot