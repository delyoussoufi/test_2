import psutil


class SystemUtils:

    BYTE_TO_MB = 9.5367e-7

    @staticmethod
    def get_estimated_free_memory() -> float:
        """
        Get an estimation of the allocable free memory.
        :return: The total amount of memory in MB that can be still allocate.
        """
        return psutil.virtual_memory().free * SystemUtils.BYTE_TO_MB
