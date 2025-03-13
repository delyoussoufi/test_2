import contextlib

import tzlocal
from apscheduler.events import JobExecutionEvent
from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger

from flaskapp import scheduler
from flaskapp.models.classifying_job_model import ClassifyingJobModel
from flaskapp.services import DigiProcessingService, AdministrationService, DigitalisatService


# cron = second, minute, hour, day, month, day(s) of week. This is the original cron.
# cron_aps = minute, hour, day, month, day(s) of week. The apscheduler version don't use seconds.
# Important. All jobs MUST have the field id, or you will
# get a new copy of the job every time your application restarts!

tz_info = str(tzlocal.get_localzone())


# It's called every time a job finishes execution. If event has an exception the job has fail.
def scheduler_listener(event: JobExecutionEvent):
    if event.exception:
        # msg = f"The job {event.job_id} crashed: Code - {event.code} - MSG - {event.exception}"
        # app_logger.exception(msg=msg)
        e = event.exception
        with scheduler.app.app_context():
            exception_log = AdministrationService.create_exception_log(e)
            exception_log.save()


@contextlib.contextmanager
def pause_and_resume_job(job: Job):
    """
    This will prevent the scheduler from waking up to do job processing until running job is finished.

    :param job: Job to be paused
    :return:
    """
    try:
        job.pause() if job else None
        yield
    finally:
        job.resume() if job else None


# run at 0:00am every day
@scheduler.scheduled_job(id="job_clean_log_model", trigger=CronTrigger.from_crontab('0 0 * * *',  timezone=tz_info),
                         max_instances=1)
def job_clean_log_model():
    with scheduler.app.app_context():
        AdministrationService.clean_log_model()


# run at 1:00am every day
@scheduler.scheduled_job(id="synchronize_digitalisate",
                         trigger=CronTrigger.from_crontab('0 1 * * *',  timezone=tz_info), max_instances=1)
def synchronize_digitalisate():
    with scheduler.app.app_context():
        DigiProcessingService().stream_digitalisat()


@scheduler.scheduled_job(id="stream_images", trigger=CronTrigger.from_crontab('*/5 * * * *',  timezone=tz_info),
                         max_instances=1)
def stream_images():
    # print("Stream images job has started.")
    with scheduler.app.app_context():
        DigiProcessingService().stream_images_from_digi()


@scheduler.scheduled_job(id="get_ocr", trigger=CronTrigger.from_crontab('*/5 * * * *',  timezone=tz_info),
                         max_instances=1)
def get_ocr():
    # print("OCR job has started.")
    with scheduler.app.app_context():
        DigiProcessingService().get_ocr_data()


@scheduler.scheduled_job(id="classify", trigger=CronTrigger.from_crontab('*/5 * * * *',  timezone=tz_info),
                         max_instances=1)
def classify():
    with scheduler.app.app_context():
        DigitalisatService.run_classify()


# run at 18:00 every day
@scheduler.scheduled_job(id="synchronize_scope_data",
                         trigger=CronTrigger.from_crontab('0 18 * * *',  timezone=tz_info), max_instances=1)
def synchronize_scope_data():
    with scheduler.app.app_context():
        DigitalisatService.synchronize_scope_data()


# runs once, one minute after application starts.
@scheduler.scheduled_job(id="reclassify_digitalisate", trigger='interval', seconds=30, max_instances=1)
def reclassify_digitalisate():
    reclassify_digitalisate_job = scheduler.get_job(job_id="reclassify_digitalisate")
    with pause_and_resume_job(reclassify_digitalisate_job):
        with scheduler.app.app_context():
            for classifying_jobs in ClassifyingJobModel.get_idles():
                with classifying_jobs.start_progress() as cj:
                    DigitalisatService.rerun_classification(category_id=cj.category_id, cj=cj)
