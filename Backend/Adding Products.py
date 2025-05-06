import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
import os
import threading
import logging
from PIL import Image, ImageTk

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Mock function for AI categorization
def mock_ai_categorize(image_path):
    categories = ["Vintage", "Casual", "Formal", "Sportswear", "Designer", "Dresses", "Shoes", "Bags", "Accessories"]
    return categories[hash(image_path) % len(categories)]

class ImageUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Uploader")
        self.images = []
        self.image_data = []
        self.categories = ["Vintage", "Casual", "Formal", "Sportswear", "Designer", "Dresses", "Shoes", "Bags", "Accessories"]
        self.create_widgets()

    def create_widgets(self):
        self.select_button = tk.Button(self.root, text="Select Folder", command=self.select_folder)
        self.select_button.pack(pady=10)

        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.table = ttk.Treeview(self.table_frame, columns=("Image", "Category", "Name", "Price", "Rating"), show="headings")
        self.table.heading("Image", text="Image")
        self.table.heading("Category", text="Category")
        self.table.heading("Name", text="Name")
        self.table.heading("Price", text="Price (USD)")
        self.table.heading("Rating", text="Rating")
        self.table.column("Image", width=200)
        self.table.column("Category", width=150)
        self.table.column("Name", width=200)
        self.table.column("Price", width=100)
        self.table.column("Rating", width=100)
        self.table.pack(fill=tk.BOTH, expand=True)

        self.upload_button = tk.Button(self.root, text="Upload Images to Database", command=self.upload_images)
        self.upload_button.pack(pady=10)

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.images = [
                os.path.join(folder_path, f) for f in os.listdir(folder_path)
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp', '.ico', '.jfif', '.heic'))
            ]
            if not self.images:
                messagebox.showinfo("Info", "No images found in the selected folder.")
                return
            self.populate_table()

    def populate_table(self):
        for item in self.table.get_children():
            self.table.delete(item)

        for image_path in self.images:
            category = mock_ai_categorize(image_path)
            image_name = os.path.basename(image_path)
            name_without_extension = os.path.splitext(image_name)[0]
            price = ""
            rating = ""
            self.table.insert("", "end", values=(image_path, category, name_without_extension, price, rating), tags=("image_row",))

        self.table.bind('<Double-1>', self.on_row_double_click)

    def on_row_double_click(self, event):
        item = self.table.selection()
        if not item:
            return
        values = self.table.item(item[0], 'values')
        self.open_edit_window(values)
        self.display_image(values[0])

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def open_edit_window(self, values):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Image Details")
        edit_window.geometry("400x250")
        edit_window.transient(self.root)
        edit_window.update_idletasks()
        edit_window.after(100, edit_window.grab_set)

        tk.Label(edit_window, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        category_var = tk.StringVar(value=values[1])
        category_dropdown = ttk.Combobox(edit_window, textvariable=category_var, values=self.categories, state="readonly")
        category_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(edit_window, text="Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        name_entry = tk.Entry(edit_window, width=30)
        name_entry.insert(0, values[2])
        name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(edit_window, text="Price (USD):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        price_entry = tk.Entry(edit_window, width=10)
        price_entry.insert(0, values[3])
        price_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(edit_window, text="Rating (1-5):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        rating_entry = tk.Entry(edit_window, width=10)
        rating_entry.insert(0, values[4])
        rating_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        def save_changes():
            new_category = category_var.get()
            new_name = name_entry.get().strip()
            new_price = price_entry.get().strip()
            new_rating = rating_entry.get().strip()

            if not new_name:
                messagebox.showerror("Error", "Name cannot be empty.", parent=edit_window)
                return
            if not new_price:
                messagebox.showerror("Error", "Price cannot be empty.", parent=edit_window)
                return
            if not new_rating:
                messagebox.showerror("Error", "Rating cannot be empty.", parent=edit_window)
                return
            try:
                new_price = float(new_price)
                if new_price < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Price must be a valid non-negative number.", parent=edit_window)
                return
            try:
                new_rating = int(new_rating)
                if new_rating < 1 or new_rating > 5:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Rating must be a number between 1 and 5.", parent=edit_window)
                return

            self.table.item(self.table.selection()[0], values=(values[0], new_category, new_name, f"{new_price:.2f}", new_rating))
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def upload_images(self):
        self.image_data = []
        for child in self.table.get_children():
            values = self.table.item(child, 'values')
            image_path, category, name, price, rating = values
            if not name or not price or not rating:
                messagebox.showerror("Error", f"Please fill in name, price, and rating for image: {image_path}")
                return
            try:
                price = float(price)
                if price < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", f"Invalid price for image {image_path}. Please enter a valid non-negative number.")
                return
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", f"Invalid rating for image {image_path}. Please enter a number between 1 and 5.")
                return

            image_data = {
                "image_path": image_path,
                "name": name,
                "price": price,
                "category": category,
                "rating": rating
            }
            self.image_data.append(image_data)

        if not self.image_data:
            messagebox.showinfo("Info", "No images to upload.")
            return

        self.send_to_flask()

    def send_to_flask(self):
        url = "http://127.0.0.1:5000/add_product"
        def send_request():
            success_count = 0
            for data in self.image_data:
                try:
                    with open(data["image_path"], 'rb') as image_file:
                        files = {'image': (os.path.basename(data["image_path"]), image_file)}
                        form_data = {
                            'name': data['name'],
                            'price': str(data['price']),
                            'category': data['category'],
                            'rating': str(data['rating'])
                        }
                        response = requests.post(url, files=files, data=form_data, timeout=5)
                        if response.status_code == 201:
                            success_count += 1
                            logger.info(f"Uploaded {data['name']} successfully, ID: {response.json().get('product_id')}")
                        else:
                            messagebox.showerror("Error", f"Failed to upload {data['name']}: {response.json().get('error', 'Unknown error')}")
                            logger.error(f"Failed to upload {data['name']}: {response.text}")
                except requests.RequestException as e:
                    messagebox.showerror("Error", f"Failed to upload {data['name']}: {str(e)}")
                    logger.error(f"Upload failed for {data['name']}: {str(e)}")
            if success_count > 0:
                messagebox.showinfo("Success", f"Successfully uploaded {success_count} image(s).")
                logger.info(f"Uploaded {success_count} image(s) successfully.")
                for item in self.table.get_children():
                    self.table.delete(item)
                self.images = []
                self.image_data = []

        threading.Thread(target=send_request, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = ImageUploaderApp(root)
    root.mainloop()