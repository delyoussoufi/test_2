from __future__ import annotations

import json
import time

from flask import stream_with_context

PROGRESS_EVENTS: dict[str: ProgressEvent] = {}


class Message:
    """
    Data that is published as a server-sent event.
    """

    def __init__(self, data, event_type=None, event_id: str = None, retry: int = None):
        """
        Create a server-sent event.
        :param data: The event data. If it is not a string, it will be
            serialized to JSON.
        :param event_type: An optional event type. For example: message or complete. This is used by the client side.
        :param event_id: An optional event ID.
        :param retry: An optional integer, to specify the reconnect time for
            disconnected clients of this stream.
        """
        self.data = data if type(data) == str else json.dumps(data)
        self.type = event_type
        self.id = event_id
        self.retry = retry

    def __str__(self):
        """
        Serialize this object to a string, according to the `server-sent events
        specification <https://www.w3.org/TR/eventsource/>`_.
        """
        msgs = [f"data:{self.data}"]
        if self.type:
            msgs.insert(0, f"event:{self.type}")
        if self.id:
            msgs.append(f"id:{self.id}")
        if self.retry:
            msgs.append(f"retry:{self.retry}")
        return "\n".join(msgs) + "\n\n"


class _ProgressMeta(type):

    global PROGRESS_EVENTS

    def __call__(cls, progress_id) -> ProgressEvent:
        # if progress_id id exist return the object otherwise creates a new one.
        obj: cls = PROGRESS_EVENTS.get(progress_id, None)
        if obj:
            return obj
        else:
            return super(_ProgressMeta, cls).__call__(progress_id)


class ProgressEvent(metaclass=_ProgressMeta):

    global PROGRESS_EVENTS

    def __init__(self, progress_id, time_out=2):
        """

        :param progress_id:
        """
        self.progress_id = progress_id
        self.progress = 0
        self.time_out = time_out
        self.completed = False

    def __enter__(self):
        """
        Start a Progress event and add it to the list.

        :return: A progress event object.
        """
        # reset progress.
        self.progress = 0
        self.completed = False
        PROGRESS_EVENTS[self.progress_id] = self
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.completed = True
        self.close()

    def has_event(self):
        return self.progress_id in PROGRESS_EVENTS.keys()

    def close(self):
        if self.progress_id in PROGRESS_EVENTS.keys():
            PROGRESS_EVENTS.pop(self.progress_id, None)

    @stream_with_context
    def event_progress(self):

        msg = Message(self.progress, event_type="message", event_id=self.progress_id)
        time_out = round(self.time_out * 10)
        for i in range(time_out):
            if self.has_event():
                yield str(msg)
                break
            else:
                # Wait a bit for process to start.
                time.sleep(0.1)
        else:
            # if loop is break than assume there is no process with this id to be reported anymore.
            msg = Message(100, event_type="complete", event_id=self.progress_id)
            yield str(msg)
