import sqlite3

conn = sqlite3.connect('twitter.db')
c = conn.cursor()
c.execute('''CREATE TABLE tweets
    (tweetText text, user text, followers integer, date text, location text)''')
conn.commit()
conn.close()