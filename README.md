# StockUp API

The Python/Django API for [StockUp Client](https://github.com/KaitlinJKelley/stock-up-client).

![Server](https://img.shields.io/badge/Server%20Side-Python%2FDjango%2C%20Django--safedelete-blue)

## [Use the app](https://stockupclient.herokuapp.com/login)

## Installation
1. Make a copy of the `.env.example` file in the directory and remove the .example extension.
2. Acquire an secret key for Django by running the following command:
`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
3. Insert the resulting secret key into your new `.env` file
4. Run `pipenv shell` from the project directory
5. Seed the database with the command `./seed.sh`. If you get a permissions error, run `sudo ./seed.sh` and enter your machine user password when prompted
6. Run the server with the command `python3 manage.py runserver` (or `python` if you prefer)
7. [Run the Client](https://github.com/KaitlinJKelley/stock-up-client)