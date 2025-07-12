from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging
import json
import re

from reddit_scraper import get_reddit_reviews

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_tags_and_emojis(text):
    tags = []
    emojis = ""

    if "quiet" in text.lower():
        tags.append("quiet")
        emojis += "🤫"
    if "lively" in text.lower():
        tags.append("lively")
        emojis += "🎉"
    if "nature" in text.lower():
        tags.append("nature-filled")
        emojis += "🌿"
    if "coffee" in text.lower() or "cafe" in text.lower():
        tags.append("cozy")
        emojis += "☕"

    return tags or ["relaxed"], emojis or "🌟"

def query_ollama(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma:2b", "prompt": prompt.strip()},
            timeout=60
        )
        response.raise_for_status()

        lines = response.text.strip().splitlines()
        final_output = ""
        for line in lines:
            try:
                data = json.loads(line)
                if "response" in data:
                    final_output += data["response"]
            except json.JSONDecodeError:
                continue

        return final_output.strip() or "Sorry, I couldn't generate a summary right now."

    except Exception as e:
        logging.error(f"Ollama error: {e}")
        return "Sorry, I couldn't generate a summary right now."

def clean_summary_and_extract_places(text):
    # Strip markdown formatting like ** and ##
    cleaned_text = re.sub(r'[*#]+', '', text)

    # Extract numbered places
    places = re.findall(r'\d+\.\s+(.*)', cleaned_text)
    summary = re.split(r'\d+\.\s+', cleaned_text)[0].strip()

    return summary, places

@app.get("/summarize")
def summarize(
    city: str = Query(None),
    category: str = Query(None),
    preference: str = Query(None),
    query: str = Query(None)
):
    if query:
        prompt = f"""
You're a city vibe expert and local guide assistant. Based on the natural language user request below, summarize the vibe in a friendly tone and list at least 3 relevant places (cafes, restaurants, attractions) if mentioned. Format the output cleanly using paragraphs and a numbered list for places. Avoid using markdown (like ## or **).

Request: {query}

Your response should include:
1. A 1–2 paragraph vibe summary.
2. A numbered list of specific places mentioned (if any).
"""
        citations = []
    else:
        reviews = get_reddit_reviews(city, category)
        valid_reviews = [r for r in reviews if r.get("text") and r.get("url")]
        citations = [r["url"] for r in valid_reviews]

        if valid_reviews:
            review_texts = [r["text"].strip() for r in valid_reviews]
            review_text = "\n\n".join(review_texts[:5])

            prompt = f"""
You're a city expert and recommendation engine. Based on these Reddit reviews about {category}s in {city} for someone who prefers {preference}, give a vibe-based summary AND list at least 3 popular {category} names if they appear in the reviews.

Format your response like this:
1. Vibe summary (1–2 paragraphs)
2. A cleanly formatted numbered list of places (no markdown like ** or ##)

Reviews:
{review_text}
"""
        else:
            prompt = f"""
You're a city expert and travel assistant. Suggest the vibe and at least 3 {category}s in {city} for someone who prefers a '{preference}' experience.

Format:
1. (1–2 paragraphs)
2. Numbered list of recommended {category}s in {city} that match '{preference}' vibe
"""

    raw_summary = query_ollama(prompt)
    summary, places = clean_summary_and_extract_places(raw_summary)
    tags, emojis = generate_tags_and_emojis(summary)

    return {
        "vibe": summary,
        "places": places,
        "tags": tags,
        "emojis": emojis,
        "citations": citations
    }
