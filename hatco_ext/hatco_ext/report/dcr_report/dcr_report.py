# Copyright (c) 2026, Aravind R and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Type"),
            "fieldname": "type",
            "fieldtype": "Data",
            "width": 350
        },
        {
            "label": _("Total"),
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("Invoice"),
            "fieldname": "invoice_count",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 0,
            "hidden": 1
        },
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 0,
            "hidden": 1
        }
    ]


def get_data(filters):
    filters = filters or {}
    date = filters.get("date")
    type_filter = filters.get("type")

    types = [
        "Cash Sales",
        "Card Sales",
        "Credit Sales",
        "Cash Purchases",
        "Card Purchases",
        "Credit Purchases",
        "Sales Return",
        "Purchase Return",
        "Customer Receipts",
        "Supplier Payments",
        "Bank Receipts",
        "Bank Payments",
        "Cash Receipts",
        "Cash Payments",
        "Journal Entry",
    ]

    # If type filter is selected, show only that type
    if type_filter:
        types = [type_filter]

    result = []

    for t in types:
        conditions = ""
        params = []

        
        if date:
            conditions += " AND posting_date = %s"
            params.append(date)

        # Voucher type conditions
        if t in ["Cash Sales", "Card Sales", "Credit Sales"]:
            conditions += " AND voucher_type = 'Sales Invoice'"

        elif t in ["Cash Purchases", "Card Purchases", "Credit Purchases"]:
            conditions += " AND voucher_type = 'Purchase Invoice'"

        elif t == "Sales Return":
            conditions += " AND voucher_type = 'Sales Invoice'"

        elif t == "Purchase Return":
            conditions += " AND voucher_type = 'Purchase Invoice'"

        elif t in ["Customer Receipts", "Bank Receipts", "Cash Receipts"]:
            conditions += " AND voucher_type = 'Payment Entry'"

        elif t in ["Supplier Payments", "Bank Payments", "Cash Payments"]:
            conditions += " AND voucher_type = 'Payment Entry'"

        elif t == "Journal Entry":
            conditions += " AND voucher_type = 'Journal Entry'"

        # Report
        summary = frappe.db.sql(f"""
            SELECT
                COALESCE(SUM(debit), 0) as total,
                COUNT(DISTINCT voucher_no) as invoice_count
            FROM `tabGL Entry`
            WHERE docstatus = 1
            {conditions}
        """, tuple(params), as_dict=True)

        total = summary[0]["total"] if summary else 0
        count = summary[0]["invoice_count"] if summary else 0

        result.append({
            "type": t,
            "total": total,
            "invoice_count": count,
            "indent": 0
        })

        # Invoices
        invoices = frappe.db.sql(f"""
            SELECT
                voucher_type,
                voucher_no,
                SUM(debit) as amount
            FROM `tabGL Entry`
            WHERE docstatus = 1
            {conditions}
            GROUP BY voucher_type, voucher_no
        """, tuple(params), as_dict=True)

        for inv in invoices:
            result.append({
                "type": f"{inv['voucher_type']} {inv['voucher_no']}",
                "total": inv["amount"],
                "invoice_count": "",
                "indent": 1,
                "voucher_type": inv['voucher_type'],
                "voucher_no": inv['voucher_no']
            })

    return result