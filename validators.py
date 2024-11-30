"""Валидаторы taskmanager."""
from datetime import datetime


def validate_non_empty(prompt: str) -> str:
    """Проверяет, что поле не пустое."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Поле не может быть пустым")


def validate_date(prompt: str) -> str:
    """Проверяет, что дата в формате YYYY-MM-DD."""
    while True:
        date_str = input(prompt).strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Дата должна быть в формате YYYY-MM-DD и не быть пустым")


def validate_priority(prompt: str) -> str:
    """Проверяет, что приоритетом является:('Низкий', 'Средний', 'Высокий')."""
    valid_text = ['Низкий', 'Средний', 'Высокий']
    while True:
        priority = input(prompt).strip()
        if priority in valid_text:
            return priority
        print("Приоритет должен быть 'Низкий', 'Средний' или 'Высокий'")


def validate_integer(prompt: str) -> int:
    """Проверяет, что значение является числом."""
    while True:
        try:
            value = int(input(prompt).strip())
            return value
        except ValueError:
            print("Введите число")


def validate_task_exists(tasks, prompt: str) -> int:
    """Проверяет, что значение является числом и что задача существует."""
    while True:
        task_id = validate_non_empty(prompt)
        try:
            task_id = int(task_id)
        except ValueError:
            print("Пожалуйста, введите целое число")
            continue
        if task_id <= len(tasks) and task_id > 0:
            return task_id
        print(f"Задачи с ID {task_id} не существует.")
