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
            r.emoji,
        FROM Reaction r
        """)
        reactions = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            reaction = Reaction(row['id'], row['emoji'])

            reactions.append(reaction.__dict__)

        return json.dumps(reactions)