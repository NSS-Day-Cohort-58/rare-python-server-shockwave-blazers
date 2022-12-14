import sqlite3
import json

from models import Post, Category, Tag, User,Reaction


def get_all_posts():
    # Open a connection to the database
    with sqlite3.connect("./rare.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
        """
        SELECT
            p.id,
            p.user_id,
            p.category_id ,
            p.title ,
            p.publication_date ,
            p.image_url ,
            p.content ,
            p.approved,
            c.label,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            r.id reaction_id,
            r.emoji,
            t.id tag_id,
            t.label tag_label
        FROM Posts p
        JOIN Categories c
            ON c.id = p.category_id
        JOIN Users u
            ON u.id = p.user_id
        JOIN PostReactions pr
            ON p.id = pr.post_id
        JOIN Reactions r
            ON pr.reaction_id = r.id
        JOIN PostTags pt
            ON p.id = pt.post_id
        JOIN Tags t
            ON pt.tag_id = t.id
        """
        )

        # Initialize an empty list to hold all post representations
        posts = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an post instance from the current row
            post = Post(
                row["id"],
                row["user_id"],
                row["category_id"],
                row["title"],
                row["publication_date"],
                row["image_url"],
                row["content"],
                row["approved"],
            )
            user = User(
                row["user_id"],
                row["first_name"],
                row["last_name"],
                row["email"],
                row["bio"],
                row["username"],
                row["password"],
                row["profile_image_url"],
                row["created_on"],
                row["active"],
            )
            category = Category(
                row["category_id"],
                row["label"]
            )
            tag = Tag(
                row["tag_id"],
                row["tag_label"]
            )
            reaction = Reaction(
                row ["reaction_id"],
                row ["emoji"]
            )
            post.user = user.__dict__
            post.category = category.__dict__
            post.tag = tag.__dict__
            post.reaction= reaction.__dict__

            # Add the dictionary representation of the post to the list
            posts.append(post.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(posts)


def get_single_post(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            p.id,
            p.user_id,
            p.category_id ,
            p.title ,
            p.publication_date ,
            p.image_url ,
            p.content ,
            p.approved,
            c.label,
            u.first_name,
            u.last_name,
            u.email,
            u.bio,
            u.username,
            u.password,
            u.profile_image_url,
            u.created_on,
            u.active,
            r.emoji,
            t.label tag_label
        FROM Posts p
        JOIN Categories c
            ON c.id = p.category_id
        JOIN Users u
            ON u.id = p.user_id
        JOIN PostReactions pr
            ON p.id = pr.post_id
        JOIN Reactions r
            ON pr.reaction_id = r.id
        JOIN PostTags pt
            ON p.id = pt.post_id
        JOIN Tags t
            ON pt.tag_id = t.id
        WHERE p.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an post instance from the current row
        post = Post(
            data["id"],
            data["user_id"],
            data["category_id"],
            data["title"],
            data["publication_date"],
            data["image_url"],
            data["content"],
            data["approved"],
        )
        user = User(
            data["user_id"],
            data["first_name"],
            data["last_name"],
            data["email"],
            data["bio"],
            data["username"],
            data["password"],
            data["profile_image_url"],
            data["created_on"],
            data["active"],
        )
        category = Category(
            data["category_id"],
            data["label"]
            )
        tag = Tag(
            data["tag_id"],
            data["label"]
        )
        
        post.user = user.__dict__
        post.category = category.__dict__
        post.tag = tag.__dict__


        return json.dumps(post.__dict__)


def create_post(new_post):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO Post
            ( user_id, category_id, title, publication_date, image_url, content, approved )
        VALUES
            ( ?, ?, ?, ?, ?, ?, ?);
        """,
            (
                new_post["user_id"],
                new_post["category_id"],
                new_post["title"],
                new_post["publication_date"],
                new_post["image_url"],
                new_post["content"],
                new_post["approved"],
            ),
        )

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the post dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post["id"] = id

    return new_post


def delete_post(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM Posts
        WHERE id = ?
        """,
            (id,),
        )


def update_post(id, new_post):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Post
            SET
                user_id = ?,
                category_id = ?,
                title = ?,
                publication_date = ?,
                image_url = ?,
                content = ?,
                approved = ?
        WHERE id = ?
        """,
            (
                new_post["user_id"],
                new_post["category_id"],
                new_post["title"],
                new_post["publication_date"],
                new_post["image_url"],
                new_post["content"],
                new_post["approved"],
                id,
            ),
        )

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True
