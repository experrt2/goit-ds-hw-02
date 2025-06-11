
from faker import Faker
from random import randint
import sqlite3

NUMBER_USERS = 20
NUMBER_DESCRIPTIONS = 30
NUMBER_TASKS = 20
NUMBER_STATUS = 3

def generate_fake_data(number_users, number_descriptions, number_tasks) -> tuple():
    fake_users = []
    fake_tasks = []
    possible_tasks = ['Change request', 'Bug', 'Testing', 'Technical debt', 'Research']
    possible_statuses = ['new', 'in progress', 'completed']

    fake_data = Faker()

    for _ in range(number_users):
        fake_users.append({"fullname": fake_data.name(), "email": fake_data.email()})

    for _ in range(number_tasks):
        fake_tasks.append({"title": fake_data.random_element(possible_tasks), "description": fake_data.paragraph()})

    return fake_users, fake_tasks, possible_statuses

def prepare_data(users, tasks, statuses) -> tuple():
    for_users = []
    for user in users:
        for_users.append((user['fullname'], user['email']))

    for_statuses = []
    for status in statuses:
        for_statuses.append((status, ))

    for_tasks = []
    for task in tasks:
        for_tasks.append((task['title'], task['description'], randint(1, NUMBER_STATUS), randint(1, NUMBER_USERS) ))

    return for_users, for_statuses, for_tasks

def insert_data_to_db(users, statuses, tasks) -> None:
    with sqlite3.connect('tasks.db') as con:
        cur = con.cursor()

        sql_to_users = """INSERT INTO users(fullname, email) VALUES (?, ?)"""
        cur.executemany(sql_to_users, users)

        sql_to_statuses = """INSERT INTO statuses(name) VALUES (?)"""
        cur.executemany(sql_to_statuses, statuses)
        #
        sql_to_tasks = """INSERT INTO tasks(title, description, status_id, user_id) VALUES (?, ?, ?, ?)"""
        cur.executemany(sql_to_tasks, tasks)

        con.commit()

if __name__ == "__main__":
    users, tasks, statuses = generate_fake_data(NUMBER_USERS, NUMBER_DESCRIPTIONS, NUMBER_TASKS)
    prepared_users, prepared_statuses, prepared_tasks = prepare_data(users, tasks, statuses)
    insert_data_to_db(prepared_users, prepared_statuses, prepared_tasks)
