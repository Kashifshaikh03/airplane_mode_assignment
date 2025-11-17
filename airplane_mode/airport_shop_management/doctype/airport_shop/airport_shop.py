# Copyright (c) 2025, Kashif Shaikh and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.utils import today


class AirportShop(WebsiteGenerator):
    def validate(doc):
        if doc.is_occupied:
            doc.status = "Occupied"
        else:
            doc.status = "Available" 

        if doc.shop_type:
            enabled = frappe.db.get_value("Shop Type", doc.shop_type, "enabled")
            if not enabled:
                frappe.throw("Selected Shop Type is disabled. Please choose an enabled type.")


def send_rent_due_reminders():
    settings = frappe.get_single("Airport Shop Settings")
    if not settings.enable_rent_reminders:
        frappe.logger().info("Rent reminders disabled in Airport Shop Settings.")
        return

    shops = frappe.get_all(
        "Airport Shop",
        filters={"is_occupied": 1},
        fields=["shop_name", "tenant_name", "tenant_email", "rent_amount"]
    )

    for shop in shops:
        if not shop.tenant_email:
            continue

        frappe.sendmail(
            recipients=[shop.tenant_email],
            subject=f"Monthly Rent Reminder - {shop.shop_name}",
            message=f"""
                <p>Dear {shop.tenant_name},</p>
                <p>This is a reminder that your rent of <b>₹{shop.rent_amount}</b> 
                is due for {frappe.utils.formatdate(today(), "MMMM yyyy")}.</p>
                <p>Kindly make the payment at your earliest convenience.</p>
                <p>Regards,<br>Airport Management Team</p>
            """
        )

    frappe.logger().info(f"Sent rent reminders to {len(shops)} tenants.")