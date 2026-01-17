# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    relationship_ids = fields.One2many('employee.relatives', 'employee_id', string='Relatives')


# Your Python code (e.g., in a controller or model)

class EmployeeRelative(models.Model):
    _name = 'employee.relatives'
    _description = 'Employee Relatives'

    health_ids = fields.One2many('employee.health', 'employee_id', string='Health')
    employee_id = fields.Many2one('hr.employee', string='Employee')

    name = fields.Char(string='Name')
    last_name = fields.Char(string='Last Name')
    father_name = fields.Char(string='Father Name')
    grand_father_name = fields.Char(string='Grand Father Name')
    job = fields.Char(string='Job')
    nic_no = fields.Integer(string='NIC No')
    permanent_address = fields.Many2one('res.country.state', string="Province", tracking=True)
    permanent_district_id = fields.Many2one('employee.district', string="Permanent District / Village")
    temporary_address = fields.Many2one('res.country.state', string="Province", tracking=True)
    temporary_district_id = fields.Many2one('employee.district', string="Temporary District / Village")
    street_no = fields.Integer(string='Street No')
    home_no = fields.Integer(string='Home No')

    relationship_id = fields.Many2one('employee.relationship', string="Relationship", tracking=True)
    relationship_name = fields.Char(string='Name')
    relationship_last_name = fields.Char(string='Last Name')
    relationship_father_name = fields.Char(string='Father Name')
    relationship_grand_father_name = fields.Char(string='Grand Father Name')
    relationship_job_position = fields.Char(string='Job Position')
    relationship_email = fields.Char(string='Email')
    relationship_contact_info = fields.Char(string='Contact Info')
    relationship_identification_no = fields.Char(string='Identification No')
    relationship_permanent_address = fields.Char(string='Permanent Address')
    relationship_contemporary_address = fields.Char(string='Contemporary Address')
    relationship_property = fields.Char(string='Property')
    relationship_remarks = fields.Text(string='Remarks')

    image = fields.Binary("Upload Image", attachment=True)
    image_filename = fields.Char("Image Filename")  # optional, store original filename


    @api.constrains('relationship_name', 'relationship_last_name', 'relationship_father_name',
                    'relationship_grand_father_name', 'relationship_job_position')
    def _check_only_characters(self):
        pattern = r'^[a-zA-Z ]+$'
        for record in self:
            invalid_fields = []  # List to store fields with invalid values

            for field_name in ['relationship_name', 'relationship_last_name', 'relationship_father_name',
                               'relationship_grand_father_name', 'relationship_job_position']:
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

    name = fields.Char(string='Relationship')

    @api.constrains('name')
    def _check_name_only_characters(self):
        pattern = r'^[a-zA-Z ]+$'  # Allows only letters and spaces
        for record in self:
            if record.name and not re.match(pattern, record.name):
                raise ValidationError("The 'Relationship' field should contain only letters and spaces.")







