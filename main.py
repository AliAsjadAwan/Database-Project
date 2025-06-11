import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
import json
from datetime import datetime

class ToursTravelsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tours and Travels Company Management System")
        self.root.geometry("1200x700")

        # Database connection
        self.conn = pyodbc.connect(
            'Driver={SQL Server};'
            'Server=localhost;'
            'Database=Tours_and_Travels_Company;'
            'Trusted_Connection=yes;'
        )
        self.cursor = self.conn.cursor()

        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Create tabs
        self.create_users_tab()
        self.create_groups_tab()
        self.create_customers_tab()
        self.create_flights_tab()
        self.create_hotels_tab()
        self.create_meals_tab()
        self.create_transport_tab()
        self.create_visas_tab()
        self.create_syria_tickets_tab()
        self.create_expenses_tab()
        self.create_reports_tab()
        self.create_history_tab()

    def create_users_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Users")

        # Treeview for displaying users
        self.users_tree = ttk.Treeview(tab, columns=("UserID", "Username", "Role"), show="headings")
        self.users_tree.heading("UserID", text="User ID")
        self.users_tree.heading("Username", text="Username")
        self.users_tree.heading("Role", text="Role")
        self.users_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Users", command=self.load_users).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add User", command=self.add_user_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update User", command=self.update_user_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete User", command=self.delete_user).pack(side=tk.LEFT, padx=5)

        self.load_users()

    def load_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        self.cursor.execute("SELECT UserID, Username, Role FROM USERS")
        for row in self.cursor.fetchall():
            self.users_tree.insert("", tk.END, values=row)

    def add_user_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New User")

        tk.Label(dialog, text="Username:").grid(row=0, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(dialog)
        username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Password:").grid(row=1, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Role:").grid(row=2, column=0, padx=5, pady=5)
        role_combobox = ttk.Combobox(dialog, values=["CEO", "Employee"])
        role_combobox.grid(row=2, column=1, padx=5, pady=5)

        def save_user():
            username = username_entry.get()
            password = password_entry.get()
            role = role_combobox.get()

            if not all([username, password, role]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                self.cursor.execute(
                    "INSERT INTO USERS (UserID, Username, Password, Role) VALUES (?, ?, ?, ?)",
                    self.get_next_id("USERS", "UserID"), username, password, role
                )
                self.conn.commit()
                messagebox.showinfo("Success", "User added successfully!")
                self.load_users()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add user: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_user).grid(row=3, columnspan=2, pady=10)

    def update_user_dialog(self):
        selected = self.users_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a user to update!")
            return

        user_data = self.users_tree.item(selected, "values")

        dialog = tk.Toplevel(self.root)
        dialog.title("Update User")

        tk.Label(dialog, text="User ID:").grid(row=0, column=0, padx=5, pady=5)
        id_label = tk.Label(dialog, text=user_data[0])
        id_label.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Username:").grid(row=1, column=0, padx=5, pady=5)
        username_entry = ttk.Entry(dialog)
        username_entry.insert(0, user_data[1])
        username_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        password_entry = ttk.Entry(dialog, show="*")
        password_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(dialog, text="Role:").grid(row=3, column=0, padx=5, pady=5)
        role_combobox = ttk.Combobox(dialog, values=["CEO", "Employee"])
        role_combobox.set(user_data[2])
        role_combobox.grid(row=3, column=1, padx=5, pady=5)

        def save_changes():
            username = username_entry.get()
            password = password_entry.get()
            role = role_combobox.get()

            if not all([username, role]):
                messagebox.showerror("Error", "Username and Role are required!")
                return

            try:
                if password:
                    self.cursor.execute(
                        "UPDATE USERS SET Username=?, Password=?, Role=? WHERE UserID=?",
                        username, password, role, user_data[0]
                    )
                else:
                    self.cursor.execute(
                        "UPDATE USERS SET Username=?, Role=? WHERE UserID=?",
                        username, role, user_data[0]
                    )
                self.conn.commit()
                messagebox.showinfo("Success", "User updated successfully!")
                self.load_users()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update user: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=4, columnspan=2, pady=10)

    def delete_user(self):
        selected = self.users_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a user to delete!")
            return

        user_data = self.users_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete user {user_data[1]}?"):
            try:
                self.cursor.execute("DELETE FROM USERS WHERE UserID=?", user_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "User deleted successfully!")
                self.load_users()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

    def create_groups_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Travel Groups")

        # Treeview for displaying groups
        self.groups_tree = ttk.Treeview(tab, columns=("GroupID", "GroupName", "Destination", "StartDate", "EndDate", "Status"), show="headings")
        self.groups_tree.heading("GroupID", text="Group ID")
        self.groups_tree.heading("GroupName", text="Group Name")
        self.groups_tree.heading("Destination", text="Destination")
        self.groups_tree.heading("StartDate", text="Start Date")
        self.groups_tree.heading("EndDate", text="End Date")
        self.groups_tree.heading("Status", text="Status")
        self.groups_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Groups", command=self.load_groups).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Group", command=self.add_group_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Group", command=self.update_group_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Group", command=self.delete_group).pack(side=tk.LEFT, padx=5)

        self.load_groups()

    def load_groups(self):
        for item in self.groups_tree.get_children():
            self.groups_tree.delete(item)

        self.cursor.execute("SELECT GroupID, GroupName, DestinationCountry, StartDate, EndDate, Status FROM TRAVELGROUPS")
        for row in self.cursor.fetchall():
            self.groups_tree.insert("", tk.END, values=row)

    def add_group_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Travel Group")

        fields = [
            ("Group Name:", "entry"),
            ("Destination Country:", "entry"),
            ("Start Date (YYYY-MM-DD):", "entry"),
            ("End Date (YYYY-MM-DD):", "entry"),
            ("Created By User ID:", "entry")
        ]

        entries = []
        for i, (label, field_type) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)
            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)

        def save_group():
            try:
                group_name = entries[0].get()
                destination = entries[1].get()
                start_date = entries[2].get()
                end_date = entries[3].get()
                created_by = entries[4].get()

                if not all([group_name, destination, start_date, end_date, created_by]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO TRAVELGROUPS (GroupID, GroupName, DestinationCountry, StartDate, EndDate, Status, CreatedBy) "
                    "VALUES (?, ?, ?, ?, ?, 'Open', ?)",
                    self.get_next_id("TRAVELGROUPS", "GroupID"), group_name, destination, start_date, end_date, created_by
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Travel group added successfully!")
                self.load_groups()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add group: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_group).grid(row=len(fields), columnspan=2, pady=10)

    def update_group_dialog(self):
        selected = self.groups_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a group to update!")
            return

        group_data = self.groups_tree.item(selected, "values")

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Travel Group")

        fields = [
            ("Group ID:", group_data[0], "label"),
            ("Group Name:", group_data[1], "entry"),
            ("Destination Country:", group_data[2], "entry"),
            ("Start Date (YYYY-MM-DD):", group_data[3], "entry"),
            ("End Date (YYYY-MM-DD):", group_data[4], "entry"),
            ("Status:", group_data[5], "combobox", ["Open", "Closed", "Cancelled"])
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                group_name = entries[0].get()
                destination = entries[1].get()
                start_date = entries[2].get()
                end_date = entries[3].get()
                status = entries[4].get()

                if not all([group_name, destination, start_date, end_date, status]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE TRAVELGROUPS SET GroupName=?, DestinationCountry=?, StartDate=?, EndDate=?, Status=? "
                    "WHERE GroupID=?",
                    group_name, destination, start_date, end_date, status, group_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Travel group updated successfully!")
                self.load_groups()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update group: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_group(self):
        selected = self.groups_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a group to delete!")
            return

        group_data = self.groups_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete group {group_data[1]} and all related data?"):
            try:
                # First delete related records in other tables
                self.cursor.execute("DELETE FROM CUSTOMERS WHERE GroupID=?", group_data[0])
                self.cursor.execute("DELETE FROM EXPENSES WHERE GroupID=?", group_data[0])
                self.cursor.execute("DELETE FROM PROFITREPORTS WHERE GroupID=?", group_data[0])

                # Then delete the group
                self.cursor.execute("DELETE FROM TRAVELGROUPS WHERE GroupID=?", group_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Group deleted successfully!")
                self.load_groups()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete group: {str(e)}")

    def create_customers_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Customers")

        # Treeview for displaying customers
        self.customers_tree = ttk.Treeview(tab, columns=("CustomerID", "FullName", "Passport", "Nationality", "Group"), show="headings")
        self.customers_tree.heading("CustomerID", text="Customer ID")
        self.customers_tree.heading("FullName", text="Full Name")
        self.customers_tree.heading("Passport", text="Passport Number")
        self.customers_tree.heading("Nationality", text="Nationality")
        self.customers_tree.heading("Group", text="Group ID")
        self.customers_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Customers", command=self.load_customers).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Customer", command=self.add_customer_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Customer", command=self.update_customer_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Customer", command=self.delete_customer).pack(side=tk.LEFT, padx=5)

        self.load_customers()

    def load_customers(self):
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)

        self.cursor.execute("SELECT CustomerID, FullName, PassportNumber, Nationality, GroupID FROM CUSTOMERS")
        for row in self.cursor.fetchall():
            self.customers_tree.insert("", tk.END, values=row)

    def add_customer_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Customer")

        fields = [
            ("Full Name:", "entry"),
            ("Passport Number:", "entry"),
            ("Nationality:", "entry"),
            ("Contact Number:", "entry"),
            ("Email:", "entry"),
            ("Group ID (optional):", "entry"),
            ("Service Type:", "combobox", ["Flight", "Hotel", "Meal", "Transport", "Visa", "Syria Ticket"])
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_customer():
            try:
                full_name = entries[0].get()
                passport = entries[1].get()
                nationality = entries[2].get()
                contact = entries[3].get()
                email = entries[4].get()
                group_id = entries[5].get()
                service_type = entries[6].get()

                if not all([full_name, passport, nationality, contact, email, service_type]):
                    messagebox.showerror("Error", "All fields except Group ID are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO CUSTOMERS (CustomerID, FullName, PassportNumber, Nationality, ContactNumber, Email, GroupID, ServiceType) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    self.get_next_id("CUSTOMERS", "CustomerID"), full_name, passport, nationality,
                    contact, email, group_id if group_id else None, service_type
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                self.load_customers()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add customer: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_customer).grid(row=len(fields), columnspan=2, pady=10)

    def update_customer_dialog(self):
        selected = self.customers_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to update!")
            return

        customer_data = self.customers_tree.item(selected, "values")

        # Get full customer data
        self.cursor.execute("SELECT * FROM CUSTOMERS WHERE CustomerID=?", customer_data[0])
        full_data = self.cursor.fetchone()

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Customer")

        fields = [
            ("Customer ID:", customer_data[0], "label"),
            ("Full Name:", full_data.FullName, "entry"),
            ("Passport Number:", full_data.PassportNumber, "entry"),
            ("Nationality:", full_data.Nationality, "entry"),
            ("Contact Number:", full_data.ContactNumber, "entry"),
            ("Email:", full_data.Email, "entry"),
            ("Group ID:", full_data.GroupID if full_data.GroupID else "", "entry"),
            ("Service Type:", full_data.ServiceType, "combobox", ["Flight", "Hotel", "Meal", "Transport", "Visa", "Syria Ticket"])
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                full_name = entries[0].get()
                passport = entries[1].get()
                nationality = entries[2].get()
                contact = entries[3].get()
                email = entries[4].get()
                group_id = entries[5].get()
                service_type = entries[6].get()

                if not all([full_name, passport, nationality, contact, email, service_type]):
                    messagebox.showerror("Error", "All fields except Group ID are required!")
                    return

                self.cursor.execute(
                    "UPDATE CUSTOMERS SET FullName=?, PassportNumber=?, Nationality=?, ContactNumber=?, "
                    "Email=?, GroupID=?, ServiceType=? WHERE CustomerID=?",
                    full_name, passport, nationality, contact, email,
                    group_id if group_id else None, service_type, customer_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Customer updated successfully!")
                self.load_customers()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update customer: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_customer(self):
        selected = self.customers_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a customer to delete!")
            return

        customer_data = self.customers_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete customer {customer_data[1]} and all related bookings?"):
            try:
                # First delete related bookings
                self.cursor.execute("DELETE FROM FLIGHTS WHERE CustomerID=?", customer_data[0])
                self.cursor.execute("DELETE FROM HOTELS WHERE CustomerID=?", customer_data[0])
                self.cursor.execute("DELETE FROM MEALS WHERE CustomerID=?", customer_data[0])
                self.cursor.execute("DELETE FROM TRANSPORT WHERE CustomerID=?", customer_data[0])
                self.cursor.execute("DELETE FROM VISAS WHERE CustomerID=?", customer_data[0])
                self.cursor.execute("DELETE FROM SYRIATICKETS WHERE CustomerID=?", customer_data[0])

                # Then delete the customer
                self.cursor.execute("DELETE FROM CUSTOMERS WHERE CustomerID=?", customer_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Customer deleted successfully!")
                self.load_customers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")

    def create_flights_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Flights")

        # Treeview for displaying flights
        self.flights_tree = ttk.Treeview(tab, columns=("FlightID", "Customer", "Airline", "FlightNo", "Departure", "Arrival", "Status"), show="headings")
        self.flights_tree.heading("FlightID", text="Flight ID")
        self.flights_tree.heading("Customer", text="Customer")
        self.flights_tree.heading("Airline", text="Airline")
        self.flights_tree.heading("FlightNo", text="Flight No")
        self.flights_tree.heading("Departure", text="Departure Date")
        self.flights_tree.heading("Arrival", text="Arrival Date")
        self.flights_tree.heading("Status", text="Status")
        self.flights_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Flights", command=self.load_flights).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Flight", command=self.add_flight_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Flight", command=self.update_flight_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Flight", command=self.delete_flight).pack(side=tk.LEFT, padx=5)

        self.load_flights()

    def load_flights(self):
        for item in self.flights_tree.get_children():
            self.flights_tree.delete(item)

        self.cursor.execute("""
                            SELECT f.FlightID, c.FullName, f.Airline, f.FlightNumber, f.DepartureDate, f.ArrivalDate, f.BookingStatus
                            FROM FLIGHTS f
                                     JOIN CUSTOMERS c ON f.CustomerID = c.CustomerID
                            """)
        for row in self.cursor.fetchall():
            self.flights_tree.insert("", tk.END, values=row)

    def add_flight_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Flight Booking")

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]

        fields = [
            ("Customer:", "combobox", customer_options),
            ("Airline:", "entry"),
            ("Flight Number:", "entry"),
            ("Country:", "entry"),
            ("Departure Date (YYYY-MM-DD):", "entry"),
            ("Arrival Date (YYYY-MM-DD):", "entry"),
            ("Ticket Price:", "entry"),
            ("Currency:", "combobox", ["USD", "EUR", "GBP", "SAR"]),
            ("Discount Applied:", "entry"),
            ("Booking Status:", "combobox", ["Confirmed", "Pending", "Cancelled"])
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_flight():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                airline = entries[1].get()
                flight_number = entries[2].get()
                country = entries[3].get()
                departure_date = entries[4].get()
                arrival_date = entries[5].get()
                ticket_price = entries[6].get()
                currency = entries[7].get()
                discount = entries[8].get()
                status = entries[9].get()

                if not all([customer_id, airline, flight_number, country, departure_date,
                            arrival_date, ticket_price, currency, status]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO FLIGHTS (FlightID, CustomerID, Airline, FlightNumber, Country, "
                    "DepartureDate, ArrivalDate, TicketPrice, Currency, DiscountApplied, BookingStatus) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    self.get_next_id("FLIGHTS", "FlightID"), customer_id, airline, flight_number, country,
                    departure_date, arrival_date, ticket_price, currency, discount, status
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Flight booking added successfully!")
                self.load_flights()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add flight booking: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_flight).grid(row=len(fields), columnspan=2, pady=10)

    def update_flight_dialog(self):
        selected = self.flights_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a flight to update!")
            return

        flight_data = self.flights_tree.item(selected, "values")

        # Get full flight data
        self.cursor.execute("SELECT * FROM FLIGHTS WHERE FlightID=?", flight_data[0])
        full_data = self.cursor.fetchone()

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]
        current_customer = f"{full_data.CustomerID} - {flight_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Flight Booking")

        fields = [
            ("Flight ID:", flight_data[0], "label"),
            ("Customer:", current_customer, "combobox", customer_options),
            ("Airline:", full_data.Airline, "entry"),
            ("Flight Number:", full_data.FlightNumber, "entry"),
            ("Country:", full_data.Country, "entry"),
            ("Departure Date:", full_data.DepartureDate, "entry"),
            ("Arrival Date:", full_data.ArrivalDate, "entry"),
            ("Ticket Price:", full_data.TicketPrice, "entry"),
            ("Currency:", full_data.Currency, "combobox", ["USD", "EUR", "GBP", "SAR"]),
            ("Discount Applied:", full_data.DiscountApplied, "entry"),
            ("Booking Status:", full_data.BookingStatus, "combobox", ["Confirmed", "Pending", "Cancelled"])
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                airline = entries[1].get()
                flight_number = entries[2].get()
                country = entries[3].get()
                departure_date = entries[4].get()
                arrival_date = entries[5].get()
                ticket_price = entries[6].get()
                currency = entries[7].get()
                discount = entries[8].get()
                status = entries[9].get()

                if not all([customer_id, airline, flight_number, country, departure_date,
                            arrival_date, ticket_price, currency, status]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE FLIGHTS SET CustomerID=?, Airline=?, FlightNumber=?, Country=?, "
                    "DepartureDate=?, ArrivalDate=?, TicketPrice=?, Currency=?, DiscountApplied=?, BookingStatus=? "
                    "WHERE FlightID=?",
                    customer_id, airline, flight_number, country, departure_date, arrival_date,
                    ticket_price, currency, discount, status, flight_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Flight booking updated successfully!")
                self.load_flights()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update flight booking: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_flight(self):
        selected = self.flights_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a flight to delete!")
            return

        flight_data = self.flights_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete flight {flight_data[3]} for {flight_data[1]}?"):
            try:
                self.cursor.execute("DELETE FROM FLIGHTS WHERE FlightID=?", flight_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Flight booking deleted successfully!")
                self.load_flights()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete flight booking: {str(e)}")

    def create_hotels_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Hotels")

        # Treeview for displaying hotels
        self.hotels_tree = ttk.Treeview(tab, columns=("HotelID", "Customer", "Vendor", "Country", "Category", "CheckIn", "CheckOut"), show="headings")
        self.hotels_tree.heading("HotelID", text="Hotel ID")
        self.hotels_tree.heading("Customer", text="Customer")
        self.hotels_tree.heading("Vendor", text="Vendor ID")
        self.hotels_tree.heading("Country", text="Country")
        self.hotels_tree.heading("Category", text="Category")
        self.hotels_tree.heading("CheckIn", text="Check In")
        self.hotels_tree.heading("CheckOut", text="Check Out")
        self.hotels_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Hotels", command=self.load_hotels).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Hotel", command=self.add_hotel_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Hotel", command=self.update_hotel_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Hotel", command=self.delete_hotel).pack(side=tk.LEFT, padx=5)

        self.load_hotels()

    def load_hotels(self):
        for item in self.hotels_tree.get_children():
            self.hotels_tree.delete(item)

        self.cursor.execute("""
                            SELECT h.HotelID, c.FullName, h.VendorID, h.Country, h.Category, h.CheckInDate, h.CheckOutDate
                            FROM HOTELS h
                                     JOIN CUSTOMERS c ON h.CustomerID = c.CustomerID
                            """)
        for row in self.cursor.fetchall():
            self.hotels_tree.insert("", tk.END, values=row)

    def add_hotel_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Hotel Booking")

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]

        fields = [
            ("Customer:", "combobox", customer_options),
            ("Vendor ID:", "entry"),
            ("Country:", "entry"),
            ("Category:", "combobox", ["1 Star", "2 Star", "3 Star", "4 Star", "5 Star"]),
            ("Check In Date (YYYY-MM-DD):", "entry"),
            ("Check Out Date (YYYY-MM-DD):", "entry"),
            ("Total Cost:", "entry"),
            ("Currency:", "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_hotel():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                vendor_id = entries[1].get()
                country = entries[2].get()
                category = entries[3].get()
                check_in = entries[4].get()
                check_out = entries[5].get()
                total_cost = entries[6].get()
                currency = entries[7].get()

                if not all([customer_id, vendor_id, country, category, check_in, check_out, total_cost, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO HOTELS (HotelID, CustomerID, VendorID, Country, Category, "
                    "CheckInDate, CheckOutDate, TotalCost, Currency) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    self.get_next_id("HOTELS", "HotelID"), customer_id, vendor_id, country, category,
                    check_in, check_out, total_cost, currency
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Hotel booking added successfully!")
                self.load_hotels()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add hotel booking: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_hotel).grid(row=len(fields), columnspan=2, pady=10)

    def update_hotel_dialog(self):
        selected = self.hotels_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a hotel booking to update!")
            return

        hotel_data = self.hotels_tree.item(selected, "values")

        # Get full hotel data
        self.cursor.execute("SELECT * FROM HOTELS WHERE HotelID=?", hotel_data[0])
        full_data = self.cursor.fetchone()

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]
        current_customer = f"{full_data.CustomerID} - {hotel_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Hotel Booking")

        fields = [
            ("Hotel ID:", hotel_data[0], "label"),
            ("Customer:", current_customer, "combobox", customer_options),
            ("Vendor ID:", full_data.VendorID, "entry"),
            ("Country:", full_data.Country, "entry"),
            ("Category:", full_data.Category, "combobox", ["1 Star", "2 Star", "3 Star", "4 Star", "5 Star"]),
            ("Check In Date:", full_data.CheckInDate, "entry"),
            ("Check Out Date:", full_data.CheckOutDate, "entry"),
            ("Total Cost:", full_data.TotalCost, "entry"),
            ("Currency:", full_data.Currency, "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                vendor_id = entries[1].get()
                country = entries[2].get()
                category = entries[3].get()
                check_in = entries[4].get()
                check_out = entries[5].get()
                total_cost = entries[6].get()
                currency = entries[7].get()

                if not all([customer_id, vendor_id, country, category, check_in, check_out, total_cost, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE HOTELS SET CustomerID=?, VendorID=?, Country=?, Category=?, "
                    "CheckInDate=?, CheckOutDate=?, TotalCost=?, Currency=? "
                    "WHERE HotelID=?",
                    customer_id, vendor_id, country, category, check_in, check_out,
                    total_cost, currency, hotel_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Hotel booking updated successfully!")
                self.load_hotels()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update hotel booking: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_hotel(self):
        selected = self.hotels_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a hotel booking to delete!")
            return

        hotel_data = self.hotels_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete hotel booking {hotel_data[0]} for {hotel_data[1]}?"):
            try:
                self.cursor.execute("DELETE FROM HOTELS WHERE HotelID=?", hotel_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Hotel booking deleted successfully!")
                self.load_hotels()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete hotel booking: {str(e)}")

    def create_meals_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Meals")

        # Treeview for displaying meals
        self.meals_tree = ttk.Treeview(tab, columns=("MealID", "Customer", "Vendor", "ServiceType", "TotalCost", "Currency"), show="headings")
        self.meals_tree.heading("MealID", text="Meal ID")
        self.meals_tree.heading("Customer", text="Customer")
        self.meals_tree.heading("Vendor", text="Vendor ID")
        self.meals_tree.heading("ServiceType", text="Service Type")
        self.meals_tree.heading("TotalCost", text="Total Cost")
        self.meals_tree.heading("Currency", text="Currency")
        self.meals_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Meals", command=self.load_meals).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Meal", command=self.add_meal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Meal", command=self.update_meal_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Meal", command=self.delete_meal).pack(side=tk.LEFT, padx=5)

        self.load_meals()

    def load_meals(self):
        for item in self.meals_tree.get_children():
            self.meals_tree.delete(item)

        self.cursor.execute("""
                            SELECT m.MealID, c.FullName, m.VendorID, m.ServiceType, m.TotalCost, m.Currency
                            FROM MEALS m
                                     JOIN CUSTOMERS c ON m.CustomerID = c.CustomerID
                            """)
        for row in self.cursor.fetchall():
            self.meals_tree.insert("", tk.END, values=row)

    def add_meal_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Meal Service")

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]

        fields = [
            ("Customer:", "combobox", customer_options),
            ("Vendor ID:", "entry"),
            ("Service Type:", "combobox", ["Breakfast", "Lunch", "Dinner", "Full Board"]),
            ("Total Cost:", "entry"),
            ("Currency:", "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_meal():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                vendor_id = entries[1].get()
                service_type = entries[2].get()
                total_cost = entries[3].get()
                currency = entries[4].get()

                if not all([customer_id, vendor_id, service_type, total_cost, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO MEALS (MealID, CustomerID, VendorID, ServiceType, TotalCost, Currency) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    self.get_next_id("MEALS", "MealID"), customer_id, vendor_id, service_type, total_cost, currency
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Meal service added successfully!")
                self.load_meals()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add meal service: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_meal).grid(row=len(fields), columnspan=2, pady=10)

    def update_meal_dialog(self):
        selected = self.meals_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a meal service to update!")
            return

        meal_data = self.meals_tree.item(selected, "values")

        # Get full meal data
        self.cursor.execute("SELECT * FROM MEALS WHERE MealID=?", meal_data[0])
        full_data = self.cursor.fetchone()

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]
        current_customer = f"{full_data.CustomerID} - {meal_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Meal Service")

        fields = [
            ("Meal ID:", meal_data[0], "label"),
            ("Customer:", current_customer, "combobox", customer_options),
            ("Vendor ID:", full_data.VendorID, "entry"),
            ("Service Type:", full_data.ServiceType, "combobox", ["Breakfast", "Lunch", "Dinner", "Full Board"]),
            ("Total Cost:", full_data.TotalCost, "entry"),
            ("Currency:", full_data.Currency, "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                vendor_id = entries[1].get()
                service_type = entries[2].get()
                total_cost = entries[3].get()
                currency = entries[4].get()

                if not all([customer_id, vendor_id, service_type, total_cost, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE MEALS SET CustomerID=?, VendorID=?, ServiceType=?, TotalCost=?, Currency=? "
                    "WHERE MealID=?",
                    customer_id, vendor_id, service_type, total_cost, currency, meal_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Meal service updated successfully!")
                self.load_meals()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update meal service: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_meal(self):
        selected = self.meals_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a meal service to delete!")
            return

        meal_data = self.meals_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete meal service {meal_data[0]} for {meal_data[1]}?"):
            try:
                self.cursor.execute("DELETE FROM MEALS WHERE MealID=?", meal_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Meal service deleted successfully!")
                self.load_meals()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete meal service: {str(e)}")

    def create_transport_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Transport")

        # Treeview for displaying transport
        self.transport_tree = ttk.Treeview(tab, columns=("TransportID", "Customer", "Vendor", "Type", "TotalCost", "Currency"), show="headings")
        self.transport_tree.heading("TransportID", text="Transport ID")
        self.transport_tree.heading("Customer", text="Customer")
        self.transport_tree.heading("Vendor", text="Vendor ID")
        self.transport_tree.heading("Type", text="Transport Type")
        self.transport_tree.heading("TotalCost", text="Total Cost")
        self.transport_tree.heading("Currency", text="Currency")
        self.transport_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Transport", command=self.load_transport).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Transport", command=self.add_transport_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Transport", command=self.update_transport_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Transport", command=self.delete_transport).pack(side=tk.LEFT, padx=5)

        self.load_transport()

    def load_transport(self):
        for item in self.transport_tree.get_children():
            self.transport_tree.delete(item)

        self.cursor.execute("""
                            SELECT t.TransportID, c.FullName, t.VendorID, t.TransportType, t.TotalCost, t.Currency
                            FROM TRANSPORT t
                                     JOIN CUSTOMERS c ON t.CustomerID = c.CustomerID
                            """)
        for row in self.cursor.fetchall():
            self.transport_tree.insert("", tk.END, values=row)

    def add_transport_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Transport Booking")

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]

        fields = [
            ("Customer:", "combobox", customer_options),
            ("Vendor ID:", "entry"),
            ("Transport Type:", "combobox", ["Bus", "Car", "Train", "Boat", "Flight"]),
            ("Total Cost:", "entry"),
            ("Currency:", "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_transport():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                vendor_id = entries[1].get()
                transport_type = entries[2].get()
                total_cost = entries[3].get()
                currency = entries[4].get()

                if not all([customer_id, vendor_id, transport_type, total_cost, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO TRANSPORT (TransportID, CustomerID, VendorID, TransportType, TotalCost, Currency) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    self.get_next_id("TRANSPORT", "TransportID"), customer_id, vendor_id, transport_type, total_cost, currency
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Transport booking added successfully!")
                self.load_transport()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add transport booking: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_transport).grid(row=len(fields), columnspan=2, pady=10)

    def update_transport_dialog(self):
        selected = self.transport_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a transport booking to update!")
            return

        transport_data = self.transport_tree.item(selected, "values")

        # Get full transport data
        self.cursor.execute("SELECT * FROM TRANSPORT WHERE TransportID=?", transport_data[0])
        full_data = self.cursor.fetchone()

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]
        current_customer = f"{full_data.CustomerID} - {transport_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Transport Booking")

        fields = [
            ("Transport ID:", transport_data[0], "label"),
            ("Customer:", current_customer, "combobox", customer_options),
            ("Vendor ID:", full_data.VendorID, "entry"),
            ("Transport Type:", full_data.TransportType, "combobox", ["Bus", "Car", "Train", "Boat", "Flight"]),
            ("Total Cost:", full_data.TotalCost, "entry"),
            ("Currency:", full_data.Currency, "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                vendor_id = entries[1].get()
                transport_type = entries[2].get()
                total_cost = entries[3].get()
                currency = entries[4].get()

                if not all([customer_id, vendor_id, transport_type, total_cost, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE TRANSPORT SET CustomerID=?, VendorID=?, TransportType=?, TotalCost=?, Currency=? "
                    "WHERE TransportID=?",
                    customer_id, vendor_id, transport_type, total_cost, currency, transport_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Transport booking updated successfully!")
                self.load_transport()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update transport booking: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_transport(self):
        selected = self.transport_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a transport booking to delete!")
            return

        transport_data = self.transport_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete transport booking {transport_data[0]} for {transport_data[1]}?"):
            try:
                self.cursor.execute("DELETE FROM TRANSPORT WHERE TransportID=?", transport_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Transport booking deleted successfully!")
                self.load_transport()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete transport booking: {str(e)}")

    def create_visas_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Visas")

        # Treeview for displaying visas
        self.visas_tree = ttk.Treeview(tab, columns=("VisaID", "Customer", "Country", "AppDate", "Status", "Company"), show="headings")
        self.visas_tree.heading("VisaID", text="Visa ID")
        self.visas_tree.heading("Customer", text="Customer")
        self.visas_tree.heading("Country", text="Country")
        self.visas_tree.heading("AppDate", text="Application Date")
        self.visas_tree.heading("Status", text="Status")
        self.visas_tree.heading("Company", text="Processing Company")
        self.visas_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Visas", command=self.load_visas).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Visa", command=self.add_visa_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Visa", command=self.update_visa_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Visa", command=self.delete_visa).pack(side=tk.LEFT, padx=5)

        self.load_visas()

    def load_visas(self):
        for item in self.visas_tree.get_children():
            self.visas_tree.delete(item)

        self.cursor.execute("""
                            SELECT v.VisaID, c.FullName, v.Country, v.ApplicationDate, v.VisaStatus, v.ProcessingCompany
                            FROM VISAS v
                                     JOIN CUSTOMERS c ON v.CustomerID = c.CustomerID
                            """)
        for row in self.cursor.fetchall():
            self.visas_tree.insert("", tk.END, values=row)

    def add_visa_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Visa Application")

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]

        fields = [
            ("Customer:", "combobox", customer_options),
            ("Country:", "entry"),
            ("Application Date (YYYY-MM-DD):", "entry"),
            ("Visa Status:", "combobox", ["Applied", "Approved", "Rejected", "Processing"]),
            ("Processing Company:", "entry")
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_visa():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                country = entries[1].get()
                app_date = entries[2].get()
                status = entries[3].get()
                company = entries[4].get()

                if not all([customer_id, country, app_date, status, company]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO VISAS (VisaID, CustomerID, Country, ApplicationDate, VisaStatus, ProcessingCompany) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    self.get_next_id("VISAS", "VisaID"), customer_id, country, app_date, status, company
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Visa application added successfully!")
                self.load_visas()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add visa application: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_visa).grid(row=len(fields), columnspan=2, pady=10)

    def update_visa_dialog(self):
        selected = self.visas_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a visa application to update!")
            return

        visa_data = self.visas_tree.item(selected, "values")

        # Get full visa data
        self.cursor.execute("SELECT * FROM VISAS WHERE VisaID=?", visa_data[0])
        full_data = self.cursor.fetchone()

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]
        current_customer = f"{full_data.CustomerID} - {visa_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Visa Application")

        fields = [
            ("Visa ID:", visa_data[0], "label"),
            ("Customer:", current_customer, "combobox", customer_options),
            ("Country:", full_data.Country, "entry"),
            ("Application Date:", full_data.ApplicationDate, "entry"),
            ("Visa Status:", full_data.VisaStatus, "combobox", ["Applied", "Approved", "Rejected", "Processing"]),
            ("Processing Company:", full_data.ProcessingCompany, "entry")
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                country = entries[1].get()
                app_date = entries[2].get()
                status = entries[3].get()
                company = entries[4].get()

                if not all([customer_id, country, app_date, status, company]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE VISAS SET CustomerID=?, Country=?, ApplicationDate=?, VisaStatus=?, ProcessingCompany=? "
                    "WHERE VisaID=?",
                    customer_id, country, app_date, status, company, visa_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Visa application updated successfully!")
                self.load_visas()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update visa application: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_visa(self):
        selected = self.visas_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a visa application to delete!")
            return

        visa_data = self.visas_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete visa application {visa_data[0]} for {visa_data[1]}?"):
            try:
                self.cursor.execute("DELETE FROM VISAS WHERE VisaID=?", visa_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Visa application deleted successfully!")
                self.load_visas()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete visa application: {str(e)}")

    def create_syria_tickets_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Syria Tickets")

        # Treeview for displaying Syria tickets
        self.syria_tickets_tree = ttk.Treeview(tab, columns=("TicketID", "Customer", "Airline", "ServiceType", "PurchasePrice", "ProfitMargin", "Currency"), show="headings")
        self.syria_tickets_tree.heading("TicketID", text="Ticket ID")
        self.syria_tickets_tree.heading("Customer", text="Customer")
        self.syria_tickets_tree.heading("Airline", text="Airline")
        self.syria_tickets_tree.heading("ServiceType", text="Service Type")
        self.syria_tickets_tree.heading("PurchasePrice", text="Purchase Price")
        self.syria_tickets_tree.heading("ProfitMargin", text="Profit Margin")
        self.syria_tickets_tree.heading("Currency", text="Currency")
        self.syria_tickets_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Tickets", command=self.load_syria_tickets).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Ticket", command=self.add_syria_ticket_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Ticket", command=self.update_syria_ticket_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Ticket", command=self.delete_syria_ticket).pack(side=tk.LEFT, padx=5)

        self.load_syria_tickets()

    def load_syria_tickets(self):
        for item in self.syria_tickets_tree.get_children():
            self.syria_tickets_tree.delete(item)

        self.cursor.execute("""
                            SELECT s.TicketID, c.FullName, s.Airline, s.ServiceType, s.PurchasePrice, s.ProfitMargin, s.Currency
                            FROM SYRIATICKETS s
                                     JOIN CUSTOMERS c ON s.CustomerID = c.CustomerID
                            """)
        for row in self.cursor.fetchall():
            self.syria_tickets_tree.insert("", tk.END, values=row)

    def add_syria_ticket_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Syria Ticket")

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]

        fields = [
            ("Customer:", "combobox", customer_options),
            ("Airline:", "entry"),
            ("Service Type:", "combobox", ["One Way", "Round Trip"]),
            ("Purchase Price:", "entry"),
            ("Profit Margin:", "entry"),
            ("Currency:", "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_ticket():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                airline = entries[1].get()
                service_type = entries[2].get()
                purchase_price = entries[3].get()
                profit_margin = entries[4].get()
                currency = entries[5].get()

                if not all([customer_id, airline, service_type, purchase_price, profit_margin, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO SYRIATICKETS (TicketID, CustomerID, Airline, ServiceType, PurchasePrice, ProfitMargin, Currency) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    self.get_next_id("SYRIATICKETS", "TicketID"), customer_id, airline, service_type,
                    purchase_price, profit_margin, currency
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Syria ticket added successfully!")
                self.load_syria_tickets()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add Syria ticket: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_ticket).grid(row=len(fields), columnspan=2, pady=10)

    def update_syria_ticket_dialog(self):
        selected = self.syria_tickets_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a Syria ticket to update!")
            return

        ticket_data = self.syria_tickets_tree.item(selected, "values")

        # Get full ticket data
        self.cursor.execute("SELECT * FROM SYRIATICKETS WHERE TicketID=?", ticket_data[0])
        full_data = self.cursor.fetchone()

        # Get customers for dropdown
        self.cursor.execute("SELECT CustomerID, FullName FROM CUSTOMERS")
        customers = self.cursor.fetchall()
        customer_options = [f"{c[0]} - {c[1]}" for c in customers]
        current_customer = f"{full_data.CustomerID} - {ticket_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Syria Ticket")

        fields = [
            ("Ticket ID:", ticket_data[0], "label"),
            ("Customer:", current_customer, "combobox", customer_options),
            ("Airline:", full_data.Airline, "entry"),
            ("Service Type:", full_data.ServiceType, "combobox", ["One Way", "Round Trip"]),
            ("Purchase Price:", full_data.PurchasePrice, "entry"),
            ("Profit Margin:", full_data.ProfitMargin, "entry"),
            ("Currency:", full_data.Currency, "combobox", ["USD", "EUR", "GBP", "SAR"])
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                customer_id = entries[0].get().split(" - ")[0]
                airline = entries[1].get()
                service_type = entries[2].get()
                purchase_price = entries[3].get()
                profit_margin = entries[4].get()
                currency = entries[5].get()

                if not all([customer_id, airline, service_type, purchase_price, profit_margin, currency]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE SYRIATICKETS SET CustomerID=?, Airline=?, ServiceType=?, PurchasePrice=?, ProfitMargin=?, Currency=? "
                    "WHERE TicketID=?",
                    customer_id, airline, service_type, purchase_price, profit_margin, currency, ticket_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Syria ticket updated successfully!")
                self.load_syria_tickets()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update Syria ticket: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_syria_ticket(self):
        selected = self.syria_tickets_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a Syria ticket to delete!")
            return

        ticket_data = self.syria_tickets_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete Syria ticket {ticket_data[0]} for {ticket_data[1]}?"):
            try:
                self.cursor.execute("DELETE FROM SYRIATICKETS WHERE TicketID=?", ticket_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Syria ticket deleted successfully!")
                self.load_syria_tickets()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete Syria ticket: {str(e)}")

    def create_expenses_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Expenses")

        # Treeview for displaying expenses
        self.expenses_tree = ttk.Treeview(tab, columns=("ExpenseID", "Group", "Category", "Amount", "Currency", "Date", "Description"), show="headings")
        self.expenses_tree.heading("ExpenseID", text="Expense ID")
        self.expenses_tree.heading("Group", text="Group ID")
        self.expenses_tree.heading("Category", text="Category")
        self.expenses_tree.heading("Amount", text="Amount")
        self.expenses_tree.heading("Currency", text="Currency")
        self.expenses_tree.heading("Date", text="Date")
        self.expenses_tree.heading("Description", text="Description")
        self.expenses_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Expenses", command=self.load_expenses).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Expense", command=self.add_expense_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Expense", command=self.update_expense_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Expense", command=self.delete_expense).pack(side=tk.LEFT, padx=5)

        self.load_expenses()

    def load_expenses(self):
        for item in self.expenses_tree.get_children():
            self.expenses_tree.delete(item)

        self.cursor.execute("""
                            SELECT e.ExpenseID, e.GroupID, e.Category, e.Amount, e.Currency, e.Date, e.Description
                            FROM EXPENSES e
                            """)
        for row in self.cursor.fetchall():
            self.expenses_tree.insert("", tk.END, values=row)

    def add_expense_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Expense")

        # Get groups for dropdown
        self.cursor.execute("SELECT GroupID, GroupName FROM TRAVELGROUPS")
        groups = self.cursor.fetchall()
        group_options = [f"{g[0]} - {g[1]}" for g in groups]

        fields = [
            ("Group:", "combobox", group_options),
            ("Category:", "entry"),
            ("Amount:", "entry"),
            ("Currency:", "combobox", ["USD", "EUR", "GBP", "SAR"]),
            ("Date (YYYY-MM-DD):", "entry"),
            ("Description:", "entry")
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_expense():
            try:
                group_id = entries[0].get().split(" - ")[0]
                category = entries[1].get()
                amount = entries[2].get()
                currency = entries[3].get()
                date = entries[4].get()
                description = entries[5].get()

                if not all([group_id, category, amount, currency, date]):
                    messagebox.showerror("Error", "All fields except Description are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO EXPENSES (ExpenseID, GroupID, Category, Amount, Currency, Date, Description) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    self.get_next_id("EXPENSES", "ExpenseID"), group_id, category, amount, currency, date, description
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Expense added successfully!")
                self.load_expenses()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add expense: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_expense).grid(row=len(fields), columnspan=2, pady=10)

    def update_expense_dialog(self):
        selected = self.expenses_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select an expense to update!")
            return

        expense_data = self.expenses_tree.item(selected, "values")

        # Get full expense data
        self.cursor.execute("SELECT * FROM EXPENSES WHERE ExpenseID=?", expense_data[0])
        full_data = self.cursor.fetchone()

        # Get groups for dropdown
        self.cursor.execute("SELECT GroupID, GroupName FROM TRAVELGROUPS")
        groups = self.cursor.fetchall()
        group_options = [f"{g[0]} - {g[1]}" for g in groups]
        current_group = f"{full_data.GroupID} - {expense_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Expense")

        fields = [
            ("Expense ID:", expense_data[0], "label"),
            ("Group:", current_group, "combobox", group_options),
            ("Category:", full_data.Category, "entry"),
            ("Amount:", full_data.Amount, "entry"),
            ("Currency:", full_data.Currency, "combobox", ["USD", "EUR", "GBP", "SAR"]),
            ("Date:", full_data.Date, "entry"),
            ("Description:", full_data.Description, "entry")
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                group_id = entries[0].get().split(" - ")[0]
                category = entries[1].get()
                amount = entries[2].get()
                currency = entries[3].get()
                date = entries[4].get()
                description = entries[5].get()

                if not all([group_id, category, amount, currency, date]):
                    messagebox.showerror("Error", "All fields except Description are required!")
                    return

                self.cursor.execute(
                    "UPDATE EXPENSES SET GroupID=?, Category=?, Amount=?, Currency=?, Date=?, Description=? "
                    "WHERE ExpenseID=?",
                    group_id, category, amount, currency, date, description, expense_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Expense updated successfully!")
                self.load_expenses()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update expense: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_expense(self):
        selected = self.expenses_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select an expense to delete!")
            return

        expense_data = self.expenses_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete expense {expense_data[0]}?"):
            try:
                self.cursor.execute("DELETE FROM EXPENSES WHERE ExpenseID=?", expense_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Expense deleted successfully!")
                self.load_expenses()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete expense: {str(e)}")

    def create_reports_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Profit Reports")

        # Treeview for displaying reports
        self.reports_tree = ttk.Treeview(tab, columns=("ReportID", "Group", "Month", "Year", "Revenue", "Expense", "Profit"), show="headings")
        self.reports_tree.heading("ReportID", text="Report ID")
        self.reports_tree.heading("Group", text="Group ID")
        self.reports_tree.heading("Month", text="Month")
        self.reports_tree.heading("Year", text="Year")
        self.reports_tree.heading("Revenue", text="Total Revenue")
        self.reports_tree.heading("Expense", text="Total Expense")
        self.reports_tree.heading("Profit", text="Net Profit")
        self.reports_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load Reports", command=self.load_reports).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Add Report", command=self.add_report_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update Report", command=self.update_report_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Report", command=self.delete_report).pack(side=tk.LEFT, padx=5)

        self.load_reports()

    def load_reports(self):
        for item in self.reports_tree.get_children():
            self.reports_tree.delete(item)

        self.cursor.execute("""
                            SELECT pr.ReportID, pr.GroupID, pr.Month, pr.Year, pr.TotalRevenue, pr.TotalExpense, pr.NetProfit
                            FROM PROFITREPORTS pr
                            """)
        for row in self.cursor.fetchall():
            self.reports_tree.insert("", tk.END, values=row)

    def add_report_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Profit Report")

        # Get groups for dropdown
        self.cursor.execute("SELECT GroupID, GroupName FROM TRAVELGROUPS")
        groups = self.cursor.fetchall()
        group_options = [f"{g[0]} - {g[1]}" for g in groups]

        fields = [
            ("Group:", "combobox", group_options),
            ("Month:", "combobox", ["January", "February", "March", "April", "May", "June",
                                    "July", "August", "September", "October", "November", "December"]),
            ("Year:", "entry"),
            ("Total Revenue:", "entry"),
            ("Total Expense:", "entry"),
            ("Net Profit:", "entry")
        ]

        entries = []
        for i, (label, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_report():
            try:
                group_id = entries[0].get().split(" - ")[0]
                month = entries[1].get()
                year = entries[2].get()
                revenue = entries[3].get()
                expense = entries[4].get()
                profit = entries[5].get()

                if not all([group_id, month, year, revenue, expense, profit]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "INSERT INTO PROFITREPORTS (ReportID, GroupID, Month, Year, TotalRevenue, TotalExpense, NetProfit) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?)",
                    self.get_next_id("PROFITREPORTS", "ReportID"), group_id, month, year, revenue, expense, profit
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Profit report added successfully!")
                self.load_reports()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add profit report: {str(e)}")

        ttk.Button(dialog, text="Save", command=save_report).grid(row=len(fields), columnspan=2, pady=10)

    def update_report_dialog(self):
        selected = self.reports_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a report to update!")
            return

        report_data = self.reports_tree.item(selected, "values")

        # Get full report data
        self.cursor.execute("SELECT * FROM PROFITREPORTS WHERE ReportID=?", report_data[0])
        full_data = self.cursor.fetchone()

        # Get groups for dropdown
        self.cursor.execute("SELECT GroupID, GroupName FROM TRAVELGROUPS")
        groups = self.cursor.fetchall()
        group_options = [f"{g[0]} - {g[1]}" for g in groups]
        current_group = f"{full_data.GroupID} - {report_data[1]}"

        dialog = tk.Toplevel(self.root)
        dialog.title("Update Profit Report")

        fields = [
            ("Report ID:", report_data[0], "label"),
            ("Group:", current_group, "combobox", group_options),
            ("Month:", full_data.Month, "combobox", ["January", "February", "March", "April", "May", "June",
                                                     "July", "August", "September", "October", "November", "December"]),
            ("Year:", full_data.Year, "entry"),
            ("Total Revenue:", full_data.TotalRevenue, "entry"),
            ("Total Expense:", full_data.TotalExpense, "entry"),
            ("Net Profit:", full_data.NetProfit, "entry")
        ]

        entries = []
        for i, (label, value, field_type, *options) in enumerate(fields):
            tk.Label(dialog, text=label).grid(row=i, column=0, padx=5, pady=5)

            if field_type == "label":
                tk.Label(dialog, text=value).grid(row=i, column=1, padx=5, pady=5)
            elif field_type == "entry":
                entry = ttk.Entry(dialog)
                entry.insert(0, value)
                entry.grid(row=i, column=1, padx=5, pady=5)
                entries.append(entry)
            elif field_type == "combobox":
                combo = ttk.Combobox(dialog, values=options[0])
                combo.set(value)
                combo.grid(row=i, column=1, padx=5, pady=5)
                entries.append(combo)

        def save_changes():
            try:
                group_id = entries[0].get().split(" - ")[0]
                month = entries[1].get()
                year = entries[2].get()
                revenue = entries[3].get()
                expense = entries[4].get()
                profit = entries[5].get()

                if not all([group_id, month, year, revenue, expense, profit]):
                    messagebox.showerror("Error", "All fields are required!")
                    return

                self.cursor.execute(
                    "UPDATE PROFITREPORTS SET GroupID=?, Month=?, Year=?, TotalRevenue=?, TotalExpense=?, NetProfit=? "
                    "WHERE ReportID=?",
                    group_id, month, year, revenue, expense, profit, report_data[0]
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Profit report updated successfully!")
                self.load_reports()
                dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update profit report: {str(e)}")

        ttk.Button(dialog, text="Save Changes", command=save_changes).grid(row=len(fields), columnspan=2, pady=10)

    def delete_report(self):
        selected = self.reports_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a report to delete!")
            return

        report_data = self.reports_tree.item(selected, "values")

        if messagebox.askyesno("Confirm", f"Delete profit report {report_data[0]}?"):
            try:
                self.cursor.execute("DELETE FROM PROFITREPORTS WHERE ReportID=?", report_data[0])
                self.conn.commit()
                messagebox.showinfo("Success", "Profit report deleted successfully!")
                self.load_reports()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete profit report: {str(e)}")

    def create_history_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="History Log")

        # Treeview for displaying history log
        self.history_tree = ttk.Treeview(tab, columns=("LogID", "Table", "Action", "Date", "User"), show="headings")
        self.history_tree.heading("LogID", text="Log ID")
        self.history_tree.heading("Table", text="Table")
        self.history_tree.heading("Action", text="Action")
        self.history_tree.heading("Date", text="Date")
        self.history_tree.heading("User", text="User")
        self.history_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Details frame
        details_frame = ttk.Frame(tab)
        details_frame.pack(fill='x', padx=10, pady=5)

        self.details_text = tk.Text(details_frame, height=10, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(details_frame, orient="vertical", command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=scrollbar.set)

        self.details_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons frame
        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Load History", command=self.load_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Details", command=self.view_history_details).pack(side=tk.LEFT, padx=5)

        self.load_history()

    def load_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        self.cursor.execute("SELECT LogID, TableName, ActionType, ActionDate, PerformedBy FROM DB_HISTORY_LOG ORDER BY ActionDate DESC")
        for row in self.cursor.fetchall():
            self.history_tree.insert("", tk.END, values=row)

    def view_history_details(self):
        selected = self.history_tree.focus()
        if not selected:
            messagebox.showerror("Error", "Please select a log entry to view details!")
            return

        log_data = self.history_tree.item(selected, "values")

        self.cursor.execute("SELECT RecordData FROM DB_HISTORY_LOG WHERE LogID=?", log_data[0])
        record_data = self.cursor.fetchone()[0]

        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, json.dumps(json.loads(record_data), indent=4))

    def get_next_id(self, table_name, id_column):
        self.cursor.execute(f"SELECT MAX({id_column}) FROM {table_name}")
        max_id = self.cursor.fetchone()[0]
        return 1 if max_id is None else max_id + 1

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToursTravelsApp(root)
    app.run()