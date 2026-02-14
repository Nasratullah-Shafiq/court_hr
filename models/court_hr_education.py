from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
from datetime import date, datetime

# Your Python code (e.g., in a controller or model)

class EmployeeEducation(models.Model):
    _name = 'employee.education'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Employee Education'

    employee_id = fields.Many2one('hr.employee', tracking=True, string='Employee')

    country_id = fields.Many2one('res.country', string="Country", tracking=True)
    province_id = fields.Many2one("res.country.state", string='Province', ondelete='restrict',
                                  domain="[('country_id', '=?', country_id)]")
    degree_id = fields.Many2one('employee.degree', string="Degree")

    university_id = fields.Many2one('employee.university', tracking=True, string="University")
    faculty_id = fields.Many2one('employee.faculty', tracking=True, string="Faculty")
    major = fields.Char(string='Major', tracking=True)
    education_duration = fields.Selection([('continued', 'Continued'), ('interval_type', 'Interval Type')],
                                          string='Duration',
                                          tracking=True, default='continued',
                                          groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    in_service = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                  string='In - service',
                                  tracking=True, default='no',
                                  groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    education_start_date = fields.Date(string='Start Date', tracking=True)
    education_end_date = fields.Date(string='End Date', tracking=True)
    batch_no = fields.Integer(string='Batch No', tracking=True)
    education_remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments")

    education_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Education Month",
        compute="_compute_education_year_month",
        store=True
    )

    # Education Year
    education_year = fields.Selection(
        selection=lambda self: [
            (str(y), str(y)) for y in range(
                date.today().year - 30,
                date.today().year + 10
            )
        ],
        string="Education Year",
        compute="_compute_education_year_month",
        store=True
    )

    @api.depends('education_end_date')
    def _compute_education_year_month(self):
        for rec in self:
            if rec.education_end_date:
                rec.education_month = str(rec.education_end_date.month)
                rec.education_year = str(rec.education_end_date.year)
            else:
                rec.education_month = False
                rec.education_year = False

    @api.constrains('major')
    def _check_major(self):
        for record in self:
            if record.major and not re.match('^[A-Za-z ]+$', record.major):
                raise ValidationError("The Major field should only contain alphabetic characters and spaces.")


class EmployeeUniversity(models.Model):
    _name = 'employee.university'
    _description = 'Employee University'

    name = fields.Char(string='University', tracking=True, translate=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            # if not record.name.replace(" ", "").isalpha():
            #     raise ValidationError("The University name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The University name must be unique!")


class EmployeeFaculty(models.Model):
    _name = 'employee.faculty'
    _description = 'Employee Faculty'

    name = fields.Char(string='faculty', tracking=True, translate=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            # if not record.name.replace(" ", "").isalpha():
            #     raise ValidationError("The Faculty name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Faculty name must be unique!")


class EmployeeDegree(models.Model):
    _name = 'employee.degree'
    _description = 'Employee Degree'

    name = fields.Char(string='degree', tracking=True, translate=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            # if not record.name.replace(" ", "").isalpha():
            #     raise ValidationError("The Faculty name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Faculty name must be unique!")
