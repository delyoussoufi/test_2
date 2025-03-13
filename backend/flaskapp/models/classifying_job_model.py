from __future__ import annotations
from contextlib import contextmanager
from datetime import datetime
from enum import Enum
from typing import List

from flask import stream_with_context

from flaskapp import db, app_logger
from flaskapp.http_util.event_message import Message
from flaskapp.models import BaseModel, TableNames


class ClassifyingJobStatus(Enum):
    IDLE = "Waiting"
    RUNNING = "In progress"
    FINISHED = "Done"
    ERROR = "Finished with error"


class ClassifyingJobModel(db.Model, BaseModel):

    __tablename__ = TableNames.T_CLASSIFYING_JOB

    id = db.Column(db.String(50), unique=True, primary_key=True)
    category_id = db.Column(db.String(16), db.ForeignKey(TableNames.T_SEARCH_CATEGORY + ".id"))
    status = db.Column(db.Enum(ClassifyingJobStatus))
    start_time = db.Column(db.DATETIME, default=datetime.now())
    last_update = db.Column(db.DATETIME, default=datetime.now())
    files_processed = db.Column(db.INTEGER, default=0, nullable=False)
    total_files = db.Column(db.INTEGER, nullable=False)

    @classmethod
    def add_job(cls, job_id: str, category_id: str, total_files: int):
        if category_id == "":
            category_id = None
        job_model: cls = cls.get_job(job_id=job_id)
        if job_model:
            if not job_model.is_in_progress():
                # if job is not in progress. reset it
                job_model.reset_job(category_id, total_files)
        else:
            # create a new job if it doesn't exist.
            job_model = cls(id=job_id, category_id=category_id, status=ClassifyingJobStatus.IDLE,
                            total_files=total_files)
            job_model.save()

        return job_model

    @classmethod
    def get_job(cls, job_id: str) -> ClassifyingJobModel:
        return cls.find_by_id(job_id)

    @classmethod
    def get_idles(cls) -> List[ClassifyingJobModel]:
        return cls.find_by_filter(filters=[cls.status == ClassifyingJobStatus.IDLE])

    def update_process(self, files_processed: int):
        self.files_processed = files_processed

        if self.files_processed == self.total_files:
            self.status = ClassifyingJobStatus.FINISHED
        else:
            self.status = ClassifyingJobStatus.RUNNING

        self.last_update = datetime.now()
        self.save()

    def reset_job(self, category_id: str, total_files: int):
        self.status = ClassifyingJobStatus.IDLE
        self.start_time = datetime.now()
        self.last_update = datetime.now()
        self.total_files = total_files
        self.category_id = category_id
        self.files_processed = 0
        self.save()

    def is_in_progress(self):
        return self.status == ClassifyingJobStatus.RUNNING

    @contextmanager
    def start_progress(self):
        self.status = ClassifyingJobStatus.RUNNING
        self.files_processed = 0
        self.start_time = datetime.now()
        try:
            self.save()
            yield self
        except Exception as e:
            self.status = ClassifyingJobStatus.ERROR
            app_logger.error(f"{e}")
        finally:
            if self.status != ClassifyingJobStatus.ERROR:
                self.status = ClassifyingJobStatus.FINISHED
            self.last_update = datetime.now()
            self.save()

    @stream_with_context
    def event_progress(self):
        if self.is_in_progress():
            progress = (self.files_processed/self.total_files)*100. if self.total_files > 0 else 0
            msg = Message(progress, event_type="message", event_id=self.id)
        elif self.status == ClassifyingJobStatus.IDLE:
            msg = Message(0, event_type="message", event_id=self.id)
        else:
            msg = Message(100, event_type="complete", event_id=self.id)
        yield str(msg)
