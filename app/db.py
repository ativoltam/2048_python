import sqlite3, pickle


# def create_db():
#     conn = sqlite3.connect('scores.db')
#     c = conn.cursor()
#     c.execute("CREATE TABLE high_scores (id text, game text)")
#     conn.commit()
#     conn.close()

# def create_db():
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     c.execute("CREATE TABLE high_scores (id text, game text)")
#     conn.commit()
#     conn.close()


def save_to_scores_db(u_name, c_score):
    conn = sqlite3.connect('scores.db')
    c = conn.cursor()
    c.execute("INSERT INTO high_scores VALUES(?, ?)", (u_name, c_score))
    conn.commit()
    conn.close()


# def save_games_db(uId, b):
#     conn = sqlite3.connect('scores.db')
#     c = conn.cursor()
#     c.execute("INSERT INTO game_list VALUES(?, ?)", (uId, b))
#     conn.commit()
#     conn.close()


def get_game(uId):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT game FROM game_list WHERE id=?", (uId,))
    gam = c.fetchone()
    b = pickle.loads(gam[0])
    conn.commit()
    conn.close()
    print(b)
    return b
