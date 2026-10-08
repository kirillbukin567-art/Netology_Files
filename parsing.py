import requests
from bs4 import BeautifulSoup

# Определяем список ключевых слов:
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

BASE_URL = 'https://habr.com'
URL = BASE_URL + '/ru/articles/'  # бывший /ru/all/ — теперь редиректит сюда
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/124.0 Safari/537.36'
    ),
    'Accept-Language': 'ru-RU,ru;q=0.9',
}


def has_keyword(text, keywords):
    """Ищем ключевое слово как подстроку, без учёта регистра."""
    text = text.lower()
    return any(word.lower() in text for word in keywords)


def parse_preview(article):
    """Достаём данные из карточки статьи на странице списка."""
    title_tag = article.select_one('a.tm-title__link')
    if title_tag is None:
        return None

    time_tag = article.select_one('time')
    date = time_tag['datetime'][:10] if time_tag and time_tag.has_attr('datetime') else '—'
    link = BASE_URL + title_tag['href']
    title = title_tag.get_text(strip=True)

    # Вся preview-информация: заголовок, текст превью, хабы, теги
    preview_text = ' '.join(
        part.get_text(' ', strip=True)
        for part in article.select(
            'h2, .article-formatted-body, .tm-article-snippet__hubs, '
            '.tm-article-snippet__labels, .tm-publication-hub__link'
        )
    )
    # запасной вариант, если вёрстка изменилась
    if not preview_text:
        preview_text = article.get_text(' ', strip=True)

    return date, title, link, preview_text


def main():
    response = requests.get(URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = soup.select('article.tm-articles-list__item') or soup.find_all('article')

    found = 0
    for article in articles:
        parsed = parse_preview(article)
        if parsed is None:
            continue
        date, title, link, preview_text = parsed

        if has_keyword(preview_text, KEYWORDS):
            found += 1
            print(f'{date} – {title} – {link}')

    if not found:
        print('Подходящих статей не найдено.')


if __name__ == '__main__':
    main()