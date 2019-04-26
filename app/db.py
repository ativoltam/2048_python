import sqlite3


def create_db():
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("CREATE TABLE high_scores (name text, score integer)")
    conn.commit()
    conn.close()


def save_to_db(u_name, c_score):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("INSERT INTO high_scores VALUES(?, ?)", (u_name, c_score))
    conn.commit()
    conn.close()
