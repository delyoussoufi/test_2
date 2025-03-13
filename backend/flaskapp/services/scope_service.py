from contextlib import contextmanager
from datetime import datetime
from dateutil import parser
from typing import List, Dict, Union, Final

import cx_Oracle

from flaskapp.services import ExternalDbInterface
from flaskapp.services.external_db_interface import ScopeConfig
from flaskapp.utils import ListUtils


class ScopeGsftObjDtl:

    def __init__(self, *args):
        self.scope_id, self.daten_elemnt_id, self.bgn_dt, self.memo_txt = args
        if self.bgn_dt:
            self.bgn_dt: datetime
            self.bgn_dt = self.bgn_dt.date()

    def __repr__(self):
        atr = (f"{key}: {value}" for key, value in self.__dict__.items())
        return f"{type(self).__name__}({', '.join(atr)})"


class DigitalisatScopeInfo:

    # The attribute dat_findbuch has two ids because there is a difference between test and prod database.
    # TODO Let application decide. Remove this, it only adds overhead
    SCOPE_ELEMENTS: Final = ["title", "geburtsname", "dat_findbuch", "dat_findbuch", "geburtsdatum", "geburtsort",
                      "wohnort", "registry_signature", "associates"]

    # This should be set by ApplicationParamModel
    SCOPE_ELEMENTS_MAPPER: Dict[int, str] = {}

    def __init__(self, scope_id, signature):

        # it you change fields here, you must adapt ScopeDataModel.from_digitalisat_scope_info
        self.scope_id = scope_id
        self.signature = signature
        self.title = None
        self.geburtsname = None
        self.dat_findbuch = None
        self.geburtsdatum = None
        self.geburtsort = None
        self.wohnort = None
        self.registry_signature = None
        self.associates = None

        self._validate_attributes()

    def __repr__(self):
        atr = (f"{key}: {value}" for key, value in self.__dict__.items())
        return f"{type(self).__name__}({', '.join(atr)})"

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    @property
    def scope_elements_mapper(self) -> Dict[int, str]:
        if not DigitalisatScopeInfo.SCOPE_ELEMENTS_MAPPER:
            DigitalisatScopeInfo.set_scope_elements_mapper()

        return DigitalisatScopeInfo.SCOPE_ELEMENTS_MAPPER

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items()}

    def _validate_attributes(self):
        for v in self.SCOPE_ELEMENTS:
            self.__getattribute__(v)

    @classmethod
    def clear_scope_elements_mapper(cls):
        cls.SCOPE_ELEMENTS_MAPPER = {}

    @classmethod
    def set_scope_elements_mapper(cls):
        from flaskapp.models import ApplicationParamModel
        app_params_model: List[ApplicationParamModel] = ApplicationParamModel.get_scope_elements()
        cls.clear_scope_elements_mapper()
        cls.SCOPE_ELEMENTS_MAPPER = {int(p.param_value): p.param_id for p in app_params_model}

    def filter_gsft_objs_dtl(self, god: ScopeGsftObjDtl) -> bool:
        if str(god.scope_id).strip() != str(self.scope_id).strip():
            return False
        return bool(self.scope_elements_mapper.get(god.daten_elemnt_id, None))

    def map_gsft_objs_dtl(self, gsft_objs_dtl: List[ScopeGsftObjDtl]):

        for god in filter(self.filter_gsft_objs_dtl, gsft_objs_dtl):
            attr_name = self.scope_elements_mapper.get(god.daten_elemnt_id)
            v = god.memo_txt if god.memo_txt else god.bgn_dt
            self.__setattr__(attr_name, v)


