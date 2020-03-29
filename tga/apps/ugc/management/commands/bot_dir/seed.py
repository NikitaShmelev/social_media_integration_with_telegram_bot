import sqlite3
from datetime import datetime
from random import randint
from time import sleep
conn = sqlite3.connect(
    './tga/apps/ugc/management/commands/bot_dir/database.sqlite3')
cur = conn.cursor()
user_id = 465995986
for i in range(1):
    post_date = datetime.today().strftime('"%A, %d. %B %Y %H:%M:%S"')
    print(post_date)
    cur.execute('INSERT INTO POSTS (USER_ID,CREATED_AT,POST_TEXT,LOCATION,MEDIA,CREATOR_NAME,PUBLISHED) VALUES(?,?,?,?,?,?,?)',
                (
                    user_id, post_date, f'Text_{i}',
                    0, 0, f'Username_{i}', 0
                )
                )
    conn.commit()
    # sleep(1)
cur.close()
conn.close()
