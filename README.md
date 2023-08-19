# Airport Api Service

API service for tracking flights from airports written on DRF
  # Airport
  - AirplaneType
  - Airplane
  - Airport
  - Route
  - Crew
  - Flight
  # Account
  - User
  # Cart
  - Order
  - Ticket

## Features
- JWT Authenticated
- Documentation is located in /api/v1/doc/swagger/
- Managing orders and tickets
- CRUD for all entity except User
- filtering with django_filters and query_params

## Installing using GitHub
Install PostgreSQL and create db

```shell
 git clone https://github.com/AntonShpakovych/airport-api-service
 cd airport-api-service
 python -m venv venv
 venv\Scripts\activate
 pip install requirements.txt
 create .env file based on env.sample
 python manage.py migrate
 python manage.py runserver
```
## Run with docker
Docker should be installed
```shell
docker-compose up --build
```

## Gettings access
### Admin for you

Email: admin@gmail.com
Password: admin

- create user api/v1/account/register
- get access token api/v1/account/token
- refresh token api/v1/account/token/refresh
- verify token api/v1/account/token/verify

## Available urls
- api/v1/account/register/
- api/v1/account/token/
- api/v1/account/token/refresh/
- api/v1/account/token/verify/
- api/v1/account/profile/
#
- api/v1/airport/airplane_types/
- api/v1/airport/airplanes/
- api/v1/airport/airports/
- api/v1/airport/routes/
- api/v1/airport/crews/
- api/v1/airport/flights/
#
- api/v1/cart/orders/
## Documantation
- api/v1/doc/
