import requests
import logging

headers = {
    "User-Agent": "VibeNavigator/0.1"
}

def get_reddit_reviews(city=None, topic=None):
    if not city or not topic:
        logging.warning("City or topic is missing.")
        return []

    search_terms = [f"{topic} in {city}"]
    subreddits = ["india", "travel", "bangalore", "delhi", "mumbai", "restaurants", "coffeeinindia", "FoodPorn"]

    collected = []
    for sub in subreddits:
        for term in search_terms:
            url = f"https://www.reddit.com/r/{sub}/search.json?q={term}&restrict_sr=1&sort=relevance&t=year"
            try:
                res = requests.get(url, headers=headers)
                if res.status_code != 200:
                    continue
                posts = res.json().get("data", {}).get("children", [])
                for post in posts:
                    data = post["data"]
                    if len(data.get("selftext", "")) > 50:
                        collected.append({
                            "text": data["title"] + "\n" + data["selftext"],
                            "url": "https://reddit.com" + data["permalink"]
                        })
            except Exception as e:
                logging.warning(f"Reddit scrape error: {e}")
    return collected
