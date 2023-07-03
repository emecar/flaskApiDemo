from flask import Flask, render_template, jsonify, request
import psycopg2

app = Flask(__name__)
# url = "postgres://uwyfoily:Ep151WIg59xUW2SlfzBAtGGVx1k2KJZ-@rajje.db.elephantsql.com/uwyfoily"
url = "postgres://ehwuexwg:jJde5hY4KKV9aSyde4NsGDI-NC0DPgsR@mahmud.db.elephantsql.com/ehwuexwg"

## API Route endpoint for retrieving all the items in the PostgreSQL table
@app.route("/")
#Route Handler
def root():
    conn = psycopg2.connect(url)
    cur = conn.cursor()
    cur.execute("SELECT * FROM veggies")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # rows = [(1, 'orange', 'carrot'), (2, 'yellow', 'onion'), (3, 'green', 'zucchini'), (4, 'yellow', 'squash'), (5, 'red', 'pepper'), (6, 'red', 'onion')]
    items = []
    for row in rows:
        id = row[0]
        name = row[1]
        color = row[2]
        # Create a dictionary representing each user
        fruit = {
            'id': id,
            'name': name,
            'color': color,
        }
        items.append(fruit)

    # Return the user data as a JSON response
    return jsonify(items)
   
# API endpoint for adding a single item to the PostgreSQL database
@app.route('/add_item', methods=['POST'])
def add_item():
    # Retrieve the item details from the request JSON
    item = request.get_json()
    color = item['color']
    name = item['name']
    
    conn = psycopg2.connect(url) # Establish a connection to the PostgreSQL database
    cur = conn.cursor() # Create a cursor object to interact with the database

    # Get the current maximum ID from the table
    cur.execute("SELECT MAX(id) FROM veggies")
    max_id = cur.fetchone()[0]

    # Increment the ID and insert the item into the database
    next_id = max_id + 1 if max_id else 1
    query = f"INSERT INTO veggies (id, color, name) VALUES ({next_id}, '{color}', '{name}')"
    cur.execute(query)

    # Commit the transaction
    conn.commit()

    # Close the cursor and the connection
    cur.close()
    conn.close()

    # Return a success message
    return jsonify({'message': 'Item added successfully'})
 
# API endpoint for adding multiple items to the PostgreSQL database. The endpoint method ends with an 's'
@app.route('/add_items', methods=['POST'])
def add_items():
    # Retrieve the item details from the request JSON
    items = request.get_json()
    my_list = []
    for item in items:
        color = item['color']
        name = item['name']
        my_list.append((color, name))
    print(my_list)
    # return my_list
    conn = psycopg2.connect(url) # Establish a connection to the PostgreSQL database
    cur = conn.cursor() # Create a cursor object to interact with the database
    
    for tup in my_list:
        # Get the current maximum ID from the table
        cur.execute("SELECT MAX(id) FROM veggies")
        max_id = cur.fetchone()[0]
        
        # Increment the ID and insert the item into the database
        next_id = max_id + 1 if max_id else 1
        color = tup[0]
        name = tup[1]
        query = f"INSERT INTO veggies (id, color, name) VALUES ({next_id}, '{color}', '{name}')"
        cur.execute(query)
	    #Commit the transaction
        conn.commit()

    # Close the cursor and the connection
    cur.close()
    conn.close()

    #Return a success message
    return jsonify({'message': 'Item added successfully'})
    
if __name__ == '__main__':
    app.run()
 

# @app.route("/user")
# #Route Handler
# def user():
#     people = [
#         {"name": "Carter"},
#         {"name": "Tony"}
#     ]
#     people_string = ""
    
#     for person in people:
#          people_string += f"<h1>{person['name']}</h1>"
         
#     return people_string

