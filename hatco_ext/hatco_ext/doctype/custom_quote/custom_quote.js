// Copyright (c) 2026, Aravind R and contributors
// For license information, please see license.txt


//Set valid till date to 30 days from posting date
frappe.ui.form.on("Custom Quote", {
    onload(frm) {
        if (frm.is_new()) {
            if (!frm.doc.posting_date) {
                frm.set_value(
                    "posting_date",
                    frappe.datetime.now_datetime()
                );
            }
            if (!frm.doc.valid_till) {
                let posting_date = frm.doc.posting_date || frappe.datetime.now_datetime();

                let valid_till = frappe.datetime.add_days(
                    posting_date,
                    30
                );

                frm.set_value("valid_till", valid_till);
            }
        }
    }
});

