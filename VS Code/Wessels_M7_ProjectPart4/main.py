import tkinter as tk
from tkinter import ttk, messagebox

class Item:
    def __init__(self, name, category, quantity, price):
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price

    def total_value(self):
        return self.quantity * self.price

class Inventory:
    def __init__(self):
        self.items = []
        self.load_default_items()

    def load_default_items(self):
        defaults = [
            {"Name": "Apple", "Category": "Fruit", "Quantity": 50, "Price": 0.50},
            {"Name": "Bacon", "Category": "Meat", "Quantity": 25, "Price": 4.50},
            {"Name": "Banana", "Category": "Fruit", "Quantity": 100, "Price": 0.30},
            {"Name": "Bread", "Category": "Bakery", "Quantity": 30, "Price": 2.00},
            {"Name": "Carrots", "Category": "Produce", "Quantity": 60, "Price": 1.00},
            {"Name": "Chicken breast", "Category": "Meat", "Quantity": 50, "Price": 5.00},
            {"Name": "Coffee", "Category": "Beverage", "Quantity": 20, "Price": 8.00},
            {"Name": "Eggs", "Category": "Dairy", "Quantity": 40, "Price": 2.50},
            {"Name": "Ground Beef", "Category": "Meat", "Quantity": 40, "Price": 4.00},
            {"Name": "Lettuce", "Category": "Produce", "Quantity": 40, "Price": 1.50},
            {"Name": "Milk", "Category": "Dairy", "Quantity": 25, "Price": 3.00},
            {"Name": "Orange Juice", "Category": "Beverage", "Quantity": 30, "Price": 4.00},
            {"Name": "Peanut Butter", "Category": "Pantry", "Quantity": 25, "Price": 3.00},
            {"Name": "Rice", "Category": "Pantry", "Quantity": 100, "Price": 1.20},
        ]
        for item in defaults:
            self.items.append(Item(item["Name"], item["Category"], item["Quantity"], item["Price"]))

    def add_item(self, item):
        for existing in self.items:
            if existing.name.lower() == item.name.lower():
                return False
        self.items.append(item)
        return True

    def remove_item(self, name):
        for item in self.items:
            if item.name.lower() == name.lower():
                self.items.remove(item)
                return True
        return False

    def update_item(self, name, quantity, price):
        for item in self.items:
            if item.name.lower() == name.lower():
                item.quantity = quantity
                item.price = price
                return True
        return False

    def search_by_name(self, name):
        return [item for item in self.items if item.name.lower() == name.lower()]

    def search_by_category(self, category):
        return [item for item in self.items if item.category.lower() == category.lower()]

    def get_all(self):
        return self.items

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grocery Inventory Manager")
        self.inventory = Inventory()

        self.setup_gui()
        self.load_items()

    def setup_gui(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Item", command=self.open_add_window).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Item", command=self.open_update_window).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Remove Selected", command=self.remove_selected_item).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Search", command=self.open_search_window).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Refresh", command=self.load_items).pack(side=tk.LEFT, padx=5)

        columns = ("Name", "Category", "Quantity", "Price", "Total")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_items(self, items=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        item_list = items if items is not None else self.inventory.get_all()
        for item in item_list:
            self.tree.insert("", tk.END, values=(
                item.name,
                item.category,
                item.quantity,
                f"${item.price:.2f}",
                f"${item.total_value():.2f}"
            ))

    def get_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])['values']

    def open_add_window(self):
        self.popup_form("Add New Item", self.add_item)

    def open_update_window(self):
        selected = self.get_selected_item()
        if not selected:
            messagebox.showerror("No selection", "Please select an item to update.")
            return
        self.popup_form("Update Item", self.update_item, prefill=selected)

    def open_search_window(self):
        win = tk.Toplevel(self.root)
        win.title("Search Items")

        tk.Label(win, text="Search by Name or Category:").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)

        def search():
            term = entry.get().strip()
            if not term:
                return
            by_name = self.inventory.search_by_name(term)
            by_category = self.inventory.search_by_category(term)
            results = by_name + [i for i in by_category if i not in by_name]
            self.load_items(results)
            win.destroy()

        tk.Button(win, text="Search", command=search).pack(pady=5)

    def popup_form(self, title, on_submit, prefill=None):
        win = tk.Toplevel(self.root)
        win.title(title)

        tk.Label(win, text="Name").grid(row=0, column=0)
        tk.Label(win, text="Category").grid(row=1, column=0)
        tk.Label(win, text="Quantity").grid(row=2, column=0)
        tk.Label(win, text="Price").grid(row=3, column=0)

        name_var = tk.StringVar(value=prefill[0] if prefill else "")
        cat_var = tk.StringVar(value=prefill[1] if prefill else "")
        qty_var = tk.StringVar(value=prefill[2] if prefill else "")
        price_var = tk.StringVar(value=prefill[3].replace("$", "") if prefill else "")

        tk.Entry(win, textvariable=name_var).grid(row=0, column=1)
        tk.Entry(win, textvariable=cat_var).grid(row=1, column=1)
        tk.Entry(win, textvariable=qty_var).grid(row=2, column=1)
        tk.Entry(win, textvariable=price_var).grid(row=3, column=1)

        def submit():
            try:
                name = name_var.get().strip()
                cat = cat_var.get().strip()
                qty = int(qty_var.get())
                price = float(price_var.get())
                if not name or not cat:
                    raise ValueError("Empty fields")
                on_submit(name, cat, qty, price)
                win.destroy()
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid data.")

        tk.Button(win, text="Submit", command=submit).grid(row=4, columnspan=2, pady=10)

    def add_item(self, name, category, quantity, price):
        item = Item(name, category, quantity, price)
        if self.inventory.add_item(item):
            self.load_items()
        else:
            messagebox.showwarning("Exists", "Item already exists.")

    def update_item(self, name, category, quantity, price):
        if self.inventory.update_item(name, quantity, price):
            self.load_items()
        else:
            messagebox.showerror("Not Found", "Item not found.")

    def remove_selected_item(self):
        selected = self.get_selected_item()
        if not selected:
            messagebox.showerror("No selection", "Select an item to remove.")
            return
        name = selected[0]
        if self.inventory.remove_item(name):
            self.load_items()
        else:
            messagebox.showerror("Error", "Failed to remove item.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x500")
    app = InventoryApp(root)
    root.mainloop()
