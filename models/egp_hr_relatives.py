# -*- coding: utf-8 -*-
import re

from odoo.exceptions import ValidationError

from odoo import fields, models, api

# Your Python code (e.g., in a controller or model)

class EmployeeRelative(models.Model):
    _name = 'employee.relatives'
    _description = 'Employee Relatives'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # =========================
    # Employee Reference
    # =========================
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    job_id = fields.Many2one('hr.job', string='Job', related='employee_id.job_id', store=True, readonly=True,
                             tracking=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department',
                                    tracking=True)
    father_name = fields.Char(
        string='Father Name',
        related='employee_id.father_name',
        store=True,
        readonly=True
    )

    grand_father_name = fields.Char(
        string='Grand Father Name',
        related='employee_id.grand_father_name',
        store=True,
        readonly=True
    )

    # =========================
    # Personal Information
    # =========================
    person_name = fields.Char(string='First Name', required=True, tracking=True)
    last_name = fields.Char(string='Last Name', tracking=True)
    father_name = fields.Char(string='Father Name', tracking=True)
    grand_father_name = fields.Char(string='Grand Father Name', tracking=True)

    relationship_id = fields.Many2one('employee.relationship', string="Relationship", tracking=True)
    job_id = fields.Many2one('hr.job', string='Job', tracking=True)
    nic_no = fields.Integer(string='NIC No', tracking=True)
    identification_no = fields.Char(string='Identification No', tracking=True)

    # =========================
    # Contact Information
    # =========================
    email = fields.Char(string='Email', tracking=True)
    contact_info = fields.Char(string='Contact Info', tracking=True)

    # =========================
    # Country
    # =========================
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        default=lambda self: self.env.ref('base.af'),
        tracking=True
    )

    # =========================
    # Permanent Address
    # =========================
    permanent_province_id = fields.Many2one(
        'res.country.state',
        string='Permanent Province',
        domain="[('country_id', '=', country_id)]",
        tracking=True
    )
    permanent_district_id = fields.Many2one(
        'employee.district',
        string='Permanent District',
        domain="[('province_id', '=', permanent_province_id)]",
        tracking=True
    )
    permanent_street_no = fields.Char(string='Permanent Street No', tracking=True)
    permanent_home_no = fields.Char(string='Permanent Home No', tracking=True)

    # =========================
    # Temporary Address
    # =========================
    temporary_province_id = fields.Many2one(
        'res.country.state',
        string='Temporary Province',
        domain="[('country_id', '=', country_id)]",
        tracking=True
    )
    temporary_district_id = fields.Many2one(
        'employee.district',
        string='Temporary District',
        domain="[('province_id', '=', temporary_province_id)]",
        tracking=True
    )
    temporary_street_no = fields.Char(string='Temporary Street No', tracking=True)
    temporary_home_no = fields.Char(string='Temporary Home No', tracking=True)

    # =========================
    # Other Information
    # =========================
    property = fields.Char(string='Property', tracking=True)
    remarks = fields.Text(string='Remarks', tracking=True)

    # =========================
    # Attachments
    # =========================
    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)


@api.constrains('person_name', 'last_name', 'father_name',
                'grand_father_name', 'job_position')
def _check_only_characters(self):
    pattern = r'^[a-zA-Z ]+$'
    for record in self:
        invalid_fields = []  # List to store fields with invalid values

        for field_name in ['person_name', 'last_name', 'father_name',
                           'grand_father_name', 'job_position']:
            value = getattr(record, field_name)
            if value and not re.match(pattern, value):
                invalid_fields.append(self._fields[field_name].string)  # Store field names for error message

        if invalid_fields:  # If any invalid fields exist, raise a validation error
            raise ValidationError(
                f"The following fields should contain only letters and spaces: {', '.join(invalid_fields)}"
            )


class EmployeeRelationship(models.Model):
    _name = 'employee.relationship'
    _description = 'Employee Relationship'

    name = fields.Char(string='Relationship', tracking=True)

    @api.constrains('name')
    def _check_name_only_characters(self):
        # pattern = r'^[a-zA-Z ]+$'  # Allows only letters and spaces
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Relative Relationship  must be unique! and should not be duplicated!")
