# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import datetime


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"


    retirement_ids = fields.One2many('employee.retirement', 'employee_id', string='Retirement')


# Your Python code (e.g., in a controller or model)

class EmployeeRetirement(models.Model):
    _name = 'employee.retirement'
    _description = 'Employee Retirement'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')

    retirement_type_id = fields.Many2one('employee.retirement.type', string="Retirement Type")
    retirement_reason_id = fields.Many2one('employee.retirement.reason', string="Retirement Reason")
    retirement_end_date = fields.Date(string='End Date')
    retirement_remarks = fields.Text(string='Remarks')

    retirement_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Retirement Month",
        compute="_compute_retirement_year_month",
        store=True
    )

    retirement_year = fields.Selection(
        selection=lambda self: [(str(y), str(y)) for y in
                                range(datetime.date.today().year - 30,
                                      datetime.date.today().year + 10)],
        string="Retirement Year",
        compute="_compute_retirement_year_month",
        store=True
    )

    @api.depends('retirement_end_date')
    def _compute_retirement_year_month(self):
        for rec in self:
            if rec.retirement_end_date:
                rec.retirement_month = str(rec.retirement_end_date.month)
                rec.retirement_year = str(rec.retirement_end_date.year)
            else:
                rec.retirement_month = False
                rec.retirement_year = False



class EmployeeRetirementReason(models.Model):
    _name = 'employee.retirement.reason'
    _description = 'Employee Reason'

    name = fields.Char(string='Reason')

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            if not record.name.replace(" ", "").isalpha():
                raise ValidationError("The Retirement Reason should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Retirement Reason must be unique! and should not be duplicated!")



class EmployeeRetirementType(models.Model):
    _name = 'employee.retirement.type'
    _description = 'Employee Retirement Type'

    name = fields.Char(string='Retirement Type')

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            if not record.name.replace(" ", "").isalpha():
                raise ValidationError("The Retirement Type should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Retirement Type must be unique! and should not be duplicated!")




