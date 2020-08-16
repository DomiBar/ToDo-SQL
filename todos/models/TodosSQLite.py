import sqlite3
from sqlite3 import Error
import os

db_file = "..\static\Todos.db"

create_todos_sql = """
    -- Todos table
    CREATE TABLE IF NOT EXISTS todos (
    id integer PRIMARY KEY,
    title text NOT NULL,
    description text,
    done integer
    );
    """


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


class TodosSQLite:
    def __init__(self):
        conn = create_connection(db_file)
        if conn is not None:
            execute_sql(conn, create_todos_sql)
            conn.close()

    def select_all(self, table="todos"):
        """
        Query all rows in the table
        :param conn: the Connection object
        :return:
        """
        conn = create_connection(db_file)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()

        return rows

    def select_where(self, id, table="todos"):
        """
        Query tasks from table with data from id
        :param conn: the Connection object
        :param table: table name
        :param id: id number
        :return:
        """
        conn = create_connection(db_file)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} WHERE id=?", (id,))
        rows = cur.fetchall()
        return rows

    def add_todo(self, todo):
        """
        Create a new todo into the projects table
        :param conn:
        :param todo:
        :return:
        """
        conn = create_connection(db_file)
        sql = '''INSERT INTO todos(title, description, done)
              VALUES(?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql, todo)
        conn.commit()

    def update(self, id, table="todos", **kwargs):
        """
        update title, description, and done of todo
        :param conn:
        :param table: table name
        :param id: row id
        :return:
        """
        conn = create_connection(db_file)
        parameters = [f"{k} = ?" for k in kwargs]
        parameters = ", ".join(parameters)
        values = tuple(v for v in kwargs.values())
        values += (id, )

        sql = f''' UPDATE {table}
              SET {parameters}
              WHERE id=?'''
        try:
            cur = conn.cursor()
            cur.execute(sql, values)
            conn.commit()
            print("OK")
        except sqlite3.OperationalError as e:
            print(e)

    def delete_where(self, id, table="todos"):
        """
        Delete from table where id
        :param conn:  Connection to the SQLite database
        :param id: id of row to delete
        :param table: table name
        :return:
        """
        conn = create_connection(db_file)
        try:
            sql = f'DELETE FROM {table} WHERE id=?'
            cur = conn.cursor()
            cur.execute(sql, (id,))
            conn.commit()
            return True
        except Exception:
            return False


todos = TodosSQLite()
