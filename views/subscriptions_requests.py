import sqlite3
import json
from models import Subscription
SUBSCRIPTIONS = [
    {
        "id":1,
        "follower_id":1,
        "author_id":1,
        "created_on":2022-10-19
    },
    {
        "id":2,
        "follower_id":2,
        "author_id":2,
        "created_on":2022-10-31
    }
]

def get_all_subscriptions():
    with sqlite3.connect("./rare.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM Subscription s
        """)
        subscriptions = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])

            subscriptions.append(subscription.__dict__)

        return json.dumps(subscriptions)

def get_single_subscription(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            s.id,
            s.follower_id,
            s.author_id,
            s.created_on
        FROM Subscription s
        WHERE s.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an animal instance from the current row
        subscription = Subscription(data['id'], data['follower_id'], data['author_id'], data['created_on'])

        return json.dumps(subscription.__dict__)

def delete_subscription(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Subscription
        WHERE id = ?
        """, (id, ))

def update_subscription(id, new_subscription):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Subscription
            SET
                follower_id = ?,
                author_id = ?,
                created_on = ?,
        WHERE id = ?
        """, (new_subscription['follower_id'], new_subscription['author_id'],new_subscription['created_on'],id, ))

        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        return False
    else:
        return True

def create_subscription(new_subscription):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Subscription
            ( follower_id, author_id, created_on )
        VALUES
            ( ?, ?, ?, ?, ?);
        """, (new_subscription['follower_id'], new_subscription['author_id'],
              new_subscription['created_on'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the animal dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_subscription['id'] = id


    return new_subscription