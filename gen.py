import datetime
from faker import Faker
import random
import csv, os
from llama_index.embeddings.openai import OpenAIEmbedding
import pandas as pd
from numpy.random import choice
from tqdm import tqdm

fake = Faker()

dimensions = 2048
config = {
    "model": 'text-embedding-3-large',
    "dimensions": int(dimensions) if dimensions is not None else None,
}
embed_model = OpenAIEmbedding(**config)


# Generate fake users
def generate_fake_users(n=10):
    data = {
        "ID": [fake.uuid4() for _ in range(n)],
        "Name": [fake.name() for _ in range(n)],
        "Phone": [fake.phone_number() for _ in range(n)],
        "Address": [fake.street_address() for _ in range(n)],
        "City": [fake.city() for _ in range(n)],
        "State": [fake.state() for _ in range(n)],
        "Zip": [fake.zipcode() for _ in range(n)],
    }
    return pd.DataFrame(data)

# Generate fake products
def generate_fake_retail_products(n=10):
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Kitchen', 'Toys & Games', 'Sports & Outdoors', 'Health & Beauty']
    product_types = {
        'Electronics': ['Smartphone', 'Laptop', 'Headphones', 'Camera', 'Smartwatch'],
        'Clothing': ['T-shirt', 'Jeans', 'Sneakers', 'Jacket', 'Dress'],
        'Books': ['Novel', 'Biography', 'Textbook', 'Cookbook', 'Magazine'],
        'Home & Kitchen': ['Blender', 'Coffee Maker', 'Vacuum Cleaner', 'Mixer', 'Microwave'],
        'Toys & Games': ['Board Game', 'Action Figure', 'Doll', 'Puzzle', 'Lego Set'],
        'Sports & Outdoors': ['Tent', 'Backpack', 'Sleeping Bag', 'Yoga Mat', 'Bicycle'],
        'Health & Beauty': ['Shampoo', 'Perfume', 'Lipstick', 'Face Cream', 'Toothbrush']
    }
    
    data = {
        "ID": [fake.uuid4() for _ in range(n)],
        "Name": [],
        "Description": [],
        "embedding":[]
    }
    
    p = tqdm(range(n), "products")
    for _ in range(n):
        category = random.choice(categories)
        product_type = random.choice(product_types[category])
        product_name = f"{fake.word().capitalize()} {product_type}"
        description = f"A high-quality {product_type.lower()} perfect for {category.lower()} enthusiasts."
        data["Name"].append(product_name)
        data["Description"].append(description)
        data["embedding"].append(embed_model.get_text_embedding(description))
        p.update(1)
        
    return pd.DataFrame(data)

# Generate fake purchases
def generate_fake_purchases(users, products, n=10):
    data = {
        "user_id": [],
        "product_id": [],
        "purchase_date": [],
        "quantity": []
    }
    p = tqdm(range(n), "purchases")
    for _ in range(n):
        user = random.choice(users['ID'].tolist())
        product = random.choice(products['ID'].tolist())
        data["user_id"].append(user)
        data["product_id"].append(product)
        data["purchase_date"].append(fake.date_time_this_year())
        data["quantity"].append(random.randint(1, 5))
        p.update(1)
    
    return pd.DataFrame(data)

# Generate fake clickstream events
def generate_fake_clickstream_events(users, products, n=50):
    event_types = ['click', 'view', 'save', 'purchase']
    ec = choice(a=event_types, size=n, p=[.45, .3, .2, .05])
    
    data = {
        "user_id": [],
        "product_id": [],
        "timestamp": [],
        "event_type": [],
        "duration": []
    }
    
    p = tqdm(range(n), "clicks")
    for i in range(n):
        user = random.choice(users['ID'].tolist())
        product = random.choice(products['ID'].tolist())
        data["user_id"].append(user)
        data["product_id"].append(product)
        data["timestamp"].append(fake.date_time_this_year())
        data["event_type"].append(ec[i])
        data["duration"].append(random.choice(range(5,10000)))
        p.update(1)
    
    return pd.DataFrame(data)

# Generate fake data
fake_users = generate_fake_users(100)
fake_products = generate_fake_retail_products(100)
fake_purchases = generate_fake_purchases(fake_users, fake_products, 10000)
fake_clickstream_events = generate_fake_clickstream_events(fake_users, fake_products, 50000)

# Export to Parquet
fake_users.to_parquet('fake_users.parquet', engine='pyarrow', index=False)
fake_products.to_parquet('fake_products.parquet', engine='pyarrow', index=False)
fake_purchases.to_parquet('fake_purchases.parquet', engine='pyarrow', index=False)
fake_clickstream_events.to_parquet('fake_clickstream_events.parquet', engine='pyarrow', index=False)

print("Parquet files have been created for Users, Products, Purchases, and Clickstream Events.")
