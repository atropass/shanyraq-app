from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.get("/{id}/comments", status_code=200)
def get_shanyrak_comments(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict:
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if shanyrak is None:
        return Response(status_code=404)

    comments = shanyrak.get("comments", [])

    return {"comments": comments}
