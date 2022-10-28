import db
import psycopg2
import config

config.load()


def init_db():
    try:
        query = (
            "CREATE TABLE messages ("
            "id serial PRIMARY key,"
            "body varchar(255) NOT NULL,"
            "nickname varchar(255) NOT NULL,"
            "created_at timestamptz NOT NULL"
            ")"
        )
        conn = db.create_connection()
        cur = conn.cursor()
        cur.execute(query)
        cur.close()
        conn.commit()
        print("Successfully created database tables")
    except (Exception, psycopg2.DatabaseError) as error:
        print("There was an error when attempting to create database tables:")
        print(error)

init_db()
