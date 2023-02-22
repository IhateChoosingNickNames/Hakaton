# Hakaton_recipe_bot 

Hakaton_recipe_bot это проект помогающий найти новые идеи и смыслы на вашей кухне. Огромный выбор блюд, вручную собранный нашей командой с привлечением лучших представителей кулинарного искусства. Удивите любимых и удивитесь сами.

Проект свято придерживается принципов open-source и распространяется под лицензией BSD.

# Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/IhateChoosingNickNames/Hakaton.git
```
```
cd Hackaton
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py bot
```


**Made by**

Ларькин Михаил
Шульгина Наталья
Елизавета Веремьёва
Анатолий Коновалов

### Technologies:
- Python 3.7
- Django 2.2.16
- python-dotenv 0.21.1
- pyTelegramBotAPI 4.10.0
