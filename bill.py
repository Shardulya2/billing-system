from tkinter import *
from tkinter import ttk, messagebox
import random
import pymysql
import os
from dotenv import load_dotenv
load_dotenv()

# ================= DB =================
def connect_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
class BillingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")
        self.root.geometry("1100x650")
        self.root.config(bg="white")

        self.bill_no = random.randint(100, 999)
        self.cart = []

        # VARIABLES
        self.c_name = StringVar()
        self.c_phone = StringVar()
        self.c_email = StringVar()

        self.category = StringVar()
        self.sub_category = StringVar()
        self.product = StringVar()
        self.price = IntVar()
        self.qty = IntVar(value=1)

        self.sub_total = StringVar(value="0")
        self.tax = StringVar(value="0")
        self.total = StringVar(value="0")

        self.search_var = StringVar()

        # TITLE
        Label(root, text="BILLING SOFTWARE",
              font=("Arial", 22, "bold"), fg="red", bg="white").pack(fill=X)

        # LEFT FRAME
        left = Frame(root, bd=2, relief=RIDGE, bg="white")
        left.place(x=5, y=50, width=500, height=400)

        LabelFrame(left, text="Customer", fg="red", bg="white").place(x=5, y=5, width=490, height=130)

        Label(left, text="Mobile No:", bg="white").place(x=20, y=30)
        Entry(left, textvariable=self.c_phone).place(x=140, y=30)

        Label(left, text="Customer Name:", bg="white").place(x=20, y=60)
        Entry(left, textvariable=self.c_name).place(x=140, y=60)

        Label(left, text="Email:", bg="white").place(x=20, y=90)
        Entry(left, textvariable=self.c_email).place(x=140, y=90)

        LabelFrame(left, text="Product", fg="red", bg="white").place(x=5, y=140, width=490, height=250)

        Label(left, text="Select Categories:", bg="white").place(x=20, y=170)
        ttk.Combobox(left, textvariable=self.category,
                     values=["Lifestyle"]).place(x=180, y=170)

        Label(left, text="Price:", bg="white").place(x=320, y=170)
        Entry(left, textvariable=self.price, width=8).place(x=370, y=170)

        Label(left, text="Sub Category:", bg="white").place(x=20, y=210)
        ttk.Combobox(left, textvariable=self.sub_category,
                     values=["Face Cream"]).place(x=180, y=210)

        Label(left, text="Quantity:", bg="white").place(x=320, y=210)
        Entry(left, textvariable=self.qty, width=8).place(x=390, y=210)

        Label(left, text="Product Name:", bg="white").place(x=20, y=250)
        combo = ttk.Combobox(left, textvariable=self.product,
                             values=["Fair&Lovely", "Ponds"])
        combo.place(x=180, y=250)
        combo.bind("<<ComboboxSelected>>", self.get_price)

        Button(left, text="Add To Cart", bg="orange",
               command=self.add_to_cart).place(x=350, y=250)

        # RIGHT
        right = Frame(root, bd=2, relief=RIDGE)
        right.place(x=510, y=50, width=580, height=400)

        Label(right, text="Bill Number:").place(x=10, y=10)
        Entry(right, textvariable=self.search_var).place(x=100, y=10)

        Button(right, text="Search", bg="orange",
               command=self.search_bill).place(x=260, y=7)

        Label(right, text="Bill Area", fg="red").place(x=10, y=40)

        self.textarea = Text(right)
        self.textarea.place(x=10, y=60, width=550, height=300)

        self.init_bill()

        # BOTTOM
        bottom = Frame(root, bd=2, relief=RIDGE)
        bottom.place(x=5, y=460, width=1085, height=150)

        Label(bottom, text="Sub Total:").place(x=20, y=20)
        Entry(bottom, textvariable=self.sub_total).place(x=120, y=20)

        Label(bottom, text="Govt Tax:").place(x=20, y=50)
        Entry(bottom, textvariable=self.tax).place(x=120, y=50)

        Label(bottom, text="Total:").place(x=20, y=80)
        Entry(bottom, textvariable=self.total).place(x=120, y=80)

        Button(bottom, text="Generate Bill", bg="orange",
               command=self.generate_bill).place(x=300, y=30, width=120)

        Button(bottom, text="Save Bill", bg="orange",
               command=self.save_bill).place(x=430, y=30, width=100)

        Button(bottom, text="Print", bg="orange",
               command=self.print_bill).place(x=540, y=30, width=100)

        Button(bottom, text="Clear", bg="orange",
               command=self.clear).place(x=650, y=30, width=100)

        Button(bottom, text="Exit", bg="orange",
               command=root.quit).place(x=760, y=30, width=100)

    # LOGIC
    def init_bill(self):
        self.textarea.delete("1.0", END)
        self.textarea.insert(END, f"Bill Number: {self.bill_no}\n")
        self.textarea.insert(END, "Customer Name:\nMobile Number:\nCustomer Email:\n")
        self.textarea.insert(END, "="*50 + "\n")
        self.textarea.insert(END, "Products\tQTY\tPrice\n")
        self.textarea.insert(END, "="*50 + "\n")

    def get_price(self, event=""):
        prices = {"Fair&Lovely": 120, "Ponds": 150}
        self.price.set(prices.get(self.product.get(), 0))

    def add_to_cart(self):
        total = self.qty.get() * self.price.get()
        self.cart.append((self.product.get(), self.qty.get(), self.price.get(), total))

        self.textarea.insert(END,
            f"{self.product.get()}\t{self.qty.get()}\t{total}\n")

        self.update_total()

    def update_total(self):
        subtotal = sum(item[3] for item in self.cart)
        tax = subtotal * 0.18
        total = subtotal + tax

        self.sub_total.set(f"{subtotal:.2f}")
        self.tax.set(f"{tax:.2f}")
        self.total.set(f"{total:.2f}")

    def generate_bill(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        self.textarea.delete("1.0", END)

        self.textarea.insert(END, f"Bill Number: {self.bill_no}\n")
        self.textarea.insert(END, f"Customer Name: {self.c_name.get()}\n")
        self.textarea.insert(END, f"Mobile Number: {self.c_phone.get()}\n")
        self.textarea.insert(END, f"Customer Email: {self.c_email.get()}\n")
        self.textarea.insert(END, "="*50 + "\n")
        self.textarea.insert(END, "Products\tQTY\tPrice\n")
        self.textarea.insert(END, "="*50 + "\n")

        subtotal = 0

        for item in self.cart:
            name, qty, price, total = item
            subtotal += total
            self.textarea.insert(END,
                f"{name}\t{qty}\t{price}\t{total}\n")

        gst = subtotal * 0.18
        final_total = subtotal + gst

        self.sub_total.set(f"{subtotal:.2f}")
        self.tax.set(f"{gst:.2f}")
        self.total.set(f"{final_total:.2f}")

        self.textarea.insert(END, "="*50 + "\n")
        self.textarea.insert(END, f"Sub Total:\t{subtotal:.2f}\n")
        self.textarea.insert(END, f"GST (18%):\t{gst:.2f}\n")
        self.textarea.insert(END, f"Total:\t{final_total:.2f}\n")

    def save_bill(self):
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO bills 
            (bill_no, customer_name, mobile, email, subtotal, gst, total)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            self.bill_no,
            self.c_name.get(),
            self.c_phone.get(),
            self.c_email.get(),
            float(self.sub_total.get()),
            float(self.tax.get()),
            float(self.total.get())
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Bill saved successfully")

    def search_bill(self):
        bill_no = self.search_var.get()

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM bills WHERE bill_no=%s", (bill_no,))
        bill = cur.fetchone()

        if not bill:
            messagebox.showerror("Error", "Bill not found")
            cur.close()
            conn.close()
            return

        self.textarea.delete("1.0", END)

        self.textarea.insert(END, f"Bill Number: {bill[1]}\n")
        self.textarea.insert(END, f"Customer Name: {bill[2]}\n")
        self.textarea.insert(END, f"Mobile Number: {bill[3]}\n")
        self.textarea.insert(END, f"Customer Email: {bill[4]}\n")
        self.textarea.insert(END, "="*50 + "\n")
        self.textarea.insert(END, f"Subtotal: {bill[5]}\n")
        self.textarea.insert(END, f"GST: {bill[6]}\n")
        self.textarea.insert(END, f"Total: {bill[7]}\n")

        conn.close()

    def print_bill(self):
        data = self.textarea.get("1.0", END)

        with open("bill.txt", "w") as f:
            f.write(data)

        os.startfile("bill.txt", "print")

    def clear(self):
        self.cart.clear()
        self.init_bill()
        self.sub_total.set("0")
        self.tax.set("0")
        self.total.set("0")


root = Tk()
app = BillingApp(root)
root.mainloop()