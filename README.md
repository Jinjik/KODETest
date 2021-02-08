# Тестовое задание от KODE

## [Тестовое задание](tz.md)

## Руководство по запуску:

### Install docker
```commandline
cd KODETest/
docker-compose up -d build
```

## API:

Регистрация: [/users/](http://localhost:8002/users/)
POST-запрос

Получение токена: [/token/](http://localhost:8002/token/)
POST-запрос

Создание поста: [/posts/](http://localhost:8002/posts/)
POST-запрос

Получение всех постов: [/posts/](http://localhost:8002/posts/)
GET-запрос

Получение конкретного поста: [/posts/{post_id}/](http://localhost:8002/posts/{post_id}/)
POST-запрос

Поставить/убрать лайк: [/posts/{post_id}/like](http://localhost:8002/posts/{post_id}/like/)
POST-запрос

Изменить пост: [/posts/{post_id}/](http://localhost:8002/posts/{post_id}/)
POST-запрос

Удалить пост: [/posts/{post_id}/](http://localhost:8002/posts/{post_id}/)
DELETE-запрос
