import tkinter as tk
from tkinter import messagebox
import requests
import json

class CreateUserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Create User")
        self.root.geometry("400x300")

        # Labels
        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(root, width=30)
        self.email_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Create User Button
        tk.Button(root, text="Create User", command=self.create_user).pack(pady=20)

        # Response Label
        self.response_label = tk.Label(root, text="", wraplength=350)
        self.response_label.pack(pady=10)

    def create_user(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        payload = {
            "username": username,
            "email": email,
            "password": password
        }

        try:
            response = requests.post("http://localhost:5000/create_user", json=payload)
            response_data = response.json()

            if response.status_code == 201:
                self.response_label.config(text="Success: User created successfully", fg="green")
            else:
                error_msg = response_data.get("error", "Unknown error")
                self.response_label.config(text=f"Error: {error_msg}", fg="red")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CreateUserApp(root)
    root.mainloop()