from redis import asyncio as aioredis
from bs4 import BeautifulSoup, Tag as SoupTag
from common.schemas import NewsItem
import requests


HACKERNEWS_URL = "https://news.ycombinator.com/"
HACKERNEWS_ITEMS_KEY = "hackernews:items"
HACKERNEWS_PODCASTS_KEY = "hackernews:podcasts"


async def get_top_items(r: aioredis.Redis, limit: int, page: int) -> list[NewsItem]:
    start, end = (page - 1) * limit, page * limit - 1
    redis_data = await r.zrevrange(HACKERNEWS_ITEMS_KEY, start, end)
    items = list(map(lambda item: NewsItem.model_validate_json(item), redis_data))
    return items


async def get_top_item_urls(r: aioredis.Redis, limit: int) -> list[str]:
    items = await get_top_items(r, limit, 1)
    return [item.url for item in items]


async def get_podcasts(
    r: aioredis.Redis,
    limit: int,
    page: int,
) -> list[str]:
    start, end = (page - 1) * limit, page * limit - 1
    redis_data = await r.zrevrange(HACKERNEWS_PODCASTS_KEY, start, end)
    return [podcast for podcast in redis_data]


async def scrap_items(r: aioredis.Redis) -> None:
    res = requests.get(HACKERNEWS_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    submission_elems = soup.select("tr.submission")
    subtext_elems = soup.select("tr td.subtext")

    items = [
        _map_element(submission_elem, subtext_elem)
        for submission_elem, subtext_elem in zip(submission_elems, subtext_elems)
    ]

    await r.delete(HACKERNEWS_ITEMS_KEY)
    for item in items:
        mapped_item, score = await item
        await r.zadd(HACKERNEWS_ITEMS_KEY, {mapped_item.model_dump_json(): score})


async def _map_element(submission_elem: SoupTag, subtext_elem: SoupTag) -> tuple[NewsItem, float]:
    item_id = int(submission_elem["id"])
    title = submission_elem.select_one(".title a").text.strip()
    url = submission_elem.select_one(".title a")["href"]

    points = subtext_elem.select_one(".score")
    points = int(points.text.strip().split()[0]) if points else 0
    comments = subtext_elem.select(".subline a")
    comments = comments[-1].text.strip() if len(comments) > 0 else ""
    comments = int(comments.split()[0]) if comments not in ["", "discuss"] else 0

    score = points + comments * 0.5

    return (NewsItem(id=item_id, title=title, url=url), score)
