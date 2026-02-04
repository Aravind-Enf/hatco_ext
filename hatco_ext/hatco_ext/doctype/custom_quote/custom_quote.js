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

frappe.ui.form.on("Custom Quote Item", {

    qty(frm, cdt, cdn) {
        calculate_values(cdt, cdn);
    },

    rate(frm, cdt, cdn) {
        calculate_values(cdt, cdn);
    },

    tax_rate(frm, cdt, cdn) {
        calculate_values(cdt, cdn);
    }
});

function calculate_values(cdt, cdn) {
    let row = locals[cdt][cdn];

    let qty = row.qty || 0;
    let rate = row.rate || 0;
    let tax_rate = row.tax_rate || 0;

    //value automaticaly set
    let total = qty * rate;
    let vat = (total * tax_rate) / 100;
    let total_incl_vat = total + vat;

    frappe.model.set_value(cdt, cdn, "total", total);
    frappe.model.set_value(cdt, cdn, "vat", vat);
    frappe.model.set_value(cdt, cdn, "total_incl_vat", total_incl_vat);
}
