import tkinter as tk
from tkinter import messagebox
import requests
import json

class AuthenticateUserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Authenticate User")
        self.root.geometry("400x250")

        # Labels
        tk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(root, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Authenticate Button
        tk.Button(root, text="Authenticate", command=self.authenticate_user).pack(pady=20)

        # Response Label
        self.response_label = tk.Label(root, text="", wraplength=350)
        self.response_label.pack(pady=10)

    def authenticate_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required!")
            return

        payload = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post("http://localhost:5000/authenticate_user", json=payload)
            response_data = response.json()

            if response.status_code == 200:
                user_id = response_data.get("user_id", "N/A")
                username = response_data.get("username", "N/A")
                self.response_label.config(
                    text=f"Success: Authenticated! User ID: {user_id}, Username: {username}",
                    fg="green"
                )
            else:
                error_msg = response_data.get("error", "Unknown error")
                self.response_label.config(text=f"Error: {error_msg}", fg="red")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to connect to server: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AuthenticateUserApp(root)
    root.mainloop()