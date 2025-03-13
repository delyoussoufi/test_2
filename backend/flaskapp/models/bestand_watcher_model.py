import contextlib
from datetime import datetime
from enum import Enum

from flaskapp import db
from flaskapp.models import BaseModel, TableNames
from flaskapp.utils import DateUtils


class BestandStatus(Enum):
    IDLE = 'Warten'
    RUNNING = 'In Bearbeitung'
    PAUSED = 'Angehalten'


class BestandWatcherModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_BESTAND_WATCHER

    id = db.Column(db.String(16), primary_key=True)
    name = db.Column(db.String(400))
    status = db.Column(db.Enum(BestandStatus), default=BestandStatus.IDLE)
    last_synchronization = db.Column(db.DateTime())

    def to_dict(self):
        dto = super().to_dict()
        bestand_status: BestandStatus = dto.get("status")
        dto["statusInfo"] = bestand_status.value
        dto["status"] = bestand_status.name
        dto["lastSynchronization"] = DateUtils.convert_date_to_german_string(self.last_synchronization, add_time=True)
        return dto

    def __repr__(self):
        atr = (f"{key}={value}" for key, value in self.to_dict().items())
        return f"{type(self).__name__}({', '.join(atr)})"

    def pause(self) -> bool:
        if self.status != BestandStatus.RUNNING:
            self.status = BestandStatus.PAUSED
            return self.save()
        return False

    def unpause(self) -> bool:
        if self.status != BestandStatus.RUNNING:
            self.status = BestandStatus.IDLE
            return self.save()
        return True

    def is_paused(self) -> bool:
        return self.status == BestandStatus.PAUSED

    def is_idle(self) -> bool:
        return self.status == BestandStatus.IDLE

    def is_running(self) -> bool:
        return self.status == BestandStatus.RUNNING

    @contextlib.contextmanager
    def status_with_context(self):
        try:
            self.status = BestandStatus.RUNNING
            self.save()
            yield
        finally:
            self.status = BestandStatus.IDLE
            self.last_synchronization = datetime.now()
            self.save()

    @classmethod
    def add_bestand(cls, bestand: dict):
        """
        Add the bestand from digi product to be watch. If bestand already exists do nothing.

        :param bestand: A dictionary representation from digiproduction.
        :return: True if added, false otherwise.
        """
        bestand_id = bestand["id"]
        bestand_name = bestand["name"]
        if cls.find_by_id(bestand_id):
            return True

        bestand_model = cls()
        bestand_model.id = bestand_id
        bestand_model.name = bestand_name
        return bestand_model.save()
