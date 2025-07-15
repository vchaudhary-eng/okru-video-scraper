import requests
import re
from datetime import datetime, timedelta

def scrape_okru(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text

        # Title
        title = re.search(r'<meta property="og:title" content="(.*?)"', html, re.I)
        title_value = title.group(1) if title else "N/A"

        # Duration
        duration = re.search(r'class="vid-card_duration">([\d:]+)</div>', html, re.I)
        duration_in_seconds = "N/A"
        if duration:
            time_parts = list(map(int, duration.group(1).split(":")))
            if len(time_parts) == 3:
                duration_in_seconds = time_parts[0]*3600 + time_parts[1]*60 + time_parts[2]
            elif len(time_parts) == 2:
                duration_in_seconds = time_parts[0]*60 + time_parts[1]
            elif len(time_parts) == 1:
                duration_in_seconds = time_parts[0]

        # Upload Date
        upload_date = "N/A"
        upload_date_match = re.search(r'<span class="vp-layer-info_i vp-layer-info_date">([^<]+)</span>', html, re.I)
        current_year = datetime.now().year
        if upload_date_match:
            date_text = upload_date_match.group(1).strip().lower()
            if "вчера" in date_text:
                yesterday = datetime.now() - timedelta(days=1)
                time_part = date_text.split(" ")[1] if " " in date_text else "00:00"
                upload_date = f"{yesterday.day:02d}-{yesterday.month:02d}-{current_year} {time_part}"
            else:
                time_parts = date_text.split(" ")
                if len(time_parts) == 2:
                    date_parts = time_parts[0].split("-")
                    day = date_parts[0] if len(date_parts) > 0 else "01"
                    month = date_parts[1] if len(date_parts) > 1 else "01"
                    time = time_parts[1]
                    upload_date = f"{day.zfill(2)}-{month.zfill(2)}-{current_year} {time}"

        # Views
        views = re.search(r'<div class="vp-layer-info_i"><span>(.*?)</span>', html, re.I)
        views_value = views.group(1) if views else "N/A"

        # Channel URL
        channel_url_match = re.search(r'/(group|profile)/([\w\d]+)', html, re.I)
        channel_url = f"https://ok.ru/{channel_url_match.group(1)}/{channel_url_match.group(2)}" if channel_url_match else "N/A"

        # Channel Name
        channel_name = re.search(r'name="([^"]+)" id="[\d]+"', html, re.I)
        channel_name_value = channel_name.group(1) if channel_name else "N/A"

        # Subscribers
        subscribers = re.search(r'subscriberscount="(\d+)"', html, re.I)
        subscribers_value = int(subscribers.group(1)) if subscribers else "N/A"

        return {
            "title": title_value,
            "duration_seconds": duration_in_seconds,
            "views": views_value,
            "upload_date": upload_date,
            "channel_url": channel_url,
            "channel_name": channel_name_value,
            "subscribers": subscribers_value,
            "status": "Success"
        }

    except Exception as e:
        return {
            "error": str(e),
            "status": "Error"
        }