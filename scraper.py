import os
import requests
from bs4 import BeautifulSoup
import psycopg2


# Make a GET request to the website
url = "https://www.lucernefestival.ch/en/program/summer-festival-23"
res = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(res.text, "html.parser")

# Find all event blocks
events = soup.find_all("div", class_="event-content")  

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host = os.environ.get('POSTGRES_HOST'),
    database = os.environ.get('POSTGRES_DB'),
    user = os.environ.get('POSTGRES_USER'),
    password = os.environ.get('POSTGRES_PASSWORD'),
    port = os.environ.get('POSTGRES_PORT')
)

# Create a cursor object
cur = conn.cursor()

table_name = "events"

# Check if table exists
cur.execute(f"SELECT to_regclass('public.{table_name}')")
if not cur.fetchone()[0]:
    # If table does not exist, create it
    cur.execute(f""" CREATE TABLE { table_name } (event_id SERIAL PRIMARY KEY, 
                                                  date VARCHAR(255) NOT NULL, 
                                                  time VARCHAR(255) NOT NULL, 
                                                  location VARCHAR(255) NOT NULL,
                                                  title VARCHAR(255) NOT NULL, 
                                                  artists VARCHAR(255) NOT NULL, 
                                                  works VARCHAR(255) NOT NULL, 
                                                  image_link VARCHAR(512) NOT NULL) """)
    conn.commit()

# Loop through each event
for event in events:
    # Extract event details
    event_date_location = event.find("div", class_="cell xlarge-6 body-small").text.split("|")
    date = event_date_location[0].strip("\nDate and Venue\n")
    time = event_date_location[1].strip("\n\t\t\t\t\t\t\t\t")
    location = event_date_location[2].strip("\n")
    title = event.find("div", class_="body-small").text
    performers = event.find("p", class_="event-title h3").text
    works = event.find("div", class_="body-small").text
    image_link = 'https://www.lucernefestival.ch' + event.find("source")["srcset"]   
   
    # Insert data into the database
    sql = "INSERT INTO events (date, time, location, title, artists, works, image_link) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cur.execute(sql, (date, time, location, title, performers, works, image_link))

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()

print("Program executed successfully.")

