import os
import json
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')
interacted_users = set()


def create_interacted_users_table():
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS interacted_users (
                        user_id TEXT PRIMARY KEY
                    )
                    """
                )
        print('Table interacted_users created successfully.')
    except psycopg2.Error as e:
        print(f'Failed to create table interacted_users: {e}')

def load_interacted_users_from_database():
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT user_id FROM interacted_users")
                rows = cur.fetchall()
                return set(user_id[0] for user_id in rows)
    except psycopg2.Error as e:
        print(f'Error loading interacted_users from the database. Starting with an empty set. {e}')
        return set()

create_interacted_users_table()
interacted_users = load_interacted_users_from_database()

def save_interacted_users():
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM interacted_users")  # Clear the table before saving new data

                for user_id in interacted_users:
                    try:
                        cur.execute("INSERT INTO interacted_users (user_id) VALUES (%s)", (user_id,))
                    except psycopg2.Error as e:
                        conn.rollback()  # Roll back the transaction in case of error
                        print(f"Failed to insert user_id {user_id}: {e}")

                conn.commit()  # Commit the transaction after all data is inserted

        print('Data successfully saved to the database.')

    except psycopg2.Error as e:
        print(f'Failed to save interacted_users data to the database: {e}')

