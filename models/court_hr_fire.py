# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import datetime

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    fire_ids = fields.One2many('employee.fire', 'employee_id', string='Fire')


# Your Python code (e.g., in a controller or model)

class EmployeeFire(models.Model):
    _name = 'employee.fire'
    _description = 'Employee Fire'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')

    fire_type = fields.Many2one('employee.fire.type', string='Fire Type', Tracking='true')
    leave_reason = fields.Many2one('employee.leave.reason', string='reason for leaving the job', Tracking='true')

    order_date = fields.Date(string='Order Date', Tracking='true')
    order_no = fields.Integer(string='Order No', Tracking='true')
    date_approved = fields.Date(string='Date Approved', Tracking='true')
    fire_remarks = fields.Text(string='Remarks', Tracking='true')

    attachments = fields.Many2many('ir.attachment', string="Attachments")

    # Month & Year for filtering
    fire_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Month",
        compute="_compute_fire_year_month",
        store=True
    )

    fire_year = fields.Selection(
        selection=lambda self: [(str(y), str(y)) for y in
                                range(datetime.date.today().year - 30,
                                      datetime.date.today().year + 10)],
        string="Year",
        compute="_compute_fire_year_month",
        store=True
    )

    @api.depends('date_approved')
    def _compute_fire_year_month(self):
        for rec in self:
            if rec.date_approved:
                rec.fire_month = str(rec.date_approved.month)
                rec.fire_year = str(rec.date_approved.year)
            else:
                rec.fire_month = False
                rec.fire_year = False


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

