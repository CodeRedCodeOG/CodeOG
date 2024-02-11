import psycopg2

# Set connection parameters
host="localhost"
port= "1109"
database="suggestions"
user="postgres"
password="Kimlien**2512"

try:
    # Connect to the PostgreSQL server
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    
    # Create a cursor object using the connection
    cursor = connection.cursor()
    
    # Example query to select data from a table
    query = "SELECT * FROM summertravel;"
    
    # Execute the query
    cursor.execute(query)
    
    # Fetch all rows from the result set
    rows = cursor.fetchall()
    
    # Process the fetched data
    for row in rows:
        print(row)  # Print each row
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    
except psycopg2.Error as e:
    print("Error: Could not connect to PostgreSQL database:", e)