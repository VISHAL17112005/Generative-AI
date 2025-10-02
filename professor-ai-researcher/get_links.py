import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


def get_links(topic):
    topic=topic.replace(" ","+")


    api_key = os.environ.get("SERPER_API_KEY")
    if not api_key:
        raise ValueError("SERPER_API_KEY environment variable not set. Please add it to a .env file as SERPER_API_KEY=your_api_key_here.")

    url = f"https://google.serper.dev/search?q={topic}&apiKey={api_key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    data = json.loads(response.text)
    links = []
    for item in data['organic']:
        links.append(item['link'])
        if "sitelinks" in item:
            for sub in item['sitelinks']:
                print(sub['link'])
    return links