class ScopeService(ExternalDbInterface):

    def __init__(self, config):
        """
        Scope service with a config object.
            Example::

                class Config:
                    USE_SCOPE_TEST: bool
                    SCOPEDB_CONN_STR: str
                    SCOPEDB_USR: str
                    SCOPEDB_PWD: str

        :param config: A config class
        """
        self.config: ScopeConfig = config
        self.table_schema: str = ""

        self.setup_configuration(config)

        self.table_vws_vrzng_enht_tree = "vws_vrzng_enht_tree"
        self.table_tbs_vrzng_enht = "TBS_VRZNG_ENHT"
        self.table_vwb_gsft_obj_dtl_grund_daten = "VWB_GSFT_OBJ_DTL_GRUND_DATEN"
        self.table_tbs_gsft_obj_dtl = "TBS_GSFT_OBJ_DTL"
        self.table_tbs_daten_elmnt = "TBS_DATEN_ELMNT"

        self.__append_schema_to_tables()

    def setup_configuration(self, config):
        """
        Set the new configuration to scope service.
        The config class must contain:
            USE_SCOPE_TEST: bool

            SCOPEDB_CONN_STR: str

            SCOPEDB_USR: str

            SCOPEDB_PWD: str

        :param config: The config class

        :return:
        """
        self.config: ScopeConfig = config
        self.table_schema = "aplkn_archv_blha"

    def __append_schema_to_tables(self):
        # TODO Refactoring: Remove schema from table name
        self.table_vws_vrzng_enht_tree = self.table_schema + "." + self.table_vws_vrzng_enht_tree
        self.table_tbs_vrzng_enht = self.table_schema + "." + self.table_tbs_vrzng_enht
        self.table_vwb_gsft_obj_dtl_grund_daten = self.table_schema + "." + self.table_vwb_gsft_obj_dtl_grund_daten
        self.table_tbs_gsft_obj_dtl = self.table_schema + "." + self.table_tbs_gsft_obj_dtl
        self.table_tbs_daten_elmnt = self.table_schema + "." + self.table_tbs_daten_elmnt

    @contextmanager
    def __open_connection(self):
        connection = None
        cursor = None
        try:
            usr = self.config.SCOPEDB_USR
            pwd = self.config.SCOPEDB_PWD
            conn_str = self.config.SCOPEDB_CONN_STR
            connection = cx_Oracle.connect(usr, pwd, conn_str)
            cursor = connection.cursor()
            yield cursor
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def get_signature(self, scope_id: int) -> Union[str, None]:
        """
        Gets the signature from the given scope id.

        :param scope_id: the scope id
        :return signature from scope id or None if not found.
        """
        signature_value = self.__get_result_with_select_column_and_where_column(
            "sgntr_cd", "vrzng_enht_id", scope_id)
        if not signature_value:
            return None
        return signature_value

    def get_id(self, signature: str) -> Union[int, None]:
        """
        Gets the id from the given signature.

        :param signature: the signature
        :return id from signature or None if not found.
        """
        id_value = self.__get_result_with_select_column_and_where_column(
            "vrzng_enht_id", "sgntr_cd", signature)
        if not id_value:
            return None
        return int(id_value)

    def get_title(self, scope_id: int) -> Union[str, None]:
        """
        Gets the title from the given scope id.

        :param scope_id: the scope id
        :return title from scope id or None if not found.
        """
        title_value = self.__get_result_with_select_column_and_where_column(
            "vrzng_enht_titel", "vrzng_enht_id", scope_id)
        if not title_value:
            return None
        return title_value

    def get_classification_type_id(self, scope_id: str) -> str:
        """
        Gets the classification type id from the given scope id.

        :param scope_id: the scope id.
        :return: Classification id from the given scope id. None if nothing is found.
        """
        if scope_id and scope_id != "":
            result = self.__get_result_with_select_column_and_where_column_and_table("vrzng_enht_entrg_typ_id",
                                                                                     "vrzng_enht_id", scope_id,
                                                                                     self.table_tbs_vrzng_enht)
            return str(result) if result else None

    @staticmethod
    def convert_to_datetime(cursor: cx_Oracle.Cursor, name, default_type, size, precision, scale):
        def parse_date(date_str):
            if date_str:
                return parser.parse(date_str)
            return None

        if default_type == cx_Oracle.DB_TYPE_DATE:
            return cursor.var(cx_Oracle.STRING, arraysize=cursor.arraysize,
                              outconverter=parse_date)

    def get_gsft_obj_dtl(self, scope_id: int):

        with self.__open_connection() as cursor:
            # alter datetime format, default = YY.MM.DD. Which causes problem with old dates
            sql = """alter session set nls_date_format = 'YYYY.MM.DD' nls_timestamp_tz_format = 'YYYY.MM.DD'"""
            cursor.execute(sql)
            # Construct the query.
            select_sql = f"SELECT gsft_obj_id, DATEN_ELMNT_ID, BGN_DT, MEMO_TXT FROM " \
                         f"{self.table_tbs_gsft_obj_dtl} WHERE gsft_obj_id =:match_value AND ELMNT_SQNZ_NR = 1"

            cursor: cx_Oracle.Cursor
            cursor.outputtypehandler = self.convert_to_datetime
            cursor.execute(select_sql, match_value=scope_id)
            results = []
            for r in cursor:
                dto = ScopeGsftObjDtl(*r)
                # dto = {"scope_id": r[0], "daten_elemnt_id": r[1], "bgn_dt": r[2], "memo_txt": r[3]}
                results.append(dto)

        return results

    def __get_result_with_select_column_and_where_column(self, select_col, where_col: str, match_value) -> str:
        """
        Gets the result from SELECT selectCol FROM tableVwsVrzngEnhtTree WHERE whereCol = matchValue.

        :param select_col the name of the column to select.
        :param where_col the name of the column to check if matchValue is equal.
        :param match_value the value to match.
        :return the query results
        :raise Exception throw exceptions.
        """
        return self.__get_result_with_select_column_and_where_column_and_table(select_col,
                                                                               where_col, match_value,
                                                                               self.table_vws_vrzng_enht_tree)

    def __get_result_with_select_column_and_where_column_and_table(
            self, select_col: str, where_col: str, match_value: any, table: str) -> str:
        """
        Gets the result from SELECT selectCol FROM table WHERE whereCol = matchValue.

        :param select_col the name of the column to select.
        :param where_col the name of the column to check if matchValue is equal.
        :param match_value the value to match.
        :param table the table to query.
        :return the query results.
        :raise Exception throw exceptions.
        """
        result = ""
        with self.__open_connection() as cursor:
            # Construct the query.
            select_sql = "SELECT " + select_col + " " + "FROM " + table + " " + "WHERE " + where_col + "=:match_value"

            cursor.execute(select_sql, match_value=match_value)
            for select_val in cursor:
                result = select_val[0]

        return result

    def __get_results_with_select_column_and_where_column(self, select_col: str, where_col: str,
                                                          match_values: List[str]) -> Dict[str, str]:
        """
        Gets the result from SELECT selectCol FROM tableVwsVrzngEnhtTree WHERE whereCol IN(matchValue).

        :param select_col the name of the column to select.
        :param where_col the name of the column to check if matchValue is equal.
        :param match_values list of values to match.
        :return A map that contain the query results.The key is the value from whereCol in the db.
        :raise Exception throw exceptions.
        """
        results = {}
        with self.__open_connection() as cursor:

            for chunk_values in ListUtils.chunks(match_values, 900):
                # Construct the query.
                select_sql = "SELECT " + select_col + "," + where_col + \
                             " FROM " + self.table_vws_vrzng_enht_tree + \
                             " WHERE " + where_col + " IN ("

                for i, value in enumerate(chunk_values):
                    if i == 0:
                        select_sql += "'" + str(value) + "'"
                    else:
                        select_sql += ",'" + str(value) + "'"
                select_sql += ")"

                cursor.execute(select_sql)
                for select_val, where_val in cursor:
                    results[where_val] = select_val
        return results
