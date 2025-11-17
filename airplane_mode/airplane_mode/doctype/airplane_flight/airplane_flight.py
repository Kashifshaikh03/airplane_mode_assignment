# Copyright (c) 2025, Kashif Shaikh and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils.background_jobs import enqueue


class AirplaneFlight(WebsiteGenerator):

	def on_submit(doc):
		doc.status = "Completed"
		frappe.db.set_value("Airplane Flight", doc.name, "status", "Completed")

	def on_update(doc):
		enqueue(update_ticket_gate_numbers, flight=doc.name, gate=doc.gate_number)

def update_ticket_gate_numbers(flight, gate):
	
	tickets = frappe.get_all("Airplane Ticket", filters={"flight": flight}, fields=["name"])
	for ticket in tickets:
		frappe.db.set_value("Airplane Ticket", ticket.name, "gate_number", gate)
	frappe.db.commit()
