# Jumprope e-commerce

## История появления проекта
Одно из моих хобби - это rope skipping (прыжки со скакалкой с выполнением различных элементов).
В данный момент я хочу создать интернет-магазин, в котором будет продаваться всё необходимое
для этого вида спорта, а также впоследствии будет возможность добавить какие-то обучающие
материалы и т.д.

Поскольку проект довольно большой, в данной работе будет освещена только его часть,
а именно интернет магазин.

## Выбор технологий
Сервис будет раздёлен на back-end и front-end, что позволит добиться следующего:

- Возможность создания современного и красивого интерфейса;
- Возможность со временем разделить обязанности и нанять front-end разработчика;
- Возможность разработать разный front-end для разных устройств, используя
один back-end (например, со временем можно сделать мобильное приложение).

Таким образом, на стороне бэкенда необходимо спроектировать API и реализовать сервер, с учетом требований интернет магазина.

Исходя из этого:
- в качестве фреймворка был выбран FastAPI;
- в качестве ORM будем использовать sqlalchemy;
- используем sqlite (при развёртывании приложения на боевом виртуальном сервере sqlite
будет заменена на postgres).

## Технические особенности и требования:

1) Пользователю не нужно регистрироваться, чтобы сделать заказ

При выработке данного требования я руководствовался следующей логикой:

- Скакалка, коврик для прыжков и т.д. не являются товарами первой необходимости 
и необходимость регистрации, для того чтобы купить товар раз в год, будет раздражать,
что может отпугнуть потенциальных покупателей;
- В дополнение к первому пункту: у пользователя с большой вероятностью уже есть
большое число аккаунтов от других сервисов, и добавлять ещё один не хочется. Учитывая, что
в среднем покупать товар будут не так часто, эти данные пользователь может легко потерять и потом
придётся восстанавливать доступ/создавать новый аккаунт, что создаст отрицательный опыт
при работе с сервисом.
- Пользователь может опасаться рассылки спама с рекламой, что также не добавит
желания создавать аккаунт.

2) Тем не менее в базе данных должна храниться информация пользователя, которую
он указал при заказе (ФИО, email, номер телефона, адрес доставки), что позволит
в будущем перейти к гибридному варианту регистрации. Например, после успешного создания заказа
пользователю можно будет предложить зарегистрироваться, все данные будут уже предзаполнены,
и останется только выбрать пароль. Также можно будет описать плюс регистрации ( "Зарегестрируйтесь, чтобы
совершать покупки быстрее").


3) Необходимо реализовать основные ендпоинты для работы с товарами:
- добавление категории товара;
- добавление характеристики**;
- добавление товара с указанными значениями характеристик;
- просмотр определенного товара;
- просмотр всех товаров с возможностью пагинации, фильтрации по названию, категории и сортировке
по цене;
- обновление количества товара на складе

Прим.

Некоторые из этих ендпоинтов по сути отражают возможности администратора, но в данный
момент требуется реализовать функционал, в будущем некоторые возможности могут переехать в админку
или будут доступны только по авторизации для администратора.

** Характеристика, а именно её название (например, длина скакалки) вынесена в отдельную
сущность в БД и работа админа с товарами представляется примерно так:

Добавить категорию -> добавить характеристики товаров (длина троса, цвет ручки,
цвет троса и т.д.) -> добавление товара с указанными значениями данных характеристик.

Заметим что в последнем пункте добавить товар означает описать товар, который будет
продаваться, самого товара в наличии на складе может ещё и не быть, поэтому автоматически
в таблицу инвентаризации будет записан 0. На фронтенде такой случай можно поддержать так:
"Скоро появится в продаже(новинка)/товар распродан(уже был на сайте)". Для учёта физического количества товаров предусмотрен
отдельный ендпоинт.


4. Склад будет один, поэтому в базе данных просто учитываем количество каждого товара.


5. Считаем, что на ендпоинт для создания заказа пришла общая сумма с учётом, например, оптовых скидок и т.д.
Т.е. корзина покупателя обрабатывается на фронтенде и временно хранится в Session Storage/Local Storage.
Сервер не хранит сессии пользователя, т.о. сервис является stateless.
Также:
- Считаем, что список товаров, полученный в деталях заказа верный, то есть
в нём нет несуществующих товаров, однако перед формированием заказа необходимо
проверить, что на складе есть достаточное количество товара.
- Как было сказано выше, данные пользователя при создании заказа также вносятся
в таблицу.

6. Добавить ендпоинт для завершения заказа (Пользователь оплатил -> заказ упаковали ->
админ переводит заказ в статус выполненных)


7. Добавить админку, проработать ограничения на действия админа по каждой из таблиц.


## Makefile commands

### Create venv:
    make venv

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format

### Run service:
    make up

You can then access the service at 
```
http://localhost:80/
```

and admin panel at:
```
http://localhost:5000/admin
```

## API Endpoints

| HTTP Method | Endpoint                             | Action                                                        | Response                     |
|-------------|--------------------------------------|---------------------------------------------------------------|------------------------------|
| POST        | /api/products/categories             | To add category                                               | Category information         | 
| POST        | /api/products/characteristic         | To add characteristic                                         | Characteristic information   | 
| GET         | /api/products/                       | To get a list of products with certain filters and pagination | List of products             |
| POST        | /api/products/                       | To add product                                                | Product information          |
| GET         | /api/products/{product_id}           | To get information about product whose id is `product_id`     | Product information          |
| PATCH       | /api/products/{product_id}/inventory | To increase product quantity                                  | Product quantity information |
| POST        | /api/orders/                         | To create order                                               | Order information            |
| PATCH       | /api/orders/{order_id}               | To complete order                                             | Completed order information  |

To get full details about endpoints go to  
```
http://localhost:80/docs
```


## Technologies Used

- Python
- Poetry
- FastAPI
- Flask-Admin
- SQLAlchemy
- Pytest
- Git
- GitHub
- Docker
- Docker Compose

## Authors

- [@AndrejTsvetkov](https://www.github.com/AndrejTsvetkov)

