## Проект «API для YaMDb»
Реализация API сервиса проекта YaMDb для обмена данными на базе DRF.
Проект YaMDb cобирает отзывы (Review) пользователей на произведения (Titles). 
Произведения делятся на категории (Category): «Книги», «Фильмы», «Музыка». 
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).
Новые жанры может создавать только администратор.
Пользовательские оценки формируют рейтинг.
На одно произведение пользователь может оставить только один отзыв.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone
```
```
cd api_yamdb
```
Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
```
```
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Выполнить миграции:
```
python3 manage.py migrate
```
Запустить проект:
```
python3 manage.py runserver
```


### Самостоятельная регистрация новых пользователей
Пользователь отправляет POST-запрос с параметрами email и username на эндпоинт /api/v1/auth/signup/.
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, 
в ответе на запрос ему приходит token (JWT-токен).

### Некоторые примеры запросов к API:
Полный список запросов в документации ReDoc по эндпоинту ...redoc/.

```
.../api/v1/auth/signup/ (POST): Для регистрации в сервисе отправляете POST-запрос с параметрами email и username.
Ждете письмо от YaMDB на указанный вами email с кодом подтверждения (confirmation_code).
```
```
.../api/v1/auth/token/ (POST): Для получения токена доступа отправляете POST-запрос с параметрами username и confirmation_code
```
```
.../api/v1/users/me/ (GET, PATCH): Получить и изменить данные своей учетной записи
```
```
...api/v1/titles/{title_id}/reviews/ (GET): Получить список всех отзывов.
```
```
...api/v1/titles/{title_id}/reviews/ (GET, POST, PATCH, DELETE): Добавить новый отзыв. Доступно только аутентифицированным пользователям.
```
