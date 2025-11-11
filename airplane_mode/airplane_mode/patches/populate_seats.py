import frappe
import random
import string

def execute():
    tickets = frappe.get_all("Airplane Ticket", filters={"seat": ["is", "not set"]}, fields=["name"])

    for ticket in tickets:
        seat = f"{random.randint(1, 99)}{random.choice(string.ascii_uppercase[:5])}"

        frappe.db.set_value("Airplane Ticket", ticket.name, "seat", seat)

    frappe.db.commit()
    frappe.logger().info(f"Populated seats for {len(tickets)} existing Airplane Ticket records.")
airplane_mode/airplane_mode/patches