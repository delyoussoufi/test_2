import json
import os
import re
from typing import List
from urllib.parse import urlencode

import requests as requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from flaskapp import active_config, app_logger


class DigiRequests(requests.Session):

    CACHED_TOKEN = {}

    def __init__(self, base_url: str = active_config.DIGI_BASE_URL, user_name: str = active_config.DIGI_USER,
                 user_psw: str = active_config.DIGI_USER_PSW, proxy=active_config.PROXY):

        super().__init__()
        self._base_url = base_url
        self._base_request = f"{self._base_url}/rest/public"
        retries = Retry(total=5,
                        backoff_factor=0.1,
                        status_forcelist=[500, 502, 503, 504])
        self.mount(self._base_url, HTTPAdapter(max_retries=retries))
        if not proxy:
            os.environ['NO_PROXY'] = '127.0.0.1'
        else:
            self.proxies["http"] = proxy
            self.proxies["https"] = proxy

        self.token = self.CACHED_TOKEN.get(user_name, None)
        self.__has_login = self.token is not None
        try:
            if not self.token:
                self.token = self.login(username=user_name, password=user_psw)
            if not self.token:
                raise ConnectionError(f"User {user_name} has no access to digiproduction. Please check your password.")
        except requests.exceptions.ConnectionError:
            app_logger.info(f"No Connection. User {user_name} fail to login to Digiproduction.")
            # TODO handle error for production use
        else:
            self.CACHED_TOKEN[user_name] = self.token

        self.headers["X-Access-Token"] = self.token

    def login(self, username, password):
        payload = {"username": f"{username}", "password": f"{password}"}
        headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}
        with self.post(f"{self._base_request}/authentication", data=payload, headers=headers) as r:
            if r.status_code == 200:
                self.__has_login = True
                return r.json()
            return None

    def has_connection(self):
        return self.__has_login

    def get_bestand(self, bestand_id):
        with self.get(f"{self._base_request}/bestand/{bestand_id}") as r:
            if r.status_code == 200:
                return r.json()
        return None

    def search_bestaende(self, bestand_search):
        with self.get(f"{self._base_request}/bestand/search?{urlencode(bestand_search.to_dict())}") as r:
            if r.status_code == 200:
                return r.json()
        return None

    def get_digitalisate(self, bestand_id):
        with self.get(f"{self._base_request}/digitalisate/{bestand_id}") as r:
            if r.status_code == 200:
                return r.json()
        return []

    def get_digitalisate_stream(self, bestand_id):

        with self.get(f"{self._base_request}/digitalisate_stream/{bestand_id}", stream=True) as r:
            if r.status_code == 200:
                for line in r.iter_lines(decode_unicode=True):
                    if line:
                        yield json.loads(line)

    def get_digitalisat_images(self, digitalisat_id):
        with self.get(f"{self._base_request}/digitalisat_images/{digitalisat_id}") as r:
            if r.status_code == 200:
                images_list: List[dict] = r.json()
                images_list.sort(key=lambda i: i.get("order", 0))
                return images_list
        return []

    def get_image_file(self, image_id, output_dir, name=None):
        if not os.path.isdir(output_dir):
            AttributeError(f"output_dir={output_dir} must be an existing directory.")

        with self.get(f"{self._base_request}/image_file/{image_id}", stream=True) as r:
            if r.status_code == 200:
                content = r.headers['content-disposition']
                filename = name or re.findall("filename=(.+)", content)[0]
                output = os.path.join(output_dir, filename)
                size = r.headers['content-length']
                with open(output, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=256*1024):
                        f.write(chunk)

                return output, size
        return None, 0

    def get_ocr_data(self, image_id, output_dir):
        """
        Gets the OCR data as text and writes the alto and json files into the given directory.

        :param image_id: The id of digitalisat_image
        :param output_dir: The directory where the ocr data as alto and json should be store.
        :return: An ocr text data or None.
        """
        if not os.path.isdir(output_dir):
            AttributeError(f"output_dir={output_dir} must be an existing directory.")

        def write_file(response):
            content = response.headers['content-disposition']
            filename = re.findall("filename=(.+)", content)[0]
            output = os.path.join(output_dir, filename)
            size = r.headers['content-length']
            with open(output, 'wb') as f:
                for chunk in r.iter_content(chunk_size=256 * 1024):
                    f.write(chunk)
            return output, size

        with self.get(f"{self._base_request}/ocr_data_json/{image_id}", stream=True) as r:
            if r.status_code == 200:
                write_file(r)
            else:
                return None

        with self.get(f"{self._base_request}/ocr_data_alto/{image_id}", stream=True) as r:
            if r.status_code == 200:
                write_file(r)
            else:
                return None

        with self.get(f"{self._base_request}/ocr_data/{image_id}") as r:
            if r.status_code == 200:
                r.encoding = "utf-8"
                ocr_data = r.json()
                return ocr_data
            else:
                return None
