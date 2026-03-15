import sqlite3
import random
import time
import urllib.parse
from duckduckgo_search import DDGS

categories_map = {
    'biryani': ['Hyderabadi Chicken Biryani', 'Hyderabadi Mutton Biryani', 'Lucknowi Dum Biryani', 'Kolkata Biryani', 'Paneer Biryani', 'Veg Dum Biryani', 'Egg Biryani'],
    'thali': ['North Indian Royal Thali', 'South Indian Traditional Thali', 'Gujarati Thali', 'Rajasthani Thali', 'Maharashtrian Thali', 'Punjabi Special Thali'],
    'sweets': ['Gulab Jamun', 'Rasgulla', 'Kaju Katli', 'Jalebi', 'Rasmalai', 'Motichoor Laddu', 'Mysore Pak'],
    'snacks': ['Samosa', 'Aloo Tikki Chaat', 'Pani Puri', 'Dahi Puri', 'Pav Bhaji', 'Vada Pav', 'Masala Corn', 'Bread Pakora'],
    'punjabi': ['Butter Chicken', 'Amritsari Kulcha', 'Sarson da Saag with Makki di Roti', 'Paneer Butter Masala', 'Dal Makhani', 'Chole Bhature', 'Tandoori Chicken', 'Paneer Tikka', 'Chicken Tikka', 'Sweet Lassi'],
    'andhra': ['Andhra Chicken Curry', 'Gongura Mutton', 'Andhra Fish Fry', 'Kodi Vepudu', 'Andhra Prawn Curry', 'Royyala Iguru', 'Andhra Spicy Biryani', 'Tomato Pappu', 'Andhra Rasam', 'Gutti Vankaya Curry'],
    'tamilnadu': ['Chettinad Chicken', 'Chicken Chettinad Biryani', 'Karaikudi Mutton Curry', 'Idli with Sambar', 'Dosa with Chutney', 'Pongal', 'Lemon Rice', 'Tamarind Rice', 'Medu Vada', 'Filter Coffee'],
    'kerala': ['Kerala Fish Curry', 'Malabar Chicken Biryani', 'Appam with Vegetable Stew', 'Kerala Prawn Curry', 'Kerala Beef Fry', 'Kerala Parotta with Curry', 'Avial', 'Kerala Sadya', 'Banana Chips', 'Payasam'],
    'maharashtrian': ['Misal Pav', 'Puran Poli', 'Sabudana Khichdi', 'Kanda Bhaji', 'Thalipeeth', 'Kolhapuri Chicken', 'Kolhapuri Mutton', 'Modak'],
    'rajasthani': ['Dal Baati Churma', 'Gatte ki Sabzi', 'Laal Maas', 'Ker Sangri', 'Rajasthani Kadhi', 'Bajra Roti with Garlic Chutney', 'Mawa Kachori', 'Mirchi Vada', 'Ghewar'],
    'chinese': ['Veg Hakka Noodles', 'Chicken Hakka Noodles', 'Schezwan Fried Rice', 'Chicken Manchurian', 'Veg Manchurian', 'Spring Rolls', 'Hot and Sour Soup', 'Chili Chicken', 'Garlic Noodles'],
    'thai': ['Pad Thai Noodles', 'Thai Green Curry', 'Thai Red Curry', 'Thai Basil Chicken', 'Mango Sticky Rice', 'Thai Fried Rice', 'Tom Yum Soup', 'Pineapple Fried Rice'],
    'latinamerican': ['Mexican Burrito Bowl', 'Chicken Quesadilla', 'Beef Tacos', 'Veg Enchiladas', 'Nachos Supreme', 'Mexican Street Corn', 'Chimichanga'],
    'african': ['Jollof Rice', 'Chicken Yassa', 'Bunny Chow', 'Moroccan Chicken Tagine', 'Couscous Royal', 'Peri Peri Chicken', 'Ethiopian Doro Wat'],
    'european': ['Spaghetti Carbonara', 'Mushroom Risotto', 'Chicken Alfredo Pasta', 'Fish and Chips', 'Grilled Lamb Steak', 'Lasagna', 'Bruschetta', 'French Onion Soup']
}

conn = sqlite3.connect('instance/site.db')
cursor = conn.cursor()

cursor.execute('SELECT name FROM menu_item')
existing = set([row[0] for row in cursor.fetchall()])

jinja_block_menu = ""
jinja_block_cart = ""

used_urls = set()
ddgs = DDGS()

def fetch_image(query):
    try:
        results = ddgs.images(f"{query} food high quality site:unsplash.com OR site:pexels.com", max_results=3)
        for r in results:
            if r['image'] not in used_urls:
                used_urls.add(r['image'])
                return r['image']
    except Exception as e:
        pass
    
    # Fallback if rate limited or none found
    time.sleep(1)
    return f"https://loremflickr.com/800/600/{urllib.parse.quote(query)},food/all"

for cat, items in categories_map.items():
    print(f"Processing {cat} with {len(items)} items")
    for item in items:
        image_url = fetch_image(item)
        
        jinja_block_menu += f"            {{% elif item.name == '{item}' %}}{{% set image_url = \"{image_url}\" %}}\n"
        jinja_block_cart += f"            {{% elif item.menu_item.name == '{item}' %}}{{% set image_url = \"{image_url}\" %}}\n"
        
        if item not in existing:
            price = round(random.uniform(5.99, 18.99), 2)
            desc = f"Delicious and authentic {item} prepared with the finest ingredients."
            cursor.execute("INSERT INTO menu_item (name, price, description, category) VALUES (?, ?, ?, ?)",
                           (item, price, desc, cat))
        time.sleep(0.5)

conn.commit()
conn.close()

with open('jinja_ext_menu.txt', 'w', encoding='utf-8') as f:
    f.write(jinja_block_menu)

with open('jinja_ext_cart.txt', 'w', encoding='utf-8') as f:
    f.write(jinja_block_cart)
print("Done writing mapping blocks and inserting DB rows.")
