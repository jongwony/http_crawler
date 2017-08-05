import os
from abc import ABCMeta, abstractmethod
from src.store_dir import ProjectDir
from src.http_fetch import Crawl
from src.log import Log


class Transaction(metaclass=ABCMeta):
    def __init__(self, name):
        self.dir = ProjectDir(name)
        self.db_connection = None
        self.http_session = Crawl(os.path.join(self.dir.log_dir(), 'session.log'))
        self.log = Log(os.path.join(self.dir.log_dir(), 'transaction.log'))

    def request(self, sleep=3):
        return self.http_session.make_response(self.http_requests_parameter(), sleep)

    def save_raw_file(self, filename, response):
        """
        :param filename: filename
        :param response: requests.response
        """
        encoding = response.encoding
        if encoding.lower() != 'utf-8':
            self.log.warning('Check Page Encoding!, {}'.format(str(response.headers)))

        with open(os.path.join(self.dir.data_dir(), filename), mode='w', encoding=encoding) as f:
            f.write(response.content.decode(encoding))

    @staticmethod
    def remove_file(save_path):
        """
        Avoid file collision
        """
        if os.path.isfile(save_path):
            os.remove(save_path)

    @abstractmethod
    def http_requests_parameter(self):
        """
        requests_parameter: {
            'method': 'GET',
            'url': base_url + path,
            'params': dictionary or inline string,
            'headers': dictionary,
        }
        :return: dictionary
        """
        pass

    def set_db_connection(self, db_connection):
        """
        self.db_connection: Database.connect
        """
        self.db_connection = db_connection

    def __del__(self):
        if self.db_connection is not None:
            self.db_connection.close()


class DB_Cursor:
    def __init__(self, db_connection):
        self.cursor = db_connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
