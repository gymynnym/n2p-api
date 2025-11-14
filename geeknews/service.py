from redis import asyncio as aioredis
from bs4 import BeautifulSoup, Tag as SoupTag
from common.schemas import NewsItem
import requests
import re


GEEKNEWS_URL = "https://news.hada.io/"
GEEKNEWS_ITEMS_KEY = "geeknews:items"
GEEKNEWS_PODCASTS_KEY = "geeknews:podcasts"


async def get_top_items(r: aioredis.Redis, limit: int, page: int) -> list[NewsItem]:
    start, end = (page - 1) * limit, page * limit - 1
    redis_data = await r.zrevrange(GEEKNEWS_ITEMS_KEY, start, end)
    data = list(map(lambda item: NewsItem.model_validate_json(item), redis_data))
    return data


async def get_top_item_urls(r: aioredis.Redis, limit: int) -> list[str]:
    items = await get_top_items(r, limit, 1)
    return [item.url for item in items]


async def get_podcasts(
    r: aioredis.Redis,
    limit: int,
    page: int,
) -> list[str]:
    start, end = (page - 1) * limit, page * limit - 1
    redis_data = await r.zrevrange(GEEKNEWS_PODCASTS_KEY, start, end)
    return [podcast for podcast in redis_data]


async def scrap_items(r: aioredis.Redis) -> None:
    res = requests.get(GEEKNEWS_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    topic_elems = soup.select(".topics .topic_row")

    items = [_map_element(topic_elem) for topic_elem in topic_elems]

    await r.delete(GEEKNEWS_ITEMS_KEY)
    for item in items:
        mapped_item, score = await item
        await r.zadd(GEEKNEWS_ITEMS_KEY, {mapped_item.model_dump_json(): score})


async def _map_element(topic_elem: SoupTag) -> tuple[NewsItem, float]:
    item_id = topic_elem.select_one(".vote > span")["id"][4:]  # remove 'vote' prefix
    item_id = int(item_id)
    title = topic_elem.select_one("h1").text.strip()
    url = topic_elem.select_one(".topictitle a")["href"]

    points = topic_elem.select(".topicinfo span")[0].text
    points = int(points) if points else 0
    comments = topic_elem.select(".topicinfo a")[-1].text.strip()
    comments = re.search(r"(\d+)", comments)
    comments = int(comments.group(1)) if comments else 0

    score = points + comments * 0.5

    return (NewsItem(id=item_id, title=title, url=url), score)
