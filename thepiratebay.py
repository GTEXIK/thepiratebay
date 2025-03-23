import requests

def search_piratebay(query):
    api_url = f"https://apibay.org/q.php?q={query}"
    
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return []

    results = []
    for item in data:
        title = item.get("name", "Без названия")
        magnet_link = f"magnet:?xt=urn:btih:{item['info_hash']}"
        seeders = item.get("seeders", "N/A")

        results.append({
            "title": title,
            "magnet_link": magnet_link,
            "seeders": seeders
        })

    return results

# Пример использования
if __name__ == "__main__":
    while True:
        query = input("ThePirateBay поисковик: ")
        if query.lower() == "exit":
            break
        results = search_piratebay(query)
        if results:
            for result in results:
                print(f"Название: {result['title']}")
                print(f"Magnet: {result['magnet_link']}")
                print(f"Сиды: {result['seeders']}")
                print("-" * 40)
        else:
            print("По вашему запросу ничего не найдено.")
