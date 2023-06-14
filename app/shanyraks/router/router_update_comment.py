from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.patch("/{id}/comments/{comment_id}", status_code=200)
def update_comment(
    id: str,
    comment_id: str,
    comment_content: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    shanyrak = svc.repository.get_shanyrak_by_id(id)
    user_id = jwt_data.user_id

    if user_id != str(shanyrak["user_id"]):
        return Response(status_code=401)

    if shanyrak is None:
        return Response(status_code=404)

    comments = shanyrak.get("comments", [])
    for comment in comments:
        if comment["_id"] == comment_id:
            result = svc.repository.update_comment_by_id(
                id, comment_id, jwt_data.user_id, comment_content
            )

    if result is None:
        return Response(status_code=406)

    if result.modified_count == 0:
        return Response(status_code=401)
    return Response(status_code=200)
