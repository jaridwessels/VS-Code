import tkinter as tk
from tkinter import ttk, messagebox

# Inventory Class
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
        self.load_items()

    def load_items(self):
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
        for d in defaults:
            self.items.append(Item(d["Name"], d["Category"], d["Quantity"], d["Price"]))

    def find_item_by_name(self, name):
        for item in self.items:
            if item.name.lower() == name.lower():
                return item
        return None

# Tkinter App 
class ShoppingCartApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Cart")

        self.inventory = Inventory()
        self.cart = []

        self.item_name = tk.StringVar()
        self.quantity = tk.StringVar()
        self.total_items = tk.StringVar(value="0")
        self.total_price = tk.StringVar(value="$0.00")

        self.setup_layout()
        self.load_inventory()

    def setup_layout(self):
        mainframe = ttk.Frame(self.root, padding="10")
        mainframe.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        inv_frame = ttk.LabelFrame(mainframe, text="Inventory", padding="5")
        inv_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        self.inv_tree = ttk.Treeview(inv_frame, columns=("Name", "Qty", "Price"), show="headings", height=20)
        for col in ("Name", "Qty", "Price"):
            self.inv_tree.heading(col, text=col)
            self.inv_tree.column(col, width=100, anchor="center")
        self.inv_tree.grid(row=0, column=0, sticky="ns")

        form_frame = ttk.Frame(mainframe, padding="5")
        form_frame.grid(row=0, column=1, sticky="n")

        ttk.Label(form_frame, text="Item Name:").grid(row=0, column=0, sticky="e")
        ttk.Entry(form_frame, textvariable=self.item_name, width=25).grid(row=0, column=1)

        ttk.Label(form_frame, text="Quantity:").grid(row=1, column=0, sticky="e")
        ttk.Entry(form_frame, textvariable=self.quantity, width=25).grid(row=1, column=1)

        ttk.Button(form_frame, text="Add to Cart", command=self.add_to_cart).grid(row=2, column=1, sticky="e", pady=5)
        ttk.Button(form_frame, text="Clear Cart", command=self.clear_cart).grid(row=3, column=1, sticky="e")

        # Display
        cart_frame = ttk.LabelFrame(mainframe, text="Shopping Cart", padding="5")
        cart_frame.grid(row=0, column=2, sticky="n")

        self.cart_list = tk.Listbox(cart_frame, height=20, width=50)
        self.cart_list.pack()

        ttk.Label(cart_frame, text="Total Items: ").pack(anchor="w")
        ttk.Label(cart_frame, textvariable=self.total_items).pack(anchor="w")
        ttk.Label(cart_frame, text="Total Price: ").pack(anchor="w")
        ttk.Label(cart_frame, textvariable=self.total_price).pack(anchor="w")

        # Menu
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="New Order", command=self.clear_cart)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

    def load_inventory(self):
        self.inv_tree.delete(*self.inv_tree.get_children())
        for item in self.inventory.items:
            self.inv_tree.insert("", tk.END, values=(item.name, item.quantity, f"${item.price:.2f}"))

    def add_to_cart(self):
        try:
            name = self.item_name.get().strip()
            qty = int(self.quantity.get())
            item = self.inventory.find_item_by_name(name)

            if not item:
                messagebox.showerror("Error", f"Item '{name}' not found in inventory.")
                return

            if qty <= 0:
                raise ValueError

            total = qty * item.price
            self.cart.append((item.name, qty, item.price, total))
            self.update_cart_display()
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity.")

    def clear_cart(self):
        self.cart.clear()
        self.update_cart_display()

    def update_cart_display(self):
        self.cart_list.delete(0, tk.END)
        for name, qty, price, total in self.cart:
            self.cart_list.insert(tk.END, f"{name} - Qty: {qty} @ ${price:.2f} = ${total:.2f}")
        self.total_items.set(str(sum(qty for _, qty, _, _ in self.cart)))
        total_price = sum(total for _, _, _, total in self.cart)
        self.total_price.set(f"${total_price:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x500")
    app = ShoppingCartApp(root)
    root.mainloop()
