import sqlite3
import json
from models import Subscription, User, Post
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
            s.follower_id ,
            s.author_id,
            s.created_on,
            u1.first_name follower_first_name,
            u1.last_name follower_last_name,
            u1.email follower_email,
            u1.bio follower_bio,
            u1.username follower_username,
            u1.password follower_password,
            u1.profile_image_url follower_profile_image_url,
            u1.created_on follower_created_on,
            u1.active follower_active,
            u2.first_name author_first_name,
            u2.last_name author_last_name,
            u2.email author_email,
            u2.bio author_bio,
            u2.username author_username,
            u2.password author_password,
            u2.profile_image_url author_profile_image_url,
            u2.created_on author_created_on,
            u2.active author_active,
            p.id post_id,
            p.user_id,
            p.category_id ,
            p.title ,
            p.publication_date ,
            p.image_url ,
            p.content ,
            p.approved
        FROM Subscriptions s
        JOIN Users u1
            ON u1.id = s.follower_id
        JOIN Users u2
            ON u2.id = s.author_id
        JOIN Posts p
            ON p.user_id = s.author_id
        """)
        subscriptions = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            subscription = Subscription(row['id'], row['follower_id'], row['author_id'], row['created_on'])
            
            follower = User(
                row["follower_id"],
                row["follower_first_name"],
                row["follower_last_name"],
                row["follower_email"],
                row["follower_bio"],
                row["follower_username"],
                row["follower_password"],
                row["follower_profile_image_url"],
                row["follower_created_on"],
                row["follower_active"],
            )
            author = User(
                row["author_id"],
                row["author_first_name"],
                row["author_last_name"],
                row["author_email"],
                row["author_bio"],
                row["author_username"],
                row["author_password"],
                row["author_profile_image_url"],
                row["author_created_on"],
                row["author_active"],
            )
            post = Post(
                row["post_id"],
                row["user_id"],
                row["category_id"],
                row["title"],
                row["publication_date"],
                row["image_url"],
                row["content"],
                row["approved"],
            )
            
            subscription.follower = follower.__dict__
            subscription.author = author.__dict__
            subscription.post = post.__dict__
            

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
        FROM Subscriptions s
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
                created_on = ?
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