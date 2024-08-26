// Copyright (c) 2024, vivek.kumbhar@erpdata.in and contributors
// For license information, please see license.txt

frappe.ui.form.on('OT Monthly Sheet', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on('OT Monthly Sheet', {
	from_date: function (frm) {
		frm.call({
			method:"get_month_dates",
			doc:frm.doc,
			args:{
				"input_date":frm.doc.from_date
			}
		})
	}
});
frappe.ui.form.on('OT Monthly Sheet', {
	to_date: function (frm) {
		frm.call({
			method:"get_month_dates",
			doc:frm.doc,
			args:{
				"input_date":frm.doc.to_date
			}
		})
	}
});
frappe.ui.form.on('OT Monthly Sheet Details', {
	employee: function(frm) {
		frm.call({
			method:'get_salary_comp',
			doc:frm.doc
		})
	}
});

frappe.ui.form.on('OT Monthly Sheet Details', {
	ot_hrs: function(frm) {
		frm.call({
			method:'overtime_calculate',
			doc:frm.doc
		})
	}
});