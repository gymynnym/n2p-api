from fastapi import APIRouter
from fastapi.responses import FileResponse
from common.schemas import ResponseModel
from starlette import status
from podcast import service as podcast_service


router = APIRouter(prefix="/podcasts", tags=["Podcasts"])


@router.get("/{filename}.txt", response_model=ResponseModel[str], status_code=status.HTTP_200_OK)
async def get_podcast_text(filename: str):
    filepath = await podcast_service.get_podcast_filepath(f"{filename}.txt")
    return FileResponse(
        path=filepath,
        filename=f"{filename}.txt",
        media_type="application/octet-stream",
    )


@router.get("/{filename}.mp3", status_code=status.HTTP_200_OK)
async def get_podcast_audio(filename: str):
    filepath = await podcast_service.get_podcast_filepath(f"{filename}.mp3")
    return FileResponse(
        path=filepath,
        filename=f"{filename}.mp3",
        media_type="application/octet-stream",
    )
