# Copyright (c) 2025, Kashif Shaikh and contributors
# For license information, please see license.txt

import frappe
import random
from frappe.model.document import Document


class AirplaneTicket(Document):

    def before_insert(doc):
        doc.check_flight_capacity()
        doc.set_seat()

    def set_seat(doc):
        seat_number = random.randint(1, 99)
        seat_letter = random.choice(['A', 'B', 'C', 'D', 'E'])
        doc.seat = f"{seat_number}{seat_letter}"

    def validate(doc):
        doc.remove_duplicate_addons()
        doc.calculate_total_amount()

    def remove_duplicate_addons(doc):
        unique_addons = {}
        clean_addons = []
        removed_items = []

        for addon in doc.add_on:
            if addon.item not in unique_addons:
                unique_addons[addon.item] = True
                clean_addons.append(addon)
            else:
                removed_items.append(addon.item)

        doc.add_on = clean_addons

        if removed_items:
            frappe.throw(f"Duplicate add-ons removed: {', '.join(removed_items)}")

    def calculate_total_amount(doc):
        addons_total = sum(addon.amount for addon in doc.add_on)
        doc.total_amount = (doc.flight_price or 0) + addons_total

    def check_flight_capacity(doc):
        if not doc.flight:
            frappe.throw("Please select a Flight before creating a ticket.")

        airplane = frappe.db.get_value("Airplane Flight", doc.flight, "airplane")
        if not airplane:
            frappe.throw(f"The selected flight {doc.flight} has no airplane assigned.")

        capacity = frappe.db.get_value("Airplane", airplane, "capacity") or 0

        current_tickets = frappe.db.count(
            "Airplane Ticket",
            filters={
                "flight": doc.flight,
                "docstatus": ["!=", 2]  
            }
        )

        if current_tickets >= capacity:
            frappe.throw(
                f"Cannot create ticket: Airplane capacity ({capacity}) for flight '{doc.flight}' is full."
            )


def prevent_unboarded_submission(doc, method):
    if doc.status != "Boarded":
        frappe.throw("You can only submit the ticket if the status is 'Boarded'.")
