import requests

BASE_URL = 'https://cloud-api.yandex.net/v1/disk/resources'


class YandexDisk:
    """Небольшая обёртка над Яндекс.Диск REST API для работы с папками."""

    def __init__(self, token, timeout=15):
        self.headers = {'Authorization': f'OAuth {token}'}
        self.timeout = timeout

    def create_folder(self, path):
        """Создаёт папку. Успех: 201, папка уже есть или нет родителя: 409, плохой токен: 401."""
        return requests.put(BASE_URL, headers=self.headers, params={'path': path}, timeout=self.timeout)

    def get_resource(self, path):
        """Метаданные папки или файла."""
        return requests.get(BASE_URL, headers=self.headers, params={'path': path}, timeout=self.timeout)

    def list_folder(self, path='/', limit=1000):
        """Имена элементов внутри папки, сначала самые новые."""
        response = requests.get(
            BASE_URL,
            headers=self.headers,
            params={'path': path, 'limit': limit, 'sort': '-created'},
            timeout=self.timeout,
        )
        response.raise_for_status()
        return [item['name'] for item in response.json()['_embedded']['items']]

    def delete(self, path):
        """Удаляет папку или файл мимо корзины."""
        return requests.delete(
            BASE_URL,
            headers=self.headers,
            params={'path': path, 'permanently': 'true'},
            timeout=self.timeout,
        )