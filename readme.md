

Сайт для отправки документов.
```
Функционал сайта:
1. Возможность загрузки своего документа
2. Возможность добавление нового пользователя
3. Возможность формирование документа на сайте:

    1. Выбираем тип документа(pdf, csv).
    2. В новом поле пишем то, что должно быть в документе
    3. Сохраняем его локально
    4. Выбираем документ для отправки
    5. Два варианта отправки:
        1. Сразу на email адрес:
            1. Вписываем в поле email и нажимаем отправить
        2. Периодическая отправка:
            1. Выбираем дни/часы/минуты/(с какой периодичностью отправлять) и когда остановить отправку.
            Так же можно добавить календарь для отправки каждую среду, например
    6. Вкладка с историей всех сообщений, отправка которых происходит без расписания
    7. Вкладка с историей всех сообщений, отправка которых происходит по расписанию и дополнительной информацией о них.
       В этой же вкладке возможность редактировать расписание для таска

Стек: Flask, Celery  Сайд требования: Должна быть система аутентификации для пользователя.

Отправку реализовываем селери тасками
Модели: fell free.
На выполнение задания -до 2х дней,когда выполните-сбросьте ссылку на гит)
```

Instalation
```
# install redis and start
# https://redis.io/topics/quickstart

# clone repository
git clone https://github.com/Adviser-ua/documenter.git

# create virtual environment 
virtualenv venv --python=python3.8

# activate venv
source venv/bin/activate

# install requirements
pip install requiremtns.txt

flask db init
flask db migrate
flask db upgrade


```

create directories for upload/create files
```
mkdir -p upload/uploaded
mkdir -p upload/created

```

Configure
```
change parameters in config.py if needed
```

Runing
````
# start developer server
flask run

# in anouther terminal 
sh start_worker.sh

# in anouther terminal
sh start_beat.sh
```
