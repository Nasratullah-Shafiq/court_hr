# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    promotion_ids = fields.One2many('employee.promotions', 'employee_id', string='Fire')


# Your Python code (e.g., in a controller or model)

class EmployeePromotion(models.Model):
    _name = 'employee.promotions'
    _description = 'Employee Promotions'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    approval_no = fields.Char(string='Approval No', Tracking='true')
    proposal_no = fields.Char(string='Proposal No', Tracking='true')

    rank_promotion = fields.Char(string='Rand Promotion', Tracking='true')

    order_date = fields.Date(string='Order Date', Tracking='true')
    order_no = fields.Integer(string='Order No', Tracking='true')
    approved_date = fields.Date(string='Date Approved', Tracking='true')
    proposal_date = fields.Date(string='Date Approved', Tracking='true')
    fire_remarks = fields.Text(string='Remarks', Tracking='true')

    attachments = fields.Many2many('ir.attachment', string="Attachments")


    class EmployeeLeaveReason(models.Model):
        _name = 'employee.leave.reason'
        _description = 'Employee Document Type'
        name = fields.Char(string='Document Type')

        @api.constrains('name')
        def _check_name_constraints(self):
            for record in self:
                # Ensure the name contains only letters and spaces
                if not record.name.replace(" ", "").isalpha():
                    raise ValidationError("The Leave Reason should only contain letters and spaces.")

                # Check for duplicates at the application level
                if self.search_count([('name', '=', record.name)]) > 1:
                    raise ValidationError("The Leave Reason must be unique! and should not be duplicated!")

    class EmployeeFireType(models.Model):
        _name = 'employee.fire.type'
        _description = 'Employee Fire Type'

        name = fields.Char(string='Document Type')

        @api.constrains('name')
        def _check_name_constraints(self):
            for record in self:
                # Ensure the name contains only letters and spaces
                if not record.name.replace(" ", "").isalpha():
                    raise ValidationError("The Fire Type should only contain letters and spaces.")

                # Check for duplicates at the application level
                if self.search_count([('name', '=', record.name)]) > 1:
                    raise ValidationError("The Fire Type must be unique! and should not be duplicated!")

