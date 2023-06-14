from datetime import datetime

from bson.objectid import ObjectId
from pymongo.database import Database
from typing import List


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, input: dict):
        payload = {
            "user_id": ObjectId(input["user_id"]),
            "type": input["type"],
            "price": input["price"],
            "address": input["address"],
            "area": input["area"],
            "rooms_count": input["rooms_count"],
            "description": input["description"],
            "created_at": datetime.utcnow(),
        }

        result = self.database["shanyraks"].insert_one(payload)

        return str(result.inserted_id)

    def get_shanyrak_by_id(self, id: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        return shanyrak

    def update_shanyrak_by_id(self, id: str, user_id: str, data: dict) -> bool:
        found = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
                "user_id": ObjectId(user_id),
            }
        )

        if found is None:
            return False

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$set": {
                    "type": data["type"],
                    "price": data["price"],
                    "address": data["address"],
                    "area": data["area"],
                    "rooms_count": data["rooms_count"],
                    "description": data["description"],
                }
            },
        )

        return result.modified_count == 1

    def delete_shanyrak_by_id(self, id: str, user_id: str) -> bool:
        found = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
                "user_id": ObjectId(user_id),
            }
        )

        if found is None:
            return False

        result = self.database["shanyraks"].delete_one(
            filter={"_id": ObjectId(id)},
        )

        return result.deleted_count == 1

    def add_shanyrak_media(self, id: str, media: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if shanyrak is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "media": media,
                }
            },
        )

        return result

    def delete_shanyrak_media(self, id: str, media: List[str]):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if shanyrak is None:
            return None
        for m in media:
            result = self.database["shanyraks"].update_one(
                filter={"_id": ObjectId(id)},
                update={"$pull": {"media": m}},
            )

        return result

    def add_comment_to_shanyrak(self, id: str, comment_content: str) -> dict | None:
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )
        if shanyrak is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$push": {
                    "comments": comment_content,
                }
            },
        )

        return result

    def update_comment_by_id(
        self, id: str, comment_id: str, user_id: str, content: str
    ):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(id),
            }
        )

        if shanyrak is None:
            return None

        if shanyrak["comments"] is None:
            return None

        result = self.database["shanyraks"].update_one(
            filter={
                "_id": ObjectId(id),
                "comments.id": ObjectId(comment_id),
                "comments.author_id": ObjectId(user_id),
            },
            update={
                "$set": {
                    "comments.$.content": content,
                }
            },
        )

        return result
