from sqlalchemy import or_

from flaskapp import db
from flaskapp.models import TableNames, BaseModel


class ApplicationParamModel(db.Model, BaseModel):
    __tablename__ = TableNames.T_APPLICATION_PARAM

    APP_URL_ID = "appUrl"
    USER_SERVICE_MAIL_ID = "userServiceMail"

    param_id = db.Column(db.String(50), primary_key=True)
    label = db.Column(db.String(50))
    param_value = db.Column(db.String(200))

    @classmethod
    def from_dict(cls, dto: dict):
        application_param_model = ApplicationParamModel()
        application_param_model.param_id = dto.get("id", None)
        application_param_model.label = dto.get("label", None)
        application_param_model.param_value = dto.get("value", None)
        return application_param_model

    def to_dict(self):
        return {"id": self.param_id, "label": self.label, "value": self.param_value}

    @classmethod
    def get_scope_elements(cls):
        from flaskapp.services.scope_service import DigitalisatScopeInfo

        filters = [cls.param_id == scope_element for scope_element in DigitalisatScopeInfo.SCOPE_ELEMENTS]
        return cls.find_by_filter(filters=filters, use_or=True)
