"""Тесты для task_manager."""

import pytest

from task_manager import TaskManager


@pytest.fixture
def temp_task_manager(tmp_path):
    """Фикстура для менеджера задач."""
    temp_file = tmp_path / "tasks.json"
    manager = TaskManager(storage_file=str(temp_file))
    return manager


def test_add(temp_task_manager):
    """Тест добавления задачи."""
    manager = temp_task_manager
    manager.add("Задача", "Описание", "Работа", "2024-11-30", "Высокий")
    assert len(manager.tasks) == 1
    task = manager.tasks[0]
    assert task.title == "Задача"
    assert task.description == "Описание"
    assert task.category == "Работа"
    assert task.due_date == "2024-11-30"
    assert task.priority == "Высокий"
    assert task.status == "Не выполнена"


def test_list(temp_task_manager, capsys):
    """Тест отображения списка задач."""
    manager = temp_task_manager
    manager.add("Задача 1", "Описание 1", "Работа", "2024-11-30", "Высокий")
    manager.add("Задача 2", "Описание 2", "Дом", "2024-11-30", "Низкий")
    manager.list()
    captured = capsys.readouterr()
    assert "Задача 1" in captured.out
    assert "Задача 2" in captured.out


def test_edit(temp_task_manager):
    """Тест редактирования задачи."""
    manager = temp_task_manager
    manager.add("Задача", "Описание", "Работа", "2024-11-30", "Высокий")
    manager.edit(1, title="Задача 2", category="Дом")
    task = manager.tasks[0]
    assert task.title == "Задача 2"
    assert task.category == "Дом"


def test_mark_completed(temp_task_manager):
    """Тест отметки задачи как выполненной."""
    manager = temp_task_manager
    manager.add("Задача", "Описание", "Работа", "2024-11-30", "Высокий")
    manager.mark_completed(1)
    assert manager.tasks[0].status == "Выполнена"


def test_delete(temp_task_manager):
    """Тест удаления задачи по ID."""
    manager = temp_task_manager
    manager.add("Задача 1", "Описание", "Работа", "2024-11-30", "Высокий")
    manager.add("Задача 2", "Описание", "Дом", "2024-11-30", "Низкий")
    manager.delete(task_id=1)
    assert len(manager.tasks) == 1
    assert manager.tasks[0].title == "Задача 2"


def test_delete_task_category(temp_task_manager):
    """Тест удаления задач по категории."""
    manager = temp_task_manager
    manager.add("Задача 1", "Описание", "Работа", "2024-11-30", "Высокий")
    manager.add("Задача 2", "Описание", "Работа", "2024-11-31", "Низкий")
    manager.add("Задача 3", "Описание", "Дом", "2024-12-01", "Средний")
    manager.delete(category="Работа")
    assert len(manager.tasks) == 1
    assert manager.tasks[0].category == "Дом"


def test_search(temp_task_manager, capsys):
    """Тест поиска задачи по ключевому слову."""
    manager = temp_task_manager
    manager.add("Совещание", "Посовещаться", "Работа", "2024-11-30", "Высокий")
    manager.add("Дорога", "Доехать", "Личное", "2024-11-30", "Средний")
    capsys.readouterr()
    manager.search("Совещание")
    captured = capsys.readouterr()
    assert "Совещание" in captured.out
    assert "Дорога" not in captured.out


def test_save_and_load(temp_task_manager):
    """Тест сохранения и загрузки задач."""
    manager = temp_task_manager
    manager.add("Задача", "Описание", "Работа", "2024-11-30", "Высокий")
    manager.save()
    new_manager = TaskManager(storage_file=manager.storage_file)
    assert len(new_manager.tasks) == 1
    task = new_manager.tasks[0]
    assert task.title == "Задача"
    assert task.description == "Описание"
    assert task.category == "Работа"
    assert task.due_date == "2024-11-30"
    assert task.priority == "Высокий"
    assert task.status == "Не выполнена"
