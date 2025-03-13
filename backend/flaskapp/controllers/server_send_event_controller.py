import flask

from flaskapp.controllers import sse
from flaskapp.http_util.event_message import ProgressEvent
from flaskapp.models.classifying_job_model import ClassifyingJobModel


@sse.route('/progress/<string:progress_id>', methods=["GET"])
def progress(progress_id: str):
    pe = ProgressEvent(progress_id)
    return flask.Response(pe.event_progress(), mimetype="text/event-stream")


@sse.route('/reclassifying_progress/<string:progress_id>', methods=["GET"])
def reclassifying_progress(progress_id: str):
    cj = ClassifyingJobModel.get_job(progress_id)
    return flask.Response(cj.event_progress(), mimetype="text/event-stream")
