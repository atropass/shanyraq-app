from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
import uuid
from ..service import Service, get_service
from . import router
from datetime import datetime


@router.post("/{id}/comments", status_code=200)
def add_comment_to_shanyrak(
    id: str,
    comment_content: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    shanyrak = svc.repository.get_shanyrak_by_id(id)

    if shanyrak is None:
        return Response(status_code=401)

    user_id = jwt_data.user_id

    if user_id != str(shanyrak["user_id"]):
        return Response(status_code=401)
    comment_id = str(uuid.uuid4())
    comment_content = {
        "_id": comment_id,
        "content": comment_content,
        "created_at": datetime.now(),
        "author_id": user_id,
    }
    svc.repository.add_comment_to_shanyrak(id, comment_content)

    return Response(status_code=200)
