import psycopg
from sentence_transformers import SentenceTransformer
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from pgvector.psycopg import register_vector
import os, sys


conn = psycopg.connect(dbname="postgres", autocommit=True)
model = SentenceTransformer('clip-ViT-B-32')

def seed():
    print("seeding the database")
    conn.execute('CREATE EXTENSION IF NOT EXISTS vector')
    register_vector(conn)
    conn.execute('DROP TABLE IF EXISTS images')
    conn.execute('CREATE TABLE images (id bigserial PRIMARY KEY, path varchar(64), embedding vector(512))')
    cur = conn.cursor()
    cur.execute('create extension if not exists vector with schema public')

    images = os.listdir("./mixed_wiki")
    for f in images:
        file = f'./mixed_wiki/{f}'
        img_emb = model.encode(Image.open(file))
        cur.execute('INSERT INTO images (embedding, path) VALUES (%s,%s)', (img_emb.tolist(), file))
    conn.commit()


def search():    
    # query_string = "a white bike in front of a red brick wall"
    query_string = "van gogh paintings" #input("Enter image query: ")
    text_emb = model.encode(query_string)

    cur = conn.cursor()
    cur.execute("""
                SELECT id, path, embedding <-> %s AS distance 
                FROM images 
                WHERE embedding <-> %s < 15
                ORDER BY distance
                LIMIT 3
                """, 
                (
                    str(text_emb.tolist())
                    ,str(text_emb.tolist())
                )
        )

    rows = cur.fetchall()
    for row in rows:
        print(row[1], rows[2])
        show(row[1], rows[2])

    
def show(path, distance):
    plt.title(f'{path} {distance}')
    image = mpimg.imread(path)
    plt.imshow(image)
    plt.show()

if __name__ == '__main__':

    args = sys.argv

    # seed()

    search()
