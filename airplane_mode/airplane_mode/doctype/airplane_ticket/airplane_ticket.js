// Copyright (c) 2025, Kashif Shaikh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Airplane Ticket', {
    refresh: function(frm) {
        frm.set_df_property('seat', 'hidden', 0);

        frm.add_custom_button(__('Assign Seat'), function() {
            const dialog = new frappe.ui.Dialog({
                title: __('Assign Seat'),
                fields: [
                    {
                        label: __('Seat Number'),
                        fieldname: 'seat',
                        fieldtype: 'Data',
                        reqd: 1,
                        default: frm.doc.seat || ''
                    }
                ],
                primary_action_label: __('Assign'),
                primary_action(values) {
                    if (!values.seat) {
                        frappe.msgprint(__('Please enter a seat number.'));
                        return;
                    }
                    frm.set_value('seat', values.seat);

                    frappe.show_alert({
                        message: __('Seat updated to {0}', [values.seat]),
                        indicator: 'green'
                    });
                    dialog.hide();
                    frm.save();
                }
            });

            dialog.show();
        }, __('Actions'));
    }
});
