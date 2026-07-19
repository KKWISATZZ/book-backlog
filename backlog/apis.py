import requests


def search_open_library(query):
    response = requests.get(
        "https://openlibrary.org/search.json",
        params={"q": query}
    )
    data = response.json()

    results = []
    for doc in data.get("docs", [])[:20]:
        cover_id = doc.get("cover_i")
        results.append({
            "open_library_id": doc.get("key", ""),
            "title": doc.get("title", "Unknown Title"),
            "author": doc.get("author_name", ["Unknown"])[0],
            "cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None,
            "published_year": doc.get("first_publish_year", 0),
        })
    return results