import tkinter as tk
from tkinter import ttk, messagebox
import requests
import base64
from io import BytesIO
from PIL import Image, ImageTk

# Function to fetch products from the backend
def fetch_products():
    try:
        response = requests.get('http://127.0.0.1:5000/fetch_products')
        response.raise_for_status()
        products = response.json()
        print("Data received from backend:")
        print(products)  # Print the received data to the terminal
        return products
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch products: {e}")
        return []

# Function to display products in the Tkinter window
def display_products():
    products = fetch_products()
    for widget in product_frame.winfo_children():
        widget.destroy()

    if not products:
        messagebox.showinfo("Info", "No products found.")
        return

    for product in products:
        frame = ttk.Frame(product_frame)
        frame.pack(fill='x', expand=True, pady=5, padx=5)

        name_label = ttk.Label(frame, text=product.get('name', 'Unnamed Product'), font=("Helvetica", 16))
        name_label.pack(anchor='w')

        price_label = ttk.Label(frame, text=f"Price: ${product.get('price', '0.00')}", font=("Helvetica", 12))
        price_label.pack(anchor='w')

        category_label = ttk.Label(frame, text=f"Category: {product.get('category', 'Uncategorized')}", font=("Helvetica", 12))
        category_label.pack(anchor='w')

        rating_label = ttk.Label(frame, text=f"Rating: {product.get('rating', 'N/A')}", font=("Helvetica", 12))
        rating_label.pack(anchor='w')

        if product.get('image_base64'):
            image_data = base64.b64decode(product['image_base64'])
            image = Image.open(BytesIO(image_data))
            image = image.resize((100, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)

            image_label = ttk.Label(frame, image=photo)
            image_label.image = photo
            image_label.pack(anchor='w')

# Create the main window
root = tk.Tk()
root.title("Product Viewer")
root.geometry("800x600")

# Create a frame to hold the product list
product_frame = ttk.Frame(root)
product_frame.pack(fill='both', expand=True, padx=10, pady=10)

# Create a button to fetch and display products
fetch_button = ttk.Button(root, text="Fetch Products", command=display_products)
fetch_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
