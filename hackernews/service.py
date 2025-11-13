from redis import asyncio as aioredis
from bs4 import BeautifulSoup, Tag as SoupTag
from common.schemas import NewsItem
import requests


HACKERNEWS_URL = "https://news.ycombinator.com/"
HACKERNEWS_REDIS_KEY = "hackernews:items"


async def get_top_items(r: aioredis.Redis, limit: int, page: int) -> list[NewsItem]:
    start, end = (page - 1) * limit, page * limit - 1
    redis_data = await r.zrevrange(HACKERNEWS_REDIS_KEY, start, end)
    data = list(map(lambda item: NewsItem.model_validate_json(item), redis_data))
    return data


async def scrap_items(r: aioredis.Redis) -> None:
    res = requests.get(HACKERNEWS_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    submission_elems = soup.select("tr.submission")
    subtext_elems = soup.select("tr td.subtext")

    items = [
        _map_element(submission_elem, subtext_elem)
        for submission_elem, subtext_elem in zip(submission_elems, subtext_elems)
    ]

    for item in items:
        mapped_item, score = await item
        await r.zadd(HACKERNEWS_REDIS_KEY, {mapped_item.model_dump_json(): score})


async def _map_element(submission_elem: SoupTag, subtext_elem: SoupTag) -> tuple[NewsItem, float]:
    item_id = int(submission_elem["id"])
    title = submission_elem.select_one(".title a").text.strip()
    link = submission_elem.select_one(".title a")["href"]

    points = subtext_elem.select_one(".score").text
    points = int(points.split()[0]) if points else 0
    comments = subtext_elem.select(".subline a")[-1].text.strip()
    comments = int(comments.split()[0]) if comments != "discuss" else 0

    score = points + comments * 0.5

    return (NewsItem(id=item_id, title=title, link=link), score)
