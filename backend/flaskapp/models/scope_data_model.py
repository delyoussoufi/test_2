from sqlalchemy import func
from sqlalchemy.ext.hybrid import hybrid_property

from flaskapp import db, app_utils, active_config
from flaskapp.models import BaseModel, TableNames
from flaskapp.utils import DateUtils, TSVectorType


class ScopeDataModel(db.Model, BaseModel):

    LANGUAGE = 'simple'
    __tablename__ = TableNames.T_SCOPE_DATA

    id = db.Column(db.String(16), primary_key=True)
    digitalisat_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_DIGITALISAT + ".id"))
    title = db.Column(db.String(400))
    geburtsname = db.Column(db.String(40))
    dat_findbuch = db.Column(db.String(40))
    geburtsdatum = db.Column(db.Date())
    geburtsort = db.Column(db.String(40))
    wohnort = db.Column(db.String(400))
    registry_signature = db.Column(db.String(200))
    associates = db.Column(db.String(2000))

    @hybrid_property
    def title_vector(self):
        return self.title

    @hybrid_property
    def associates_vector(self):
        return self.associates

    # noinspection PyMethodParameters
    @title_vector.expression
    def title_vector(cls) -> TSVectorType:
        return func.to_tsvector(cls.LANGUAGE, func.coalesce(cls.title, ""))

    # noinspection PyMethodParameters
    @associates_vector.expression
    def associates_vector(cls) -> TSVectorType:
        return func.to_tsvector(cls.LANGUAGE, func.coalesce(cls.associates, ""))

    @property
    def link(self) -> str:
        return f"{active_config.SCOPE_DETAIL_VIEW_URL}{self.digitalisat.scope_id}"

    def to_dict(self):
        dto = super().to_dict()
        dto["digitalisatId"] = dto.pop('digitalisat_id')
        dto["datFindbuch"] = dto.pop('dat_findbuch', '')
        dto["geburtsdatum"] = DateUtils.convert_date_to_german_string(self.geburtsdatum)
        dto["registrySignature"] = dto.pop('registry_signature', '')
        dto["link"] = self.link
        return dto

    def __repr__(self):
        atr = (f"{key}={value}" for key, value in self.to_dict().items())
        return f"{type(self).__name__}({', '.join(atr)})"

    @classmethod
    def from_digitalisat_scope_info(cls, dsi):
        """
        Convert a DigitalisatScopeInfo object to this model. Also creates a new id for it.
        Before save this model you must link it to a digitalisat.

        :param dsi: A DigitalisatScopeInfo object.
        :return: A new ScopeDataModel
        """
        dto = dsi.to_dict()
        entity = cls.from_dict(dto)
        entity.id = app_utils.generate_id(16)
        return entity

    def map_values_from_digitalisat_scope_info(self, dsi):
        """
        Convert a DigitalisatScopeInfo object to this model. Then update its values.

        You must save the entity after update it.

        :param dsi: A DigitalisatScopeInfo object.
        :return:
        """
        dto = dsi.to_dict()
        new_scope_model = ScopeDataModel.from_dict(dto)
        # keep fields that are not related to scope data.
        new_scope_model.id = self.id
        new_scope_model.digitalisat_id = self.digitalisat_id
        # dump scope data values to and existing model.
        self << new_scope_model
        return self
