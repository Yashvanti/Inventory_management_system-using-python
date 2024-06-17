# inventory_management.py

import tkinter as tk
from tkinter import messagebox
import pymongo

# Connect to MongoDB
CONNECTION_STRING = 'mongodb://localhost:27017'
client = pymongo.MongoClient(CONNECTION_STRING)
dbname = client['inventory_db']
collection_name = dbname["products"]

def create_product():
    # Get input from the user
    item_name = name_entry.get()
    category = category_entry.get()
    quantity = int(quantity_entry.get())
    price = float(price_entry.get())

    # Create a new product
    new_product = {"name": item_name, "category": category, "quantity": quantity, "price": price}

    # Insert the new product into the products collection
    result = collection_name.insert_one(new_product)

    # Display a confirmation message
    messagebox.showinfo("Success", f"Product created with id {result.inserted_id}")

def read_products():
    # Fetch all products from the products collection
    products_list.delete(0, tk.END)
    for product in collection_name.find():
        products_list.insert(tk.END, f"{product['name']} - Category: {product['category']} - Quantity: {product['quantity']} - Price: {product['price']}")
    products_list.select_set(0)
def update_product():
    selected_index = products_list.curselection()

    if len(selected_index) > 0:
        index = int(selected_index[0])
        product = products[index]

        new_name = product_name_input.get()
        new_category = product_category_input.get()
        new_quantity = int(product_quantity_input.get())
        new_price = float(product_price_input.get())

        filter_query = {"_id": product["_id"]}
        update_query = {
            "$set": {
                "name": new_name,
                "category": new_category,
                "quantity": new_quantity,
                "price": new_price
            }
        }

        collection_name.update_one(filter_query, update_query)

        read_products()
        clear_input_fields()
    else:
        messagebox.showerror("Error", "No product selected to update.")

def clear_input_fields():
    product_name_input.delete(0, "end")
    product_category_input.delete(0, "end")
    product_quantity_input.delete(0, "end")
    product_price_input.delete(0, "end")
def delete_product():
    # Get the selected product
    selected_index = products_list.curselection()
    if len(selected_index) > 0:
        index = selected_index[0]
        selected_product = products_list.get(index)
        # ... rest of the code for deleting the product
# Create the main window
root = tk.Tk()

# Set window title
root.title("Inventory Management")

# Create and position UI elements
name_label = tk.Label(root, text="Product name:")
name_label.grid(column=0, row=0, padx=5)
name_entry = tk.Entry(root)
name_entry.grid(column=1, row=0, padx=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(column=0, row=1, padx=5)
category_entry = tk.Entry(root)
category_entry.grid(column=1, row=1, padx=5)

quantity_label = tk.Label(root, text="Quantity:")
quantity_label.grid(column=0, row=2, padx=5)
quantity_entry = tk.Entry(root)
quantity_entry.grid(column=1, row=2, padx=5)

price_label = tk.Label(root, text="Price:")
price_label.grid(column=0, row=3, padx=5)
price_entry = tk.Entry(root)
price_entry.grid(column=1, row=3, padx=5)

create_btn = tk.Button(root, text="Create", command=create_product)
create_btn.grid(column=0, row=4, padx=5, pady=5)

read_btn = tk.Button(root, text="Read all", command=read_products)
read_btn.grid(column=1, row=4, padx=5, pady=5)

# Create input fields for update and delete operations
product_name_input_label = tk.Label(root, text="New product name:")
product_name_input_label.grid(column=2, row=0, padx=5, pady=5)
product_name_input = tk.Entry(root)
product_name_input.grid(column=3, row=0, padx=5, pady=5)

product_category_input_label = tk.Label(root, text="New category:")
product_category_input_label.grid(column=2, row=1, padx=5, pady=5)
product_category_input = tk.Entry(root)
product_category_input.grid(column=3, row=1, padx=5, pady=5)

product_quantity_input_label = tk.Label(root, text="New quantity:")
product_quantity_input_label.grid(column=2, row=2, padx=5, pady=5)
product_quantity_input = tk.Entry(root)
product_quantity_input.grid(column=3, row=2, padx=5, pady=5)

product_price_input_label = tk.Label(root, text="New price:")
product_price_input_label.grid(column=2, row=3, padx=5, pady=5)
product_price_input = tk.Entry(root)
product_price_input.grid(column=3, row=3, padx=5, pady=5)

product_id_input_label = tk.Label(root, text="Product id:")
product_id_input_label.grid(column=2, row=4, padx=5, pady=5)
product_id_input = tk.Entry(root)
product_id_input.grid(column=3, row=4, padx=5, pady=5)

update_btn = tk.Button(root, text="Update", command=update_product)
update_btn.grid(column=2, row=5, padx=5, pady=5)

delete_btn = tk.Button(root, text="Delete", command=delete_product)
delete_btn.grid(column=3, row=5, padx=5, pady=5)

# Define the products_list
products_list = tk.Listbox(root, width=60)
products_list.grid(column=0, row=6, columnspan=2, rowspan=5, padx=8, pady=8)



root.mainloop()