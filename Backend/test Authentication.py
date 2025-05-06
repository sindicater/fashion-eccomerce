import tkinter as tk
from tkinter import messagebox
import bcrypt


class UserAuthApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Authentication Tester")
        self.root.geometry("400x250")

        # In-memory user storage (simulating Supabase table)
        self.users = {}

        # GUI elements
        self.create_gui()

    def hash_password(self, password):
        """Hash a password for storing."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, stored_password, provided_password):
        """Check hashed password."""
        try:
            return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)
        except Exception:
            return False

    def create_user(self):
        """Create a new user."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return

        password_hash = self.hash_password(password)
        self.users[username] = {'username': username, 'password_hash': password_hash}
        messagebox.showinfo("Success", "User created successfully")
        self.clear_entries()

    def authenticate_user(self):
        """Authenticate an existing user."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password")
            return

        user = self.users.get(username)
        if user and self.check_password(user['password_hash'], password):
            messagebox.showinfo("Success", "Authentication successful")
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def clear_entries(self):
        """Clear all entry fields."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def create_gui(self):
        """Create the GUI layout."""
        # Labels
        tk.Label(self.root, text="Username:").pack(pady=10)
        self.username_entry = tk.Entry(self.root, width=30)
        self.username_entry.pack()

        tk.Label(self.root, text="Password:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, width=30, show="*")
        self.password_entry.pack()

        # Buttons
        tk.Button(self.root, text="Create User", command=self.create_user).pack(pady=15)
        tk.Button(self.root, text="Authenticate User", command=self.authenticate_user).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = UserAuthApp(root)
    root.mainloop()