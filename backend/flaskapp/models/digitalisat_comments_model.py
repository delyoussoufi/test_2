from __future__ import annotations

from datetime import datetime
from typing import Optional

from flaskapp import db, app_utils
from flaskapp.http_util.exceptions import AppException
from flaskapp.models import BaseModel, TableNames


class DigitalisatCommentsModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_DIGITALISAT_COMMENTS

    id = db.Column(db.String(16), primary_key=True)
    digitalisat_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT + ".id"))
    user_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_USER + ".user_id"))
    # weak reference to either search category, vorgang or pdf creation.
    reference = db.Column(db.String(100), default="Unknown")
    comment = db.Column(db.String())
    post_date = db.Column(db.Date(), default=datetime.now)
    # link comments ids as part of reply.
    comment_link_id = db.Column(db.String(16))

    def __repr__(self):
        atr = [f"{c.name}={getattr(self, c.name)}" for c in DigitalisatCommentsModel.__table__.columns]
        return f"{type(self).__name__}({', '.join(atr)})"

    def to_dict(self):
        from flaskapp.models import UserModel
        dto = dict()
        dto["id"] = self.id
        dto["digitalisatId"] = self.digitalisat_id
        dto["userId"] = self.user_id
        user: UserModel = self.user  # backref
        dto["userName"] = user.username if user else "anonym"
        dto["reference"] = self.reference
        dto["comment"] = self.comment
        dto["postDate"] = self.post_date.strftime('%m.%d.%Y %H:%M:%S')
        dto["commentLinkId"] = self.comment_link_id
        dto["replies"] = [e.to_dict() for e in self.get_reply_comments()]

        return dto

    @classmethod
    def from_dict(cls, dto: dict):
        model: cls = super().from_dict(dto)
        model.digitalisat_id = dto.get("digitalisatId")
        model.user_id = dto.get("userId", None)
        model.comment_link_id = dto.get("commentLinkId", None)

        return model

    @classmethod
    def create_post(cls, comment, digitalisat_id, user_id: Optional[str] = None, reference: Optional[str] = None,
                    comment_link_id: Optional[str] = None):
        model = cls()
        model.id = app_utils.generate_id(16)
        model.comment = comment
        model.digitalisat_id = digitalisat_id
        model.reference = reference
        model.user_id = user_id
        model.comment_link_id = comment_link_id
        return model

    @classmethod
    def update_comment(cls, comment_id: str, comment: str):
        model: cls = cls.find_by_id(comment_id)
        if model:
            model.comment = comment
            return model.save()
        raise AppException(f"Comment id: {comment_id} doesn't exits.")

    @classmethod
    def get_comments_from_digitalisat(cls, digitalisat_id: str):
        return cls.find_by_filter(filters=[cls.digitalisat_id == digitalisat_id, cls.comment_link_id.__eq__(None)],
                                  order_by=cls.post_date.desc())

    def get_reply_comments(self):
        return DigitalisatCommentsModel.find_by_filter(
            filters=[DigitalisatCommentsModel.comment_link_id == self.id],
            order_by=DigitalisatCommentsModel.post_date.asc()
        )

    def delete(self):
        deleted_child = DigitalisatCommentsModel.bulk_delete(
            filters=[DigitalisatCommentsModel.comment_link_id == self.id]
        )
        deleted_self = super().delete()
        return deleted_child and deleted_self


