from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DB
from flask import flash
from flask_app.models import user_model


class Keycard:
    def __init__(self, data):
        self.id = data["id"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.day_shift = data["day_shift"]
        self.evening_shift = data["evening_shift"]
        self.graveyard_shift = data["graveyard_shift"]
        self.swing_shift = data["swing_shift"]
        self.price = data["price"]
        self.keycard_id = data["keycard_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def create(cls, data):
        query = """INSERT INTO keycards (start_time, end_time, day_shift, evening_shift, graveyard_shift, swing_shift, price, keycard_id, user_id)
                    VALUES ( %(start_time)s, %(end_time)s, %(day_shift)s, %(evening_shift)s, %(graveyard_shift)s, %(swing_shift)s, %(price)s, %(keycard_id)s, %(user_id)s );"""
        results = connectToMySQL(DB).query_db(query, data)
        return results

    @classmethod
    def get_keycards_with_users(cls):
        query = (
            """SELECT * FROM keycards LEFT JOIN users ON keycards.user_id = users.id;"""
        )
        results = connectToMySQL(DB).query_db(query)
        all_keycards = []
        for row_from_db in results:
            keycard_instance = cls(row_from_db)
            user_data = {
                **row_from_db,
                "id": row_from_db["users.id"],
                "created_at": row_from_db["users.created_at"],
                "updated_at": row_from_db["users.updated_at"],
            }
            user_instance = user_model.User(user_data)
            keycard_instance.data = user_instance
            all_keycards.append(keycard_instance)
        return all_keycards
