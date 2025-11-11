# Copyright (c) 2025, Kashif Shaikh and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document

class AirplaneFlight(WebsiteGenerator):
	
	def on_submit(doc):
		doc.status = "Completed"
		frappe.db.set_value("Airplane Flight", doc.name, "status", "Completed")
	
