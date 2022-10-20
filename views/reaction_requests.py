import sqlite3
import json
from models import Reaction


def get_all_reactions():
    with sqlite3.connect("./rare.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            r.id,
            r.emoji
        FROM Reaction r
        """)
        reactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            reaction = Reaction(row['id'], row['emoji'])

            reactions.append(reaction.__dict__)

        return json.dumps(reactions)


def get_single_reaction(id):
    with sqlite3.connect("./rare.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            r.id,
            r.emoji
        FROM Reaction r
        WHERE r.id = ?
        """, (id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an post instance from the current row
        reaction = Reaction(data['id'], data['emoji'])

        return reaction.__dict__
