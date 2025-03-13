import errno
import hashlib
import os
import pathlib
import shutil
import tarfile
import tempfile
from datetime import datetime
from typing import List
from zipfile import ZipFile


class FileUtils:

    @staticmethod
    def get_file_extension(file_name: str) -> str:
        """
        Get the file extension,

            file.jpg returns jpg

            file returns ""

        :param file_name: The name of the file, expects to be a string.

        :return: The file extension
        """
        try:
            split_name = str(file_name).split(".")
            if len(split_name) < 2:
                return ""
            return split_name.pop(-1)
        except IndexError:
            return ""

    @staticmethod
    def remove_filename_extension(file_name: str) -> str:
        """
        Gets the file name and return its name without extension.

        :param file_name: A string with the file name.
        :return: The name without its extension.
        """
        if "." in file_name:
            return file_name[:file_name.rindex(".")]
        return file_name

    @staticmethod
    def get_subfolders(file_path: str) -> List[str]:
        """
        Get the sub folders for a given file path,

        :param file_path: The path to the parent file.

        :return: A list of the sub folders
        """
        # noinspection PyUnresolvedReferences
        return [f.path for f in os.scandir(file_path) if f.is_dir()]

    @staticmethod
    def get_folder_name_from_path(file_path: str) -> str:
        """
        Get the folder name for a given file path,

        :param file_path: The path to the parent file.

        :return: the folder name of the given path.
        """
        path = pathlib.PurePath(file_path)
        return path.name

    @staticmethod
    def get_file_name_from_path(file_path: str) -> str:
        """
        Get the file name for a given file path,

        :param file_path: The path to the file.

        :return: the file name of the given path.
        """

        return os.path.basename(file_path)

    @staticmethod
    def zip_files(file_paths: List[str], output_path: str = None, file_names=None) -> str:
        """
        Compress a list of files into a zip file. If output_path is not given it will be
        saved as a temporary file.

        :param file_paths: The list of files path to be compressed.

        :param output_path: (Optional) The output file path.

        :param file_names: A list of names to use for the files. If not provided it will use the name of the
        file in the given path (default). This should have the same length as file_paths

        :return: The path of the compressed zip file.
        """
        if not output_path:
            tmp_file = tempfile.NamedTemporaryFile(suffix=".zip")
            output_path = tmp_file.name
            tmp_file.close()

        if file_names is None:
            file_names = [os.path.basename(file_path) for file_path in file_paths]

        if len(file_names) != len(file_paths):
            raise ValueError("file_paths has to be the same length as file_names")

        with ZipFile(file=output_path, mode='w') as zf:
            for file_path, filename in zip(file_paths, file_names):
                zf.write(filename=file_path, arcname=filename)

        return output_path

    @classmethod
    def __zip_file(cls, file_path: str, filename: str, zf: ZipFile):

        if os.path.isdir(file_path):
            dir_path = file_path
            for filename in os.listdir(file_path):
                file_path = os.path.join(dir_path, filename)
                cls.__zip_file(file_path, filename=os.path.join(os.path.basename(dir_path), filename), zf=zf)
        else:
            zf.write(filename=file_path,  arcname=filename)

    @classmethod
    def zip_dirs(cls, dir_paths: List[str], output_path=None):
        if not output_path:
            tmp_file = tempfile.NamedTemporaryFile(suffix=".zip")
            output_path = tmp_file.name
            tmp_file.close()
        with ZipFile(file=output_path, mode='w') as zf:
            for dir_path in dir_paths:
                cls.__zip_file(dir_path, filename=os.path.join(os.path.basename(dir_path)), zf=zf)

        return output_path

    @staticmethod
    def tar_files(file_paths: List[str], output_path: str = None) -> str:
        """
        Compress a list of files into a tar file. If output_path is not given it will be
        saved as a temporary file.

        :param file_paths: The list of files path to be compressed.

        :param output_path: (Optional) The output file path.

        :return: The path of the compressed tar file.
        """
        if not output_path:
            tmp_file = tempfile.NamedTemporaryFile(suffix=".tar")
            output_path = tmp_file.name
            tmp_file.close()

        with tarfile.open(name=output_path, mode='w') as tf:
            for file_path in file_paths:
                filename = os.path.basename(file_path)
                tf.add(name=file_path, arcname=filename)

        return output_path

    @staticmethod
    def archive_dir(dir_path: str, file_format: str = "zip", output_path: str = None):
        """
        Compress a directory into a file_format file. If output_path is not given it will be
        saved as a temporary file.

        :param dir_path: The directory path to be compressed.

        :param file_format: str one of "zip", "tar", "gztar", "bztar", or "xztar".

        :param output_path: (Optional) The output file path.

        :return: The path of the compressed file.
        """
        if not output_path:
            tmp_file = tempfile.NamedTemporaryFile()
            output_path = tmp_file.name
            tmp_file.close()
        else:
            file_ext = FileUtils.get_file_extension(file_name=output_path)
            output_path = output_path.replace("." + file_ext, "")
        output_path = shutil.make_archive(output_path, format=file_format, root_dir=dir_path)
        return output_path

    @staticmethod
    def is_dir_online(dir_path: str):
        """
        Check is is dir and if exists.

        :param dir_path: The directory full path.

        :return: True if is a dir and exists, false otherwise.
        """
        if os.path.isdir(dir_path) and os.path.exists(dir_path):
            return True
        else:
            return False

    @staticmethod
    def get_xml_files(dir_path: str) -> [str]:
        """
        Get all xml files within the given folder.
        :param dir_path: The folder's path were it should retrieve the files.
        :return: All the files(*.xml) within the folder.
        """
        # Filter the files it should get.
        xml_files = []
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path) and file.lower().endswith(".xml"):
                xml_files.append(file_path)
        return xml_files

    @staticmethod
    def get_files(dir_path: str, valid_extensions: List[str] = None) -> [str]:
        """
        Get all files within the given folder.

        :param dir_path: The folder's path were it should retrieve the files.
        :param valid_extensions: Optional. A list of file's extensions, i.e: [".tif", ".tiff", ".jpg", ".jpeg"]

        :return: All the files within the folder. If valid_extensions is provided return the files that match it.
        """
        # Filter the files it should get.
        files = []
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            _, extension = os.path.splitext(filename)
            if os.path.isfile(file_path):
                if valid_extensions is None:
                    files.append(file_path)
                elif extension.lower() in valid_extensions:
                    files.append(file_path)
        return files

    @classmethod
    def get_image_files(cls, dir_path: str) -> [str]:
        """
        Get all images files within the given folder.

        :param dir_path: The folder's path were it should retrieve the files.

        :return: All the files(*.tif, *.jpg, *.jpeg) within the folder.
        """
        # Filter the files it should get.
        valid_extensions = [".tif", ".tiff", ".jpg", ".jpeg"]
        return cls.get_files(dir_path=dir_path, valid_extensions=valid_extensions)

    @classmethod
    def clean_temp_dir(cls):
        valid_extensions = [".tif", ".tiff", ".jpg", ".jpeg", ".pdf", ".zip"]
        temp_dir_path = tempfile.gettempdir()
        files_path = cls.get_files(temp_dir_path, valid_extensions=valid_extensions)
        for file_path in files_path:
            create_date = datetime.fromtimestamp(os.path.getctime(file_path)).date()
            delta_time = (datetime.today().date() - create_date).days
            if delta_time > 1:
                try:
                    os.remove(file_path)
                except (IOError, PermissionError):
                    pass

    @staticmethod
    def get_disk_info(disk_path: str = None):
        """
        Get information about the disk in the given path.

        :param disk_path: Any dir location in the disk. If None, the root dir will be used.

        :return: A tuple with attributes 'total', 'used' and 'free', which are the amount
        of total, used and free space, in gigabytes.
        """
        try:
            total, used, free = shutil.disk_usage(disk_path) if disk_path else shutil.disk_usage(
                os.path.abspath(os.sep))
        except FileNotFoundError:
            total, used, free = (0., 0., 0.)
        gb = 1. / 2 ** 30  # bites to GB.
        return total * gb, used * gb, free * gb

    @staticmethod
    def get_file_size(file_path: str) -> float:
        """
        Returns the file size in MB.
        :param file_path: The file absolute path. Include the file name.
        :return: The file size in MB.
        """
        if os.path.exists(file_path):
            return os.path.getsize(file_path) / (1024*1024.0)
        return 0.

    @classmethod
    def remove_dir(cls, dir_path, force=True):
        """
        Try to remove a directory.

        :param dir_path: The directory absolute path.
        :param force: Default=True. It will ignore IOError NotEmpty once and it will try to remove again,
            if it fails for the second attempt then an IOError will be raised.
        :return:
        :raise IOError:
        """
        if os.path.isdir(dir_path):
            if force:
                try:
                    shutil.rmtree(dir_path)
                except IOError as e:
                    if e.errno == errno.ENOTEMPTY:
                        cls.remove_dir(dir_path, force=False)
                    else:
                        raise
            else:
                shutil.rmtree(dir_path)

    @staticmethod
    def is_tiff(extension: str):
        if extension is not None:
            extension = extension.lower()
            return extension == "tif" or extension == "tiff"
        return False

    @staticmethod
    def is_jpeg(extension: str):
        if extension is not None:
            extension = extension.lower()
            return extension == "jpg" or extension == "jpeg"
        return False

    @staticmethod
    def create_hash(file_path: str) -> str:
        """
        Creates a hex key from a file.

        :param file_path: the path to the file
        :return: The hash for this file.
        """
        h = hashlib.sha1()
        # b = bytearray(128 * 1024)
        # mv = memoryview(b)
        buffer = 128 * 1024
        with open(file_path, 'rb', buffering=0) as f:
            while chunk := f.read(buffer):
                h.update(chunk)
            # for n in iter(lambda: f.readinto(mv), 0):
            #     h.update(mv[:n])
        return h.hexdigest()
