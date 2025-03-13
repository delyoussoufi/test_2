import os
import traceback
from datetime import datetime, timedelta

from flaskapp import app_utils
from flaskapp.models import ExceptionLogModel


class AdministrationService:

    SUBFOLDER_UPLOAD = os.path.join("Upload", "Master")
    SUBFOLDER_UPLOAD_REPRESENTATION = os.path.join("Upload", "Representation")
    SUBFOLDER_PREPRODUCTION = "PreProduction"
    SUBFOLDER_LIBRARY = "Library"
    STACKTRACE_LENGTH = 5000
    CLEAN_STACKS_AFTER = 30  # days

    @staticmethod
    def log(exception_log: ExceptionLogModel) -> ExceptionLogModel:
        exception_log.stacktrace = (exception_log.stacktrace[:AdministrationService.STACKTRACE_LENGTH] + '...') \
            if len(exception_log.stacktrace) > AdministrationService.STACKTRACE_LENGTH else exception_log.stacktrace
        if not exception_log.id:
            exception_log.id = app_utils.generate_id(16)
        exception_log.save()
        return exception_log

    @staticmethod
    def create_exception_log(exception) -> ExceptionLogModel or None:
        """
            Creates a ExceptionLogModel from the exception, which was thrown.
            Usage:
                try:
                    int('k')
                except Exception as ex:
                    exception_log = AdministrationService.create_exception_log(ex)
            :param exception: exception
            :return: the ExceptionLogModel
        """
        if exception:
            # stacktrace: str = "{}".format(traceback.TracebackException.from_exception(exception))
            stacktrace: str = traceback.format_exc()
            exception_log = ExceptionLogModel()
            exception_log.id = app_utils.generate_id(16)
            exception_log.stacktrace = stacktrace[-5000:]
            exception_log.title = type(exception).__name__
            exception_log.hash = hash(stacktrace)
            exception_log.date = datetime.now()
            return exception_log
        return None

    @classmethod
    def clean_log_model(cls):
        limit_date = datetime.now() - timedelta(days=cls.CLEAN_STACKS_AFTER)
        ExceptionLogModel.bulk_delete(filters=[ExceptionLogModel.date <= limit_date])
