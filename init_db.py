import psycopg2
from main import POSTGRES
# This program is for intiating the postgres database

# create connection using details in POSTGRES in main.py
conn = psycopg2.connect(
    host=POSTGRES['host'],
    database=POSTGRES['db'],
    user=POSTGRES['user'],
    password=POSTGRES['pw']
)

cur = conn.cursor()
# create the required tables
cur.execute('DROP TABLE IF EXISTS face_image;')
cur.execute('DROP TABLE IF EXISTS image_data;')
cur.execute('CREATE TABLE face_image(id serial PRIMARY KEY,face_encoding BYTEA NOT NULL);')
cur.execute('CREATE TABLE image_data( id serial PRIMARY KEY, name varchar(50) NOT NULL, version numeric, date_created date, location varchar(50));')
# commit changes and close connection 
conn.commit()
cur.close()
conn.close()

