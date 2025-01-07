import requests
from bs4 import BeautifulSoup

def search_piratebay(query):
    base_url = "https://thepiratebay0.org/search/"
    search_url = f"{base_url}{query}/1/99/0"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    for row in soup.select('tr:has(a.detLink)'):
        title_tag = row.select_one('a.detLink')
        magnet_tag = row.select_one('a[href^="magnet:"]')
        if title_tag and magnet_tag:
            title = title_tag.text
            link = title_tag['href']
            magnet_link = magnet_tag['href']
            seeders_tag = row.select('td')[-2]
            seeders = seeders_tag.text if seeders_tag else 'N/A'
            results.append({
                'title': title,
                'link': f"https://thepiratebay0.org{link}",
                'magnet_link': magnet_link,
                'seeders': seeders
            })

    if not results:
        print("Ничего не найдено или структура сайта изменилась.")

    return results

# Пример использования
if __name__ == "__main__":
    while True:
        query = input("ThePirateBay поисковик: ")
        if query.lower() == 'exit':
            break
        results = search_piratebay(query)
        if results:
            for result in results:
                print(f"Название: {result['title']}")
                print(f"Ссылка: {result['link']}")
                print(f"Magnet: {result['magnet_link']}")
                print("-" * 40)
        else:
            print("По вашему запросу ничего не найдено.")
