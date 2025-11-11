# Copyright (c) 2025, Kashif Shaikh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class FlightPassenger(Document):
    def before_save(doc):
        if doc.last_name:
            doc.full_name = f"{doc.first_name} {doc.last_name}"
        else:
            doc.full_name = doc.first_name


