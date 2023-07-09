import sqlite3
from sqlite3 import Error
from popups import display_message


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        display_message(repr(e))

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        display_message(repr(e))


def create_location(conn, location):
    """
    Create a new location
    :param conn:
    :param location: location path
    :return:
    """
    try:
        sql = """ INSERT INTO locations(location)
                VALUES(?) """
        cur = conn.cursor()
        cur.execute(sql, location)
        conn.commit()
        display_message("success_create")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def create_office(conn, name):
    """
    Create a new office
    :param conn:
    :param name: office name
    :return:
    """
    if len(name[0]) < 2:
        display_message(
            "Record not added! Office name cannot be blank or less than 2 characters."
        )
        return False
    try:
        sql = """ INSERT INTO offices(name)
                VALUES(?) """
        cur = conn.cursor()
        cur.execute(sql, name)
        conn.commit()
        display_message("success_create")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def update_location(conn, location):
    """
    Create a new location
    :param conn:
    :param location: tuple of location and rowid
    :return:
    """
    try:
        sql = """ UPDATE locations
                SET location = ? 
                WHERE rowid = ?"""
        cur = conn.cursor()
        cur.execute(sql, location)
        conn.commit()
        display_message("success_update")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def update_office(conn, office):
    """
    Create a new office
    :param conn:
    :param office: tuple of office name and rowid
    :return:
    """
    for field in office:
        if len(office[0]) < 2:
            display_message(
                "Record not added! Office name cannot be blank or less than 2 characters."
            )
            return False
    try:
        sql = """ UPDATE offices
                SET name = ? 
                WHERE rowid = ?"""
        cur = conn.cursor()
        cur.execute(sql, office)
        conn.commit()
        display_message("success_update")
    except Error as e:
        display_message(repr(e))
        return False
    return True


def select_location(conn):
    """
    Query all rows in the locations table
    :param conn: the Connection object
    :return:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT rowid, location FROM locations WHERE rowid=1;")

        location = cur.fetchone()
        return location
    except Error as e:
        display_message(repr(e))
    return


# def select_all_offices(conn):
#     """
#     Query all rows in the offices table
#     :param conn: the Connection object
#     :return offices:
#     """
#     try:
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM offices")

#         offices = cur.fetchall()
#         return offices
#     except Error as e:
#         display_message(repr(e))


def select_office(conn):
    """
    Retrieve an office from the offices table
    :param conn: the Connection object
    :param name: name of offices
    :return office:
    """
    try:
        cur = conn.cursor()
        cur.execute("SELECT rowid, name FROM offices WHERE rowid=1")

        row = cur.fetchone()
        return row
    except Error as e:
        display_message(repr(e))


def drop_table(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return


def setup_db():
    try:
        database = "mydb.db"

        sql_create_locations_table = """CREATE TABLE IF NOT EXISTS locations (
                                        location text NOT NULL
                                    );"""

        sql_create_offices_table = """CREATE TABLE IF NOT EXISTS offices (
                                        name text NOT NULL
                                    );"""

        # create a database connection
        conn = create_connection(database)

        # create tables
        if conn is not None:
            with conn:
                # create locations table
                create_table(conn, sql_create_locations_table)

                # create offices table
                create_table(conn, sql_create_offices_table)
        else:
            display_message("Error! cannot create the database connection.")
    except Error as e:
        display_message(repr(e))
    return


if __name__ == "__main__":
    setup_db()
