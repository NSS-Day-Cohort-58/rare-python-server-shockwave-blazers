import sqlite3
import json
from models import Category

def get_all_categories():
    # Open a connection to the database
    with sqlite3.connect("./rare.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        """)

        # Initialize an empty list to hold all order representations
        categories = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an order instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # order class above.
            category = Category(row['id'], row['label'])


            categories.append(category.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(categories)

def get_single_category(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            c.id,
            c.label
        FROM categories c
        WHERE c.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an category instance from the current row
        category = Category(data['id'], data['label'])

        return json.dumps(category.__dict__)

def create_category(new_category):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO categories
            ( label )
        VALUES
            ( ? )
        """, (new_category['label'], ))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the category dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_category['id'] = id


    return new_category

def delete_category(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM categories
        WHERE id = ?
        """, (id, ))
        
def update_category(id, new_category):
    with sqlite3.connect("./rare.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE categories
            SET
                label = ?
        WHERE id = ?
        """, (new_category['label'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True