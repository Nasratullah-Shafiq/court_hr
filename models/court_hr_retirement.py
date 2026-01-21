# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    retirement_ids = fields.One2many('employee.retirement', 'employee_id', string='Retirement')


# Your Python code (e.g., in a controller or model)

class EmployeeRetirement(models.Model):
    _name = 'employee.retirement'
    _description = 'Employee Retirement'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    retirement_type_id = fields.Many2one('employee.retirement.type', string="Retirement Type")
    retirement_reason_id = fields.Many2one('employee.retirement.reason', string="Retirement Reason")
    retirement_end_date = fields.Date(string='End Date')
    retirement_remarks = fields.Text(string='Remarks')



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




