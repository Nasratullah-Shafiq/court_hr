# -*- coding: utf-8 -*-
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import datetime
import re

# Your Python code (e.g., in a controller or model)

class EmployeeExperience(models.Model):
    _name = 'employee.experience'
    _description = 'Employee Experience'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')


    organization_id = fields.Many2one('employee.organization', string="Organization")
    job_id = fields.Many2one('hr.job', string='Job', tracking=True)

    country_id = fields.Many2one(
        'res.country',
        string='Country',
        default=lambda self: self.env.ref('base.af'),
        tracking=True
    )

    province_id = fields.Many2one(
        'res.country.state',
        string='Province',
        domain="[('country_id', '=', country_id)]",
        tracking=True
    )

    grade_id = fields.Many2one('employee.grade', string="Grade")

    step_id = fields.Many2one('employee.step', string="Step")

    department = fields.Char(string='Department')
    status_id = fields.Many2one('employee.status', string="Status", required=True)
    job_start_date = fields.Date(string='Start Date')
    job_end_date = fields.Date(string='End Date')
    organization_type = fields.Selection([('Civil', 'Civil'), ('Military', 'Military'), ('NGO', 'NGO'),
                                          ('international_organization', 'International Organization'),
                                          ('united_nations', 'United Nations')], string="Organization Type")
    job_remarks = fields.Text(string='Remarks')
    duration_human_readable = fields.Char(
        string="Service Duration",
        compute="_compute_duration_human_readable",
        store=True
    )

    court_level = fields.Selection([
        ('مرکز', 'مرکز'),
        ('تمیز مرکزی', 'تمیز مرکزی'),
        ('تمیز زون قندهار', 'تمیز زون قندهار'),
        ('مرافعه', 'مرافعه'),
        ('ابتداییه', 'ابتداییه'),
        ('نظامی', 'نظامی')
    ], default="مرکز", string="Court Level",
        groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    attachments = fields.Many2many('ir.attachment', string="Attachments")

    experience_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Experience Month",
        compute="_compute_experience_year_month",
        store=True
    )

    # --------------------------------------------------
    # Experience Year
    # --------------------------------------------------
    experience_year = fields.Selection(
        selection=lambda self: [
            (str(y), str(y)) for y in range(
                datetime.date.today().year - 30,
                datetime.date.today().year + 10
            )
        ],
        string="Experience Year",
        compute="_compute_experience_year_month",
        store=True
    )

    # --------------------------------------------------
    # Compute Method
    # --------------------------------------------------
    @api.depends('job_end_date')
    def _compute_experience_year_month(self):
        for rec in self:
            if rec.job_end_date:
                rec.experience_month = str(rec.job_end_date.month)
                rec.experience_year = str(rec.job_end_date.year)
            else:
                rec.experience_month = False
                rec.experience_year = False



    @api.constrains('job_position', 'department')
    def _check_only_characters(self):
        pattern = r'^[a-zA-Z ]+$'
        for record in self:
            invalid_fields = []  # List to store fields with invalid values

            for field_name in ['job_position', 'department']:
                value = getattr(record, field_name)
                if value and not re.match(pattern, value):
                    invalid_fields.append(self._fields[field_name].string)  # Store field names for error message

            if invalid_fields:  # If any invalid fields exist, raise a validation error
                raise ValidationError(
                    f"The fields should contain only letters and spaces: {', '.join(invalid_fields)}"
                )

    @api.depends('job_start_date', 'job_end_date')
    def _compute_duration_human_readable(self):
        for record in self:
            if record.job_start_date and record.job_end_date:
                # Validation: Check if start date is greater than end date
                if record.job_start_date > record.job_end_date:
                    raise ValidationError("The start date must be earlier than or equal to the end date.")

                # Calculate the duration using relativedelta
                rdelta = relativedelta(record.job_end_date, record.job_start_date)

                # Build the human-readable duration string
                duration_parts = []
                if rdelta.years:
                    duration_parts.append(f"{rdelta.years} year{'s' if rdelta.years > 1 else ''}")
                if rdelta.months:
                    duration_parts.append(f"{rdelta.months} month{'s' if rdelta.months > 1 else ''}")

                # Join the parts with 'and' if both years and months exist
                record.duration_human_readable = " and ".join(duration_parts)
            else:
                record.duration_human_readable = "0 months"


class EmployeeOrganization(models.Model):
    _name = 'employee.organization'
    _description = 'Employee Organization'

    name = fields.Char(string='Organization', required=True, translate=True, unique=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Organization name must be unique!")


class EmployeeStatus(models.Model):
    _name = 'employee.status'
    _description = 'Employee Status'

    name = fields.Char(string='Status')

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError('The status must be unique!')



class EmployeeGrade(models.Model):
    _name = 'employee.grade'
    _description = 'Employee Grade'

    name = fields.Char(string='Grade', required=True, translate=True, unique=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Grade name must be unique!")


