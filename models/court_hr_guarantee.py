# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re
from datetime import datetime

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    cash_guarantee_ids = fields.One2many('employee.cash.guarantee', 'employee_id', string='Guarantee')
    person_guarantee_ids = fields.One2many('employee.person.guarantee', 'employee_id', string='Guarantee')
    property_guarantee_ids = fields.One2many('employee.property.guarantee', 'employee_id', string='Guarantee')


# Your Python code (e.g., in a controller or model)

class CashGuarantee(models.Model):
    _name = 'employee.cash.guarantee'
    _description = 'Employee Cash Guarantee'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    amount_of_cash = fields.Integer(string='Amount of Cash')
    bank_name = fields.Char(string='Bank Name')
    bank_slip_no = fields.Integer(string='Bank Slip No')
    cash_remarks = fields.Text(string='Remarks')

    @api.constrains('bank_name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            if not record.bank_name.replace(" ", "").isalpha():
                raise ValidationError("The Bank name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('bank_name', '=', record.bank_name)]) > 1:
                raise ValidationError("The Bank name must be unique! and should not be duplicated!")


    class PropertyGuarantee(models.Model):
        _name = 'employee.property.guarantee'
        _description = 'Employee Property Guarantee'

        employee_id = fields.Many2one('hr.employee', string='Employee')

        province = fields.Selection([
            ('Badakhshan', 'Badakhshan'),
            ('Badghis', 'Badghis'),
            ('Baghlan', 'Baghlan'),
            ('Balkh', 'Balkh'),
            ('Bamyan', 'Bamyan'),
            ('Daykundi', 'Daykundi'),
            ('Farah', 'Farah'),
            ('Faryab', 'Faryab'),
            ('Ghazni', 'Ghazni'),
            ('Ghor', 'Ghor'),
            ('Helmand', 'Helmand'),
            ('Herat', 'Herat'),
            ('Jowzjan', 'Jowzjan'),
            ('Kabul', 'Kabul'),
            ('Kandahar', 'Kandahar'),
            ('Kapisa', 'Kapisa'),
            ('Khost', 'Khost'),
            ('Kunar', 'Kunar'),
            ('Kunduz', 'Kunduz'),
            ('Laghman', 'Laghman'),
            ('Logar', 'Logar'),
            ('Nangarhar', 'Nangarhar'),
            ('Nimroz', 'Nimroz'),
            ('Nuristan', 'Nuristan'),
            ('Paktia', 'Paktia'),
            ('Paktika', 'Paktika'),
            ('Panjshir', 'Panjshir'),
            ('Parwan', 'Parwan'),
            ('Samangan', 'Samangan'),
            ('Sar-e Pol', 'Sar-e Pol'),
            ('Takhar', 'Takhar'),
            ('Urozgan', 'Urozgan'),
            ('Wardak', 'Wardak'),
            ('Zabul', 'Zabul')
        ], string="Province")
        property_district_id = fields.Many2one('employee.district', string="District")
        property_village_id = fields.Many2one('employee.village', string="Village")
        deed_no = fields.Integer(string='Deed No')
        deed_date = fields.Date(string='Deed Date')
        property_remarks = fields.Text(string='Remarks')


class PersonGuarantee(models.Model):
    _name = 'employee.person.guarantee'
    _description = 'Employee Person Guarantee'

    employee_id = fields.Many2one('hr.employee', string='Employee')

    person_name = fields.Char(string='Name', required=True)
    last_name = fields.Char(string='Last Name')
    father_name = fields.Char(string='Father Name')
    grand_father_name = fields.Char(string='Grand Father Name')
    job_position = fields.Char(string='Job Position')
    organization = fields.Char(string='Organization')
    # permanent_province_id = fields.Many2one('res.country.state', string="Province", tracking=True, ondelete='cascade')
    permanent_district_id = fields.Many2one('employee.district', string="District")
    permanent_village_id = fields.Many2one('employee.village', string="Village")

    temporary_province_id = fields.Many2one('res.country.state', string="Province", tracking=True, ondelete='cascade')
    temporary_district_id = fields.Many2one('employee.district', string="District")
    temporary_village_id = fields.Many2one('employee.village', string="Village")
    phone_no = fields.Char(string='Phone No')
    person_remarks = fields.Text(string='Remarks')
    email = fields.Char(string='Email')
    PROVINCES = [
        ('Badakhshan', 'Badakhshan'),
        ('Badghis', 'Badghis'),
        ('Baghlan', 'Baghlan'),
        ('Balkh', 'Balkh'),
        ('Bamyan', 'Bamyan'),
        ('Daykundi', 'Daykundi'),
        ('Farah', 'Farah'),
        ('Faryab', 'Faryab'),
        ('Ghazni', 'Ghazni'),
        ('Ghor', 'Ghor'),
        ('Helmand', 'Helmand'),
        ('Herat', 'Herat'),
        ('Jowzjan', 'Jowzjan'),
        ('Kabul', 'Kabul'),
        ('Kandahar', 'Kandahar'),
        ('Kapisa', 'Kapisa'),
        ('Khost', 'Khost'),
        ('Kunar', 'Kunar'),
        ('Kunduz', 'Kunduz'),
        ('Laghman', 'Laghman'),
        ('Logar', 'Logar'),
        ('Nangarhar', 'Nangarhar'),
        ('Nimroz', 'Nimroz'),
        ('Nuristan', 'Nuristan'),
        ('Paktia', 'Paktia'),
        ('Paktika', 'Paktika'),
        ('Panjshir', 'Panjshir'),
        ('Parwan', 'Parwan'),
        ('Samangan', 'Samangan'),
        ('Sar-e Pol', 'Sar-e Pol'),
        ('Takhar', 'Takhar'),
        ('Urozgan', 'Urozgan'),
        ('Wardak', 'Wardak'),
        ('Zabul', 'Zabul')
    ]
    permanent_province = fields.Selection(PROVINCES, string="Province")
    temporary_province = fields.Selection(PROVINCES, string="Province")

    @api.constrains('person_name', 'last_name', 'father_name', 'grand_father_name', 'job_position', 'organization')
    def _check_only_characters(self):
        pattern = r'^[a-zA-Z ]+$'
        for record in self:
            invalid_fields = []  # List to store fields with invalid values

            for field_name in ['person_name', 'last_name', 'father_name', 'grand_father_name', 'job_position', 'organization']:
                value = getattr(record, field_name)
                if value and not re.match(pattern, value):
                    invalid_fields.append(self._fields[field_name].string)  # Store field names for error message

            if invalid_fields:  # If any invalid fields exist, raise a validation error
                raise ValidationError(
                    f"The following fields should contain only letters and spaces: {', '.join(invalid_fields)}"
                )
