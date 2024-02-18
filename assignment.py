import sqlite3
import pandas as pd
import csv

# Connect to the database
conn = sqlite3.connect('mydatabase.db')

# Create the tables based on the chart
conn.execute('''
CREATE TABLE IF NOT EXISTS Sales (
    sales_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES Customer(customer_id)
)''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Customer (
    customer_id INTEGER PRIMARY KEY,
    age INTEGER
)''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY,
    sales_id INTEGER,
    item_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (sales_id) REFERENCES Sales(sales_id),
    FOREIGN KEY (item_id) REFERENCES Items(item_id)
)''')

conn.execute('''
CREATE TABLE IF NOT EXISTS Items (
    item_id INTEGER PRIMARY KEY,
    item_name TEXT
)''')

# Save the changes
conn.commit()





# Add data to the Customer table
conn.execute("INSERT INTO Customer (customer_id, age) VALUES (1, 35)")
conn.execute("INSERT INTO Customer (customer_id, age) VALUES (2, 28)")
conn.execute("INSERT INTO Customer (customer_id, age) VALUES (3, 42)")

# Add data to the Sales table, considering multiple purchases of Item X by Customer 1
conn.execute("INSERT INTO Sales (sales_id, customer_id) VALUES (1, 1)")
conn.execute("INSERT INTO Sales (sales_id, customer_id) VALUES (2, 1)")  # Additional sale for Customer 1
conn.execute("INSERT INTO Sales (sales_id, customer_id) VALUES (3, 2)")
conn.execute("INSERT INTO Sales (sales_id, customer_id) VALUES (4, 3)")
conn.execute("INSERT INTO Sales (sales_id, customer_id) VALUES (5, 3)")  # Additional sale for Customer 3

# Add data to the Items table, ensuring quantities reflect multiple purchases
conn.execute("INSERT INTO Items (item_id, item_name) VALUES (1, 'Item X')")   #adjusted for Customer 1
conn.execute("INSERT INTO Items (item_id, item_name) VALUES (2, 'Item Y')")
conn.execute("INSERT INTO Items (item_id, item_name) VALUES (3, 'Item Z')")  # adjusted for Customer 3
conn.execute("INSERT INTO Items (item_id, item_name) VALUES (4, 'Item X')")  # Additional Item X for Customer 1
conn.execute("INSERT INTO Items (item_id, item_name) VALUES (5, 'Item Z')")  # Additional Item Z for Customer 3

# Add data to the Orders table, linking sales and items appropriately
conn.execute("INSERT INTO Orders (order_id, sales_id, item_id, quantity ) VALUES (1, 1, 1, 5)")
conn.execute("INSERT INTO Orders (order_id, sales_id, item_id, quantity ) VALUES (2, 2, 4, 1)")  # Order for additional Item X
conn.execute("INSERT INTO Orders (order_id, sales_id, item_id, quantity ) VALUES (3, 3, 2, 1)")
conn.execute("INSERT INTO Orders (order_id, sales_id, item_id, quantity ) VALUES (4, 4, 3, 5)")
conn.execute("INSERT INTO Orders (order_id, sales_id, item_id, quantity ) VALUES (5, 5, 5, 1)")  

# Save the changes
conn.commit()


print ("sql solution" )
cursor = conn.cursor()
cursor.execute("""
SELECT c.customer_id, c.age, i.item_name, SUM(oi.quantity) AS total_quantity
FROM Customer c
JOIN Sales s ON c.customer_id = s.customer_id
JOIN Orders oi ON s.sales_id = oi.sales_id
JOIN Items i ON oi.item_id = i.item_id
WHERE c.age >= 18 AND c.age <= 35
GROUP BY c.customer_id, i.item_name;
""")

results = cursor.fetchall()
column_names = [desc[0] for desc in cursor.description]
# Process and print the results
with open("query_results_pure_sql.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=";")
    writer.writerow(column_names)
    writer.writerows(results)



for row in results:
    print(f"Customer ID: {row[0]}, Age: {row[1]}, Item Name: {row[2]}, Total Quantity: {row[3]}")



csvfile.close()

print("pandas solution ")
query = """
SELECT c.customer_id, c.age, i.item_name, SUM(oi.quantity) AS total_quantity
FROM Customer c
JOIN Sales s ON c.customer_id = s.customer_id
JOIN Orders oi ON s.sales_id = oi.sales_id
JOIN Items i ON oi.item_id = i.item_id
GROUP BY c.customer_id, i.item_name;
"""

# Read the results into a DataFrame
df = pd.read_sql(query, conn)

# Filter for customers aged 18-35
df_filtered = df[df['age'] >= 18][df['age'] <= 35]

# Print the results
print(df_filtered)

df_filtered.to_csv("query_results_panda_solution.csv", sep=";")

# Close connection
conn.close()