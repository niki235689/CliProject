"""Модуль для обработки аргументов командной строки."""
import argparse
import sys


def parse_args() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.
    Возвращает объект с параметрами.
    """
    parser = argparse.ArgumentParser(description="Граф зависимостей Cargo")
    parser.add_argument("--pkg", required=True, help="Имя пакета")
    parser.add_argument("--url", required=True, help="URL или путь к файлу")
    parser.add_argument("--test", action="store_true", help="Тестовый режим")
    parser.add_argument("--ver", required=True, help="Версия пакета")
    parser.add_argument("--out", required=True, help="Имя файла PNG")
    parser.add_argument("--ascii", action="store_true", help="ASCII дерево")

    try:
        args = parser.parse_args()
        return args
    except SystemExit:
        print("Ошибка: неверно заданы аргументы командной строки.")
        sys.exit(1)