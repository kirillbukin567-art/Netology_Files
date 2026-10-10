"""Задача №2: автотесты создания папки через Яндекс.Диск REST API.

"""
import os
import uuid

import pytest
import requests

from yandex_disk import BASE_URL, YandexDisk

TOKEN = os.getenv('YANDEX_DISK_TOKEN')
needs_token = pytest.mark.skipif(not TOKEN, reason='не задана переменная окружения YANDEX_DISK_TOKEN')


def unique_name(prefix):
    return f'{prefix}_{uuid.uuid4().hex[:8]}'


@pytest.fixture
def disk():
    return YandexDisk(TOKEN)


@pytest.fixture
def cleanup(disk):
    """Запоминает созданные папки и удаляет их после теста, чтобы не засорять Диск."""
    created = []
    yield created.append
    for path in created:
        disk.delete(path)


# ---------- Положительные тесты ----------

@needs_token
@pytest.mark.parametrize('prefix', ['autotest', 'тестовая папка', 'folder with spaces'])
def test_create_folder_status_code(disk, cleanup, prefix):
    path = unique_name(prefix)
    cleanup(path)
    response = disk.create_folder(path)
    # при успешном создании папки API Диска отвечает 201 Created
    assert response.status_code == 201


@needs_token
@pytest.mark.parametrize('prefix', ['autotest', 'тестовая папка'])
def test_created_folder_appears_in_file_list(disk, cleanup, prefix):
    name = unique_name(prefix)
    cleanup(name)
    assert disk.create_folder(name).status_code == 201
    assert name in disk.list_folder('/')


@needs_token
def test_created_folder_has_type_dir(disk, cleanup):
    name = unique_name('autotest')
    cleanup(name)
    disk.create_folder(name)
    response = disk.get_resource(name)
    assert response.status_code == 200
    assert response.json()['type'] == 'dir'


@needs_token
def test_create_nested_folder(disk, cleanup):
    parent = unique_name('autotest_parent')
    cleanup(parent)
    assert disk.create_folder(parent).status_code == 201
    assert disk.create_folder(f'{parent}/child').status_code == 201
    assert 'child' in disk.list_folder(parent)


# ---------- Отрицательные тесты ----------

@needs_token
def test_create_existing_folder_returns_409(disk, cleanup):
    name = unique_name('autotest')
    cleanup(name)
    assert disk.create_folder(name).status_code == 201
    response = disk.create_folder(name)
    assert response.status_code == 409


@needs_token
def test_create_folder_without_parent_returns_409(disk):
    path = f'{unique_name("no_parent")}/child'
    response = disk.create_folder(path)
    assert response.status_code == 409


@needs_token
def test_failed_creation_does_not_add_folder(disk):
    path = f'{unique_name("no_parent")}/child'
    disk.create_folder(path)
    assert 'child' not in disk.list_folder('/')


@pytest.mark.parametrize('token', ['invalid_token', 'abc123'])
def test_create_folder_with_invalid_token_returns_401(token):
    response = YandexDisk(token).create_folder(unique_name('autotest'))
    assert response.status_code == 401


def test_create_folder_without_authorization_returns_401():
    response = requests.put(BASE_URL, params={'path': unique_name('autotest')}, timeout=15)
    assert response.status_code == 401