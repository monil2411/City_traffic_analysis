import requests

def scrape_traffic_news(location):
    api_key = "24c4f9617752d296350652bc3138d51a"
    url = f"https://gnews.io/api/v4/search?q=traffic+{location}&lang=en&max=5&apikey={api_key}"

    try:
        response = requests.get(url)
        data = response.json()

        articles = []
        for item in data.get("articles", []):
            articles.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "source": item.get("source", {}).get("name")
            })

        return articles

    except Exception as e:
        print(f"Error fetching news: {e}")
        return []
