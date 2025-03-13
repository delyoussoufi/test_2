import configparser
import os

from resources.sql import sql_path


def read_ofp_config():
    config_file = os.path.join(os.path.dirname(__file__), "ofp.ini")
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


class Config:
    __ofp_config = read_ofp_config()

    MAIL_SMTP_HOST = __ofp_config['MAIL']['MAIL_SMTP_HOST']
    SQLALCHEMY_DATABASE_URI = __ofp_config['DATABASE']['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    USE_SCOPE_TEST = False if __ofp_config['SCOPE']['SCOPEDB_TEST'].strip().lower() == "false" else True
    SCOPEDB_CONN_STR = __ofp_config['SCOPE']['CONN_STR'].strip()
    SCOPEDB_USR = __ofp_config['SCOPE']['SCOPEDB_USR'].strip()
    SCOPEDB_PWD = __ofp_config['SCOPE']['SCOPEDB_PWD'].strip()
    SCOPE_DETAIL_VIEW_URL = __ofp_config['SCOPE'].get('SCOPE_DETAIL_VIEW_URL', '').strip()

    DIGI_USER = __ofp_config['DIGI']['DIGI_USER']
    DIGI_USER_PSW = __ofp_config['DIGI']['DIGI_USER_PSW']
    DIGI_BASE_URL = __ofp_config["DIGI"]["DIGI_BASE_URL"]
    PROXY = __ofp_config["NETWORK"]["PROXY"]
    PROXY = PROXY if PROXY else None
    RUN_JOBS = True


class DevelopmentTestConfig(Config):

    __ofp_config = read_ofp_config()

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + sql_path + '/provenance.sqlite'
    SQLALCHEMY_ECHO = True
    USE_SCOPE_TEST = False if __ofp_config['SCOPE_T']['SCOPEDB_TEST'].strip().lower() == "false" else True
    SCOPEDB_CONN_STR = __ofp_config['SCOPE_T']['CONN_STR'].strip()
    SCOPEDB_USR = __ofp_config['SCOPE_T']['SCOPEDB_USR'].strip()
    SCOPEDB_PWD = __ofp_config['SCOPE_T']['SCOPEDB_PWD'].strip()
    RUN_JOBS = False


active_config = Config
