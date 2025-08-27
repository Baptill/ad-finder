import lbc
import requests
from datetime import datetime
from typing import Final

WEBHOOK_URL: Final[str] = ...

def handle(ad: lbc.Ad, search_name: str) -> None:
    timestamp = datetime.strptime(ad.index_date, "%Y-%m-%d %H:%M:%S").timestamp()
    
    payload = {
        "content": None,
        "embeds": [
            {
                "title": ad.title,
                "description": f"```{ad.body}```",
                "url": ad.url,
                "color": 14381568,
                "author": {
                    "name": ad.user.name,
                    "icon_url": ad.user.profile_picture
                },
                "image": {
                    "url": ad.images[0] if ad.images else None
                },
                "fields": [
                    {
                        "name": "🕒 Publication",
                        "value": f"<t:{int(timestamp)}:R>",
                        "inline": True
                    },
                    {
                        "name": "💰 Price",
                        "value": f"`{ad.price}€`",
                        "inline": True
                    },
                    {
                        "name": "📍 Location",
                        "value": f"`{ad.location.city_label}`",
                        "inline": True
                    }
                ],
            }
        ],
        "username": search_name,
        "attachments": []
    }

    requests.post(WEBHOOK_URL, json=payload)