# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    _description = "Human Resource"

    education_ids = fields.One2many('employee.education', 'employee_id', tracking=True, string='Education')


# Your Python code (e.g., in a controller or model)

class EmployeeEducation(models.Model):
    _name = 'employee.education'
    _inherit = ['mail.thread']
    _description = 'Employee Education'

    employee_id = fields.Many2one('hr.employee', tracking=True, string='Employee')

    country = fields.Many2one('res.country', string="Country", tracking=True)
    # degree_id = fields.Many2one('employee.degree', string="Degree")
    degree = fields.Selection([
        ('phd', 'Phd'),
        ('master', 'Master'),
        ('bachelor', 'Bachelor'),
        ('post-baccalaureate', 'Post-baccalaureate'),
        ('baccalaureate', 'Baccalaureate'),
        ('private', 'Private'),
        ('secondary', 'Secondary'),
        ('darul_uloom', 'Darul Uloom')
    ], string="Degree", tracking=True)

    university_id = fields.Many2one('employee.university', tracking=True, string="University")
    faculty_id = fields.Many2one('employee.faculty', tracking=True, string="Faculty")
    major = fields.Char(string='Major', tracking=True)
    education_duration = fields.Selection([('continued', 'Continued'), ('interval_type', 'Interval Type')], string='Duration',
                                  tracking=True,
                                  groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    in_service = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                          string='In - service',
                                          tracking=True,
                                          groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    education_start_date = fields.Date(string='Start Date', tracking=True)
    education_end_date = fields.Date(string='End Date', tracking=True)
    batch_no = fields.Integer(string='Batch No', tracking=True)
    education_remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments")



    @api.constrains('major')
    def _check_major(self):
        for record in self:
            if record.major and not re.match('^[A-Za-z ]+$', record.major):
                raise ValidationError("The Major field should only contain alphabetic characters and spaces.")




class EmployeeUniversity(models.Model):
    _name = 'employee.university'
    _description = 'Employee University'

    name = fields.Char(string='University', tracking=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            if not record.name.replace(" ", "").isalpha():
                raise ValidationError("The University name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The University name must be unique!")

class EmployeeFaculty(models.Model):
    _name = 'employee.faculty'
    _description = 'Employee Faculty'

    name = fields.Char(string='faculty', tracking=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            if not record.name.replace(" ", "").isalpha():
                raise ValidationError("The Faculty name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Faculty name must be unique!")





