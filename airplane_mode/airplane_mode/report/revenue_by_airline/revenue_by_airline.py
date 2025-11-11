# Copyright (c) 2025, Kashif Shaikh and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns = [
		{
			"fieldname": "airline",
			"label": "Airline",
			"fieldtype": "Link",
			"options": "Airline"
		},
		{
			"fieldname": "revenue",
			"label": "Revenue",
			"fieldtype": "Currency",
			"options": "INR"
		},
	]

	tickets = frappe.get_all("Airplane Ticket", fields=["total_amount", "flight"])
	print ("***********ticket*********",tickets)

	airlines = frappe.get_all("Airline", pluck="name")
	print ("***********airlines*********",airlines)

	revenue_by_airline = {airline: 0 for airline in airlines}
	print ("***********revenue_by_airline*********",revenue_by_airline)

	for t in tickets:
		if not t.flight:
			continue

		airplane = frappe.get_value("Airplane Flight", t.flight, "airplane")

		airline = frappe.get_value("Airplane", airplane, "airline")

		if airline in revenue_by_airline:
			revenue_by_airline[airline] += t.total_amount

	data = [{"airline": k, "revenue": v} for k, v in revenue_by_airline.items()]
	print ("***********data*********",data)

	chart = {
		"data": {
			"labels": [d["airline"] for d in data],
			"datasets": [{"name": "Revenue By Airline", "values": [d["revenue"] for d in data]}],
		},
		"type": "donut",
	}

	total_revenue = sum(d["revenue"] for d in data)
	summary = [{
		"label": "Total Revenue",
		"value": total_revenue,
		"indicator": "Green" if total_revenue > 0 else "Red"
	}]

	return columns, data, None, chart, summary
