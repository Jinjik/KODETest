Реализовать API сервис, который включает в себя следующий функционал:

1) Авторизация и регистрация пользователя.

2) Список сообщений блога с постраничной навигацией. Доступно всем. 

3) Получение деталей конкретного сообщения. Доступно всем.

4) Добавление сообщения в блог. Доступно только авторизованным пользователям. Сообщение может состоять из (хотя бы одно обязательно):
    4.1) Текст.
    4.2) Media (картинка / видео) (может быть несколько).
    4.3) Ссылка. По ссылке API должно получить картинку (preview) и краткое содержание (если сервис, на который ведёт ссылка, это позволяет).

5) Лайк сообщения. Доступно только авторизованным пользователям. Один пользователь может лайкнуть сообщение только один раз, при повторном лайке он снимается.

6) Удаление сообщения. Доступно только автору.

Нагрузка на блог неизвестна, но потенциально может быть высокой. 

Дополнительно:
1) Необходимо использовать Python 3.x и FastAPI.
2) Написать спецификацию API (Swagger).
3) Для запуска сервиса использовать Docker.