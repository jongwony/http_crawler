# -*- coding: utf-8 -*-
import sqlite3
from src.abstract import Transaction, DB_Cursor


class ExampleCrawl(Transaction):
    def __init__(self, working_dir):
        super().__init__(working_dir)

    def http_requests_parameter(self):
        return {
            'method': 'GET',
            'url': 'https://github.com',
        }


if __name__ == '__main__':
    """For Debugging: python3 -i example.py"""
    main_crawl = ExampleCrawl('demo')
    response = main_crawl.request()
    main_crawl.save_raw_file('test.html', response)
    main_crawl.set_db_connection(sqlite3.connect('test.sqlite3'))

    with DB_Cursor(main_crawl.db_connection) as cursor:
        try:
            cursor.execute('''CREATE TABLE test(test text)''')
        except sqlite3.OperationalError as e:
            print(e.args)
        for i in range(10):
            placeholder = 'test' + format(i)
            cursor.execute('''INSERT INTO test VALUES (?)''', (placeholder,))

        main_crawl.db_connection.commit()

        cursor.execute('''SELECT * FROM test''')
        for row in cursor:
            print(row)
