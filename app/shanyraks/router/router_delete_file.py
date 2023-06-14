from fastapi import Depends, Response
from app.utils import AppModel
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from typing import List

from ..service import Service, get_service
from . import router


class DeleteShanyrakRequest(AppModel):
    media: List[str]


@router.delete("/shanyraks/{id}/media", status_code=200)
def delete_shanyrak(
    id: str,
    input: DeleteShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.delete_shanyrak_media(id, input.media)
    if shanyrak is False:
        return Response(status_code=404)

    return Response(status_code=200)
