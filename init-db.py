import db
import config

config.load()


def init_db():
    query = (
        "CREATE TABLE IF NOT EXISTS messages ("
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


init_db()
