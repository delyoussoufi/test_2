from abc import ABC, abstractmethod


class ScopeConfig(ABC):

    USE_SCOPE_TEST: bool
    SCOPEDB_CONN_STR: str
    SCOPEDB_USR: str
    SCOPEDB_PWD: str


class ExternalDbInterface(ABC):

    @abstractmethod
    def get_signature(self, id: str) -> str:
        """
        Gets the signature from the given id.
        :param id: id
        :return: signature for id.
        """
        pass

    @abstractmethod
    def get_title(self, id: str) -> str:
        """
        Gets the title from the given id.
        :param id: id
        :return: title for id
        """
        pass

    @abstractmethod
    def get_id(self, signature: str) -> str:
        """
        Gets the id from the given signature.
        :param signature the signature to search for
        :return: the id
        """
        pass