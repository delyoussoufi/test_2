import atexit
from typing import Type

from flask_bcrypt import Bcrypt
import coloredlogs
import logging
import socket

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import ProgrammingError


from flaskapp.config import active_config, Config

db = SQLAlchemy()
bcrypt = Bcrypt()
try:
    cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})  # in new versions
except ImportError:
    cache = Cache(config={'CACHE_TYPE': 'simple'})  # deprecate.

login_manager = LoginManager()
login_manager.session_protection = 'strong'

# jobstores = SQLAlchemyJobStore(url=active_config.SQLALCHEMY_DATABASE_URI, tablename='t_apscheduler_jobs')
# scheduler = BackgroundScheduler(jobstores={'default': jobstores})
scheduler = BackgroundScheduler()

aps_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def clean_jobstores(jobstores):
    try:  # clean all jobs from db before start
        jobstores.remove_all_jobs()
    except ProgrammingError:
        pass


def thread_safe_start_apscheduler(config_class):
    global scheduler
    jobstores = SQLAlchemyJobStore(url=config_class.SQLALCHEMY_DATABASE_URI,
                                   tablename='t_apscheduler_jobs')
    # add a job store
    try:
        scheduler.add_jobstore(jobstores)
    except ValueError:
        print(f"Job store {jobstores} already added.")

    try:
        # bind the socket at localhost and port 47300 to check if it already started.
        aps_socket.bind(("127.0.0.1", 47300))
    except socket.error:
        print("APScheduler already started, DO NOTHING!!!")
        app_logger.info("APScheduler already started, DO NOTHING!!!")
    else:
        from flaskapp.jobs import scheduler_listener

        # Shut down the scheduler when exiting the app and close socket
        atexit.register(lambda *args: scheduler.shutdown(), aps_socket.close())
        # clean jobs at the database
        clean_jobstores(jobstores)
        scheduler.add_listener(scheduler_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
        # scheduler.configure(jobstores={'test': jobstores, 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')})
        # start and add jobs from scheduler_listener to database.
        scheduler.start()
        n_jobs = len(scheduler.get_jobs())
        app_logger.info(f"APScheduler started with {n_jobs} schedule jobs")


def create_logger():
    # create logger.
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    coloredlogs.install(level='DEBUG', logger=logger)

    # create console handler and set level to debug.
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create file handler.
    file_log = logging.FileHandler(filename="app.log")
    file_log.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    file_log.setFormatter(formatter)

    # add ch and file_log to logger
    logger.addHandler(ch)
    logger.addHandler(file_log)

    return logger


def create_app(config_class: Type[Config] = active_config, **kwargs):
    """
    Start create flask app

    :param config_class: Configuration to be used when creating the app
    :param kwargs:
    :keyword run_jobs: If given it will override the value in config_class. Type=bool
    :return:
    """

    # import files where jobs are schedule.
    from flaskapp.jobs import apscheduler_jobs

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Start cache.
    cache.init_app(app)
    # clear cache.
    with app.app_context():
        cache.clear()

    # start db.
    db.init_app(app)

    # set CORS-filter
    # Improved security by allowing only some origins. If a given request needs a bigger scope then we can override
    # the origins behavior with @cross_origin(origins='*') decorator to allow all origins. This decorator is used
    # after a request route api, i.e: @app.route(...)
    # CORS(app,
    #      max_age=600,
    #      origins=[
    #          r"http://localhost:*",
    #      ])
    CORS(app)

    bcrypt.init_app(app)
    login_manager.init_app(app)

    # this must be imported only after flask configuration.
    from flaskapp.controllers import rest as rest_blueprint
    from flaskapp.controllers import admin as admin_blueprint
    from flaskapp.controllers import users as users_blueprint
    from flaskapp.controllers import report as report_blueprint
    from flaskapp.controllers import vorgang as vorgang_blueprint
    from flaskapp.controllers import digitalisat as digitalisat_blueprint
    from flaskapp.controllers import search_category as search_category_blueprint
    from flaskapp.controllers import digi as digi_blueprint
    from flaskapp.controllers import sse as sse_blueprint
    from flaskapp.controllers import public as public_blueprint
    from flaskapp.main.index import main as main_blueprint
    from flaskapp.http_util.exceptions import errors

    # register new APIs here.
    app.register_blueprint(rest_blueprint, url_prefix='/rest')
    app.register_blueprint(admin_blueprint, url_prefix='/rest/admin')
    app.register_blueprint(report_blueprint, url_prefix='/rest/report')
    app.register_blueprint(vorgang_blueprint, url_prefix='/rest/vorgaenge')
    app.register_blueprint(digitalisat_blueprint, url_prefix='/rest/digitalisate')
    app.register_blueprint(search_category_blueprint, url_prefix='/rest/searchCategories')
    app.register_blueprint(users_blueprint, url_prefix='/rest/users')
    app.register_blueprint(digi_blueprint, url_prefix='/rest/digi')
    app.register_blueprint(sse_blueprint, url_prefix='/rest/sse')
    app.register_blueprint(public_blueprint, url_prefix='/rest/public')

    # redirect to Angular build.
    app.register_blueprint(main_blueprint)

    # register error blueprint.
    app.register_blueprint(errors)

    run_job = kwargs.get('run_jobs', config_class.RUN_JOBS)
    if run_job:
        global scheduler
        # Explicitly kick off the background thread
        thread_safe_start_apscheduler(config_class)
        scheduler.app = app

    app_logger.info("Provenance server started.")

    return app


app_logger = create_logger()
