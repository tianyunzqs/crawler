# -*- coding: utf-8 -*-
# @Time        : 2019/3/15 9:52
# @Author      : tianyunzqs
# @Description : mysql数据库操作工具类

import datetime
import unittest
import pymysql


class MysqlClient(object):
    """
    mysql数据库操作类
    """
    def __init__(self, host, user, password, database, port):
        conf = {
            "host": host,
            "user": user,
            "password": password,
            "database": database,
            "port": int(port),
            "cursorclass": pymysql.cursors.DictCursor,
            "charset": "utf8"
        }
        self.conn = pymysql.connect(**conf)
        self.cursor = self.conn.cursor()

    def query(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()
        row = self.cursor.fetchall()
        return row

    def update(self, sql):
        effect_row = self.cursor.execute(sql)
        self.conn.commit()
        return effect_row

    def insert_many(self, sql, param):
        effect_row = self.cursor.executemany(sql, param)
        self.conn.commit()
        return effect_row

    def __del__(self):
        self.conn.close()


class TestMysqlClient(unittest.TestCase):
    """
    各个方法的单元测试
    """
    def __init__(self, *args, **kwargs):
        super(TestMysqlClient, self).__init__(*args, **kwargs)
        self.host = "10.95.132.15"
        self.user = "root"
        self.password = "Fhpt2020!"
        self.database = "ezhou_police"
        self.port = "3306"
        self.mysql_instance = MysqlClient(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          database=self.database,
                                          port=self.port)
        self.test_table_name = 'mysql_test_' + datetime.datetime.now().strftime("%Y%m%d%H%M")

    def test_create(self):
        print("=" * 50, "create test", "=" * 50)
        sql = """
            CREATE TABLE {0}(
               ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
               NAME VARCHAR(20) NOT NULL,
               AGE INT NOT NULL,
               ADDRESS VARCHAR(50),
               SALARY FLOAT 
            );
        """.format(self.test_table_name)
        rows = self.mysql_instance.update(sql=sql)
        print(rows)

    def test_insert(self):
        print("=" * 50, "insert test", "=" * 50)
        sql = """
            INSERT INTO {0} (NAME,AGE,ADDRESS,SALARY) VALUES ('Paul', 32, 'California', 20000.00)
        """.format(self.test_table_name)
        rows = self.mysql_instance.update(sql=sql)
        print(rows)

    def test_query(self):
        print("=" * 50, "query test", "=" * 50)
        sql = """
            SELECT * FROM {0}
        """.format(self.test_table_name)
        rows = self.mysql_instance.query(sql=sql)
        print(rows)

    def test_insert_many(self):
        print("=" * 50, "insert_many test", "=" * 50)
        values = [
            ('Allen', 25, 'Texas', 15000.00),
            ('Teddy', 23, 'Norway', 20000.00),
            ('Mark', 25, 'Rich-Mond ', 65000.00)
        ]
        sql = """
            INSERT INTO {0}(NAME, AGE, ADDRESS, SALARY) VALUES(%s, %s, %s, %s)
        """.format(self.test_table_name)
        rows = self.mysql_instance.insert_many(sql=sql, param=values)
        print(rows)

    def test_update(self):
        print("=" * 50, "update test", "=" * 50)
        sql = """
            UPDATE {0} SET SALARY=20000 WHERE name='Allen'
        """.format(self.test_table_name)
        rows = self.mysql_instance.update(sql=sql)
        print(rows)

    def test_delete(self):
        print("=" * 50, "delete test", "=" * 50)
        sql = """
            DELETE FROM {0} WHERE name='Mark'
        """.format(self.test_table_name)
        rows = self.mysql_instance.update(sql=sql)
        print(rows)

    def test_drop(self):
        print("=" * 50, "drop test", "=" * 50)
        sql = """
            DROP TABLE {0}
        """.format(self.test_table_name)
        rows = self.mysql_instance.update(sql=sql)
        print(rows)


if __name__ == '__main__':
    # 在pycharm中直接运行该测试脚本会报错，请参考https://www.pythonheidong.com/blog/article/493096/c958bb7fc8cf2661b29e/
    # 构造测试集
    suite = unittest.TestSuite()
    suite.addTest(TestMysqlClient('test_create'))
    suite.addTest(TestMysqlClient("test_insert"))
    suite.addTest(TestMysqlClient("test_query"))
    suite.addTest(TestMysqlClient("test_insert_many"))
    suite.addTest(TestMysqlClient("test_query"))
    suite.addTest(TestMysqlClient("test_update"))
    suite.addTest(TestMysqlClient("test_query"))
    suite.addTest(TestMysqlClient("test_delete"))
    suite.addTest(TestMysqlClient("test_query"))
    suite.addTest(TestMysqlClient("test_drop"))
    # 执行测试
    runner = unittest.TextTestRunner()
    runner.run(suite)
