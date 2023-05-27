# spread_wings_bot


## Правила работы с git (как делать коммиты и pull request-ы)

1. Две основные ветки: `master` и `develop`
2. Ветка `develop` — “предрелизная”. Т.е. здесь должен быть рабочий и выверенный код
3. Создавая новую ветку, наследуйтесь от ветки `develop`
4. В `master` находится только production-ready код (CI/CD)
5. Правила именования веток
   - весь новый функционал — `feature/название-функционала`
   - исправление ошибок — `bugfix/название-багфикса`
6. Пушим свою ветку в репозиторий и открываем Pull Request


### Предварительные требования:

1. **Poetry** Зависимости и пакеты управляются через **poetry**. Убедитесь, что **poetry** [установлен](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) на вашем компьютере и ознакомьтесь с [документацией](https://python-poetry.org/docs/cli/).
2. **Docker** В проекте будем использовать MySQL. Рекомендуем запускать БД через Docker, следуя дальнейшим инструкциям.
3. Файлы **requirements** Файлы редактировать вручную не нужно. Обновляются через pre-commit хуки (если есть изменение в зависимостях, то список обновится при коммите).
4. **pre-commit хуки**
   [Документация](https://pre-commit.com)
   При каждом коммите выполняются хуки (автоматизации) перечисленные в **.pre-commit-config.yaml**. Если не понятно какая ошибка мешает сделать коммит можно запустить хуки вручную и посмотреть ошибки:
   ```shell
   pre-commit run --all-files
   ```

#### Poetry

Это инструмент управления зависимостями и виртуальным окружением,
также используется для упаковки проектов на Python.
Подробнее: https://python-poetry.org/

1. Установить, следуя официальным инструкциям.
    https://python-poetry.org/docs/#installation

2. Изменить конфигурацию Poetry (опционально).
    ```shell
    poetry config virtualenvs.in-project true
    ```
    > **Note**:
    > Позволяет создавать виртуальное окружение в папке проекта.

### Работа с Poetry

В этом разделе представлены наиболее часто используемые команды.
Подробнее: https://python-poetry.org/docs/cli/

#### Активировать виртуальное окружение
```shell
poetry shell
```

#### Добавить зависимость
```shell
poetry add <package_name>
```


### Настройка ```pre-comit```:

1. Убедиться, что ```pre-comit``` установлен:
   ```shell
   pre-commit --version
   ```
2. Настроить git hook скрипт:
   ```shell
   pre-commit install
   ```


### Требования к тестам
#### Запуск тестов
Все тесты запускаются командой:
   ```shell
   pytest
   ```
Выборочно тесты запускаются с указанием выбранного файла:
   ```shell
   pytest test_bot.py
   ```

#### Написание тестов
Для написания тестов используется pytest.
Основные настройки тестов хранятся в файле conftest.py.
Фикстуры хранятся в файле fixtures/fixture_data.py
Основные тесты бота хранятся в файле test_bot.py. В зависимости от функционала
тестов можно добавлять файлы тестов. Файлы тестов должны начинаться с "test_".

#### Что необходимо тестировать
Разработчик самостоятельно определяет функционал, который будет покрыт 
данными. Но, как правило, рекомендуется тестировать все написанные 
самостоятельно основные функции бота, функции отправки и получения сообщений,
функции перенаправления на сторонние или внутренние ресурсы.
