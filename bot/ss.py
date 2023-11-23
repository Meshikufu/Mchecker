import time
import requests
import re
from bs4 import BeautifulSoup
import sqlite3

from modules.SocketClient import Schat
import save.controlPanel

ssTest = False

def initialize_database():
    conn = sqlite3.connect('filtered_items.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS filtered_items (id TEXT PRIMARY KEY)')
    conn.commit()
    conn.close()

def insert_filtered_item(item_id):
    conn = sqlite3.connect('filtered_items.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM filtered_items WHERE id = ?', (item_id,))
    existing_item = cursor.fetchone()
    if not existing_item:
        cursor.execute('INSERT INTO filtered_items (id) VALUES (?)', (item_id,))
        conn.commit()
    conn.close()

def SS_OfferChecker():
    initialize_database()
    print("ssBot Started")
    time.sleep(15*60)

    # List of filter names
    filter_names = save.controlPanel.ss_filter_names

    while True:
        if ssTest:
            html_content = save.controlPanel.html_content
        elif ssTest is False:
            url = save.controlPanel.ssurl
            response = requests.get(url)
            html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')
        row_selector = 'tr[id^="tr_"]'
        rows = soup.select(row_selector)

        all_items = []

        for row in rows:
            item_id = row['id'][3:]
            text_element = row.select_one('div.d1 a.am')
            item_text = text_element.get_text(strip=True).lower() if text_element else 'Text not available'
            price_element = row.select_one('td.msga2-o.pp6')
            item_price_str = price_element.get_text(strip=True) if price_element else 'Price not available'
            item_price = int(re.sub(r'\D', '', item_price_str)) if item_price_str != 'Price not available' else None
            item_name = f'Item_{item_id}'

            all_items.append({
                'id': item_id,
                'text': item_text,
                'price': item_price,
            })

        existing_ids = set()
        conn = sqlite3.connect('filtered_items.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM filtered_items')
        existing_ids.update(row[0] for row in cursor.fetchall())
        conn.close()

        new_filtered_items = []
        filtered_items_already_in_db = []

        for item_info in all_items:
            if item_info['id'] in existing_ids:
                filtered_items_already_in_db.append(item_info)
                continue

            for filteredName in filter_names:
                if filteredName in item_info['text'] and item_info['price'] is not None and item_info['price'] < 500:
                    new_filtered_items.append(item_info)

                    # Insert the filtered item ID into the database
                    insert_filtered_item(item_info['id'])

        #print("\nNew Filtered Items:")
        for item_info in new_filtered_items:
            print(f"{item_info['id']}: {filteredName} - Price: {item_info['price']}")
            Schat(f"$tts New seller: rtx {filteredName}, price: {item_info['price']} euro")
            Schat(f"New seller: rtx {filteredName}, price: {item_info['price']} euro")
            Schat("change_icon_alert")

        #print("\nFiltered Items Already in Database:")
        for item_info in filtered_items_already_in_db:
            print(f"{item_info['id']}: {item_info['text']} - Price: {item_info['price']}")
        
        time.sleep(60*60*2)
        print("Scanning SS")