import sqlite3

conn = sqlite3.connect('LU_Bot.db')
print("connected")

conn.execute('''
      CREATE TABLE IF NOT EXISTS feedback (
          FIRST_NAME TEXT NOT NULL,
          LAST_NAME TEXT NOT NULL,
          FEEDBACK TEXT NOT NULL
      );
  ''')
conn.commit()

print("connected2")

class Repo:

  # @staticmethod
  # def initDb():
  #   conn.execute('''
  #       CREATE TABLE IF NOT EXISTS feedback (
  #           FIRST_NAME TEXT NOT NULL,
  #           LAST_NAME TEXT NOT NULL,
  #           FEEDBACK TEXT NOT NULL
  #       );
  #   ''')
  #   conn.commit()

  @staticmethod
  def insert(first_name, last_name, feedback):
    conn.execute('''
      INSERT INTO feedback (FIRST_NAME, LAST_NAME, FEEDBACK) VALUES (?, ?, ?);
    ''', (first_name, last_name, feedback))
    conn.commit()

  @staticmethod
  def select():

    cur = conn.cursor()

    cur.execute('''
      SELECT * FROM feedback;
    ''')

    rows = cur.fetchall()

    return str(rows).strip('[]') if len(rows) > 0 else "No records found"