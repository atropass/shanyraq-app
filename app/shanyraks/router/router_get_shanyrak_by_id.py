from fastapi import Depends, Response
from typing import Any
from app.utils import AppModel

from ..service import Service, get_service
from . import router
from pydantic import Field
from typing import List


class GetMyShanyrakResponse(AppModel):
    id: Any = Field(alias="_id")
    user_id: Any = Field(alias="user_id")
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    media: List[str]
    comments: List[dict[str, Any]]


@router.get("/{id}", response_model=GetMyShanyrakResponse, status_code=200)
def get_shanyrak(
    id: str,
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak_by_id(id)
    if shanyrak is None:
        return Response(status_code=404)

    return GetMyShanyrakResponse(**shanyrak)
