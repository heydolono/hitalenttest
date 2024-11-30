"""Taskmanager - приложение для создания задач."""

import json
from typing import List, Optional

from validators import (validate_date, validate_non_empty,
                        validate_priority, validate_task_exists)


class Task:
    """Класс, представляющий задачу."""

    def __init__(self, id: int, title: str, description: str, category: str,
                 due_date: str, priority: str, status: str = "Не выполнена"
                 ) -> None:
        """Инициализирует задачу."""
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self) -> dict:
        """Преобразует объект задачи в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Task":
        """Создает объект задачи из словаря."""
        return Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"]
        )


class TaskManager:
    """Класс для управления списком задач."""

    def __init__(self, storage_file: str = "tasks.json") -> None:
        """Инициализирует менеджер задач."""
        self.storage_file = storage_file
        self.tasks: List[Task] = self.load()

    def add(self, title: str, description: str, category: str,
            due_date: str, priority: str) -> None:
        """Добавляет новую задачу в список."""
        task_id = max([task.id for task in self.tasks], default=0) + 1
        new_task = Task(
            task_id, title, description, category, due_date, priority
        )
        self.tasks.append(new_task)
        self.save()
        print(f"Задача '{title}' добавлена")

    def list(self, category: Optional[str] = None) -> None:
        """Отображает список задач."""
        tasks = [
            task for task in self.tasks if not category or
            task.category == category
        ]
        for task in tasks:
            print(f"{task.id}. {task.title} - {task.category} - "
                  f"{task.due_date} - {task.priority} - {task.status}")

    def edit(self, task_id: int, **kwargs) -> None:
        """Редактирует задачу."""
        task = next((t for t in self.tasks if t.id == task_id), None)
        if not task:
            print("Задача не найдена")
            return
        for key, value in kwargs.items():
            if hasattr(task, key) and value:
                setattr(task, key, value)
        self.save()
        print(f"Задача с ID {task_id} обновлена")

    def mark_completed(self, task_id: int) -> None:
        """Отмечает задачу как выполненную."""
        self.edit(task_id, status="Выполнена")

    def delete(self, task_id: Optional[int] = None,
               category: Optional[str] = None) -> None:
        """Удаляет задачу."""
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [
                task for task in self.tasks if task.category != category
            ]
        else:
            print("Укажите ID задачи или категорию для удаления")
            return
        self.save()
        print("Удаление завершено")

    def search(self, keyword: str) -> None:
        """Выполняет поиск по ключевому слову."""
        results = [
            task for task in self.tasks if keyword.lower() in
            task.title.lower() or keyword.lower() in task.description.lower()]
        for task in results:
            print(f"{task.id}. {task.title} - {task.category} - "
                  f"{task.due_date} - {task.priority} - {task.status}")

    def save(self) -> None:
        """Сохраняет список задач в файл."""
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(
                [task.to_dict() for task in self.tasks],
                f, ensure_ascii=False, indent=4)

    def load(self) -> List[Task]:
        """Загружает список задач из файла."""
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(item) for item in data]
        except FileNotFoundError:
            return []


def main() -> None:
    """Основная функция для запуска приложения."""
    manager = TaskManager()
    while True:
        print("\n1. Просмотреть задачи\n2. Добавить задачу\n"
              "3. Изменить задачу\n4. Отметить выполненной\n"
              "5. Удалить задачу\n6. Поиск задачи\n7. Выход")
        numb = input("Выберите действие: ")

        if numb == "1":
            category = input("Введите категорию (оставьте пустым для всех): ")
            manager.list(category)

        elif numb == "2":
            title = validate_non_empty("Название: ")
            description = validate_non_empty("Описание: ")
            category = validate_non_empty("Категория: ")
            due_date = validate_date("Срок выполнения (YYYY-MM-DD): ")
            priority = validate_priority(
                "Приоритет (Низкий/Средний/Высокий): "
            )
            manager.add(title, description, category, due_date, priority)

        elif numb == "3":
            task_id = validate_task_exists(
                manager.tasks, "Введите ID задачи: "
            )
            title = input("Новое название (оставьте пустым для пропуска): ")
            description = input(
                "Новое описание(оставьте пустым для пропуска): "
            )
            category = input(
                "Новая категория(оставьте пустым для пропуска): "
            )
            due_date = input(
                ("Новый срок выполнения (YYYY-MM-DD) "
                 "(оставьте пустым для пропуска): ")
            )
            priority = input(
                ("Новый приоритет (Низкий/Средний/Высокий) "
                 "(оставьте пустым для пропуска): ")
            )
            manager.edit(
                task_id, title=title, description=description,
                category=category, due_date=due_date, priority=priority
            )

        elif numb == "4":
            task_id = validate_task_exists(
                manager.tasks, "Введите ID задачи: "
            )
            manager.mark_completed(task_id)

        elif numb == "5":
            task_id = input(
                "Введите ID (оставьте пустым для удаления по категории): "
            )
            category = input("Введите категорию (если не указан ID): ")
            manager.delete(
                task_id=int(task_id) if task_id else None, category=category
            )

        elif numb == "6":
            keyword = validate_non_empty("Введите ключевое слово: ")
            manager.search(keyword)

        elif numb == "7":

            print("Выход")
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
