import os
from contextlib import contextmanager

import pymysql
from flask import current_app, has_app_context


DEFAULTS = {
    "MYSQL_HOST": "127.0.0.1",
    "MYSQL_PORT": 3306,
    "MYSQL_USER": "root",
    "MYSQL_PASSWORD": "",
    "MYSQL_DATABASE": "pet_care",
}


def _setting(name):
    if has_app_context() and name in current_app.config:
        return current_app.config[name]

    value = os.environ.get(name)
    if value is not None:
        return value

    return DEFAULTS[name]


def _connection_params(include_database=True):
    params = {
        "host": _setting("MYSQL_HOST"),
        "port": int(_setting("MYSQL_PORT")),
        "user": _setting("MYSQL_USER"),
        "password": _setting("MYSQL_PASSWORD"),
        "charset": "utf8mb4",
        "cursorclass": pymysql.cursors.DictCursor,
        "autocommit": False,
    }

    if include_database:
        params["database"] = _setting("MYSQL_DATABASE")

    return params


def get_connection():
    return pymysql.connect(**_connection_params())


@contextmanager
def connection_scope():
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


def ensure_schema():
    database_name = _setting("MYSQL_DATABASE")

    server_connection = pymysql.connect(
        host=_setting("MYSQL_HOST"),
        port=int(_setting("MYSQL_PORT")),
        user=_setting("MYSQL_USER"),
        password=_setting("MYSQL_PASSWORD"),
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )

    try:
        with server_connection.cursor() as cursor:
            cursor.execute(
                f"""
                CREATE DATABASE IF NOT EXISTS `{database_name}`
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci
                """
            )
    finally:
        server_connection.close()

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(120) NOT NULL,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(160) NOT NULL,
                    category VARCHAR(120) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL,
                    quantity INT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """
            )
        connection.commit()
    finally:
        connection.close()