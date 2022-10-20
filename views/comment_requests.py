import sqlite3
import json
from models import Comment
from models import Post


def get_all_comments():
    # Open a connection to the database
    with sqlite3.connect("./rare.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content,
            p.title title,
            p.publication_date publication_date,
            p.image_url image_url,
            p.content content,
            p.approved approved
        FROM comments c
        JOIN Posts p
            ON p.id = p.post_id
        """
        )

        # Initialize an empty list to hold all comment representations
        comments = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an comment instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # comment class above.
            comment = Comment(
                row["id"], row["author_id"], row["post_id"], row["content"]
            )

            post = Post(
                row["id"],
                row["title"],
                row["publication_date"],
                row["image_url"],
                row["content"],
                row["approved"],
            )

            comment.post = post.__dict__

            comments.append(comment.__dict__)

        # Use `json` package to properly serialize list as JSON
        return json.dumps(comments)


def get_single_comment(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            c.id,
            c.author_id,
            c.post_id,
            c.content,
            p.title title,
            p.publication_date publication_date,
            p.image_url image_url,
            p.content content,
            p.approved approved
        FROM comments c
        JOIN Posts p
            ON p.id = p.post_id
        WHERE c.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an comment instance from the current row
        comment = Comment(
            data["id"], data["author_id"], data["post_id"], data["content"]
        )
        
        post = Post(
                data["id"],
                data["title"],
                data["publication_date"],
                data["image_url"],
                data["content"],
                data["approved"],
            )
        
        comment.post = post.__dict__

        return json.dumps(comment.__dict__)


def create_comment(new_comment):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        INSERT INTO comments
            ( author_id, post_id, content )
        VALUES
            ( ?, ?, ?);
        """,
            (new_comment["author_id"], new_comment["post_id"], new_comment["content"]),
        )

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the comment dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment["id"] = id

    return new_comment


def delete_comment(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        DELETE FROM comments
        WHERE id = ?
        """,
            (id,),
        )


def update_comment(id, updated_comment):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        UPDATE Comments
            SET
                author_id = ?
                post_id = ?
                content = ?
        WHERE id = ?
        """,
            (
                updated_comment["author_id"],
                updated_comment["post_id"],
                updated_comment["content"],
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
