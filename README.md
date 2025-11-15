# n2p(news-to-podcast) - api

**n2p(news-to-podcast)** 프로젝트는 최신 기술 뉴스를 HackerNews와 GeekNews에서 수집하여, 이를 요약하고 음성으로 변환하여 팟캐스트 형식으로 제공하는 서비스입니다.

**n2p(news-to-podcast)** project scrapes the latest tech news from HackerNews and GeekNews, summarizes the articles, converts them to speech, and delivers them in podcast format.

![FastAPI Badge](https://img.shields.io/badge/fastapi-standard-blue?logo=fastapi&labelColor=white) ![uv Badge](https://img.shields.io/badge/uv-latest-blue?logo=uv&labelColor=white)

![GitHub Actions: release-build.yml](https://img.shields.io/github/actions/workflow/status/gymynnym/n2p-api/release-build.yml?logo=github&label=release-build.yml) ![GitHub Tag](https://img.shields.io/github/v/tag/gymynnym/n2p-api?logo=github)

## Demo

https://github.com/user-attachments/assets/bc6f2a36-cb1c-442e-b9db-ae9728129166

## Installation

### Using uv: Local Development

```bash
$ git clone git@github.com:gymynnym/n2p-api.git
$ cd n2p-api
$ uv sync
# - activate virtual environment
# - setup environment variables
$ uv run uvicorn main:app
```

### Using Docker

```bash
$ docker pull ghcr.io/gymynnym/n2p-api:latest
$ docker run -d -p 8000:8000 ghcr.io/gymynnym/n2p-api:latest
```

## Environment Variables

| Variable Name| Description   | 
|:--------------|:--------------|
|`CLIENT_HOST`|Client host for setting CORS policy|
|`REDIS_URL`|Redis server URL|
|`OPENAI_API_KEY`|OpenAI API Key|
|`GOOGLE_CLOUD_PROJECT`|Google Cloud Project ID|
|`GOOGLE_APPLICATION_CREDENTIALS`|Path to Google Cloud key file|

## API Documentation

### HackerNews

| Endpoint | Method | Description |
|:---------|:-------|:------------|
|`/hackernews/top`|GET|Get top HackerNews stories|
|`/hackernews/podcasts`|GET|Get generated HackerNews podcasts|
|`/hackernews/podcasts/generate`|POST|Request to generate HackerNews podcasts|


### GeekNews

| Endpoint | Method | Description |
|:---------|:-------|:------------|
|`/geeknews/top`|GET|Get top GeekNews stories|
|`/geeknews/podcasts`|GET|Get generated GeekNews podcasts|
|`/geeknews/podcasts/generate`|POST|Request to generate GeekNews podcasts|

### Podcasts

| Endpoint | Method | Description |
|:---------|:-------|:------------|
|`/podcasts/{filename}.txt`|GET|Get transcript file by filename|
|`/podcasts/{filename}.mp3`|GET|Get podcast file by filename|
|`/podcasts/{filename}`|DELETE|Request to delete podcast by filename|