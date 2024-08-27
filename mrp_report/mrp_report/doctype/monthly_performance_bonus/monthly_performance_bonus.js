// Copyright (c) 2024, vivek.kumbhar@erpdata.in and contributors
// For license information, please see license.txt

frappe.ui.form.on('Monthly Performance Bonus', {
	// refresh: function(frm) {

	// }
});
// frappe.ui.form.on("Monthly Performance Bonus Details", {
// 	result_weightage:function(frm, cdt, cdn){
// 	var d = locals[cdt][cdn];
// 	var total1 = 0;
// 	frm.doc.items.forEach(function(d) { total1 += d.result_weightage; 

// 	});
// 	frm.set_value("bonus_per", total1);
// 	refresh_field("bonus_per");
//   },
//    items_remove:function(frm, cdt, cdn){
// 	var d = locals[cdt][cdn];
// 	var total1 = 0;
// 	frm.doc.items.forEach(function(d) { total1 += d.result_weightage; });
// 	frm.set_value("bonus_per", total1);
// 	refresh_field("bonus_per");
//    }
//  });

frappe.ui.form.on("Monthly Performance Bonus Details", {
	result_weightage: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total1 = 0;
        var weightageExceeded = false;
        frm.doc.items.forEach(function(item) {
            total1 += item.result_weightage;
            if (item.result_weightage > item.total_weightage) {
                weightageExceeded = true;
            }
        });

        if (total1 > frm.doc.max_bonus) {
            frappe.msgprint(__('The total result weightage ({0}) exceeds the maximum % of Bonus ({1}).', [total1, frm.doc.max_bonus]));
        }

        if (weightageExceeded) {
            frappe.msgprint(__('Result Weightage should not be greater than Total Weightage'));
        }

        frm.set_value("bonus_per", total1);
        refresh_field("bonus_per");
    },
    items_remove: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total1 = 0;

        frm.doc.items.forEach(function(d) {
            total1 += d.result_weightage;
        });

        frm.set_value("bonus_per", total1);
        refresh_field("bonus_per");
    }
});

frappe.ui.form.on("Monthly Performance Bonus Details", {
    total_weightage: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        var total1 = 0;
     
        frm.doc.items.forEach(function(d) {
            total1 += d.total_weightage;
        });
        
        if (total1 > frm.doc.max_bonus) {
            frappe.msgprint(__('The total result weightage ({0}) exceeds the maximum % of Bonus ({1}).', [total1, frm.doc.max_bonus]));
        }
    }
});


frappe.ui.form.on('Monthly Performance Bonus Details', {
	result_weightage: function(frm) {
		frm.call({
			method:'bonus_calculate',
			doc:frm.doc
		})
	}
});