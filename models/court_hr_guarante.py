# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re
from datetime import datetime

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    guarantee_ids = fields.One2many('employee.guarantee', 'employee_id', string='Guarantee')


class EmployeeGuarantee(models.Model):
    _name = 'employee.guarantee'
    _description = 'Employee Guarantee'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    guarantee_type = fields.Selection([
        ('cash', 'Cash Guarantee'),
        ('property', 'Property Guarantee'),
        ('person', 'Person Guarantee'),
    ], string="Guarantee Type", required=True, tracking=True)

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)

    # =======================
    # CASH GUARANTEE
    # =======================
    amount_of_cash = fields.Integer(string='Amount of Cash')
    bank_name = fields.Char(string='Bank Name')
    bank_slip_no = fields.Integer(string='Bank Slip No')
    cash_remarks = fields.Text(string='Cash Remarks')

    # =======================
    # PROPERTY GUARANTEE
    # =======================
    PROVINCES = [
        ('Badakhshan', 'Badakhshan'), ('Badghis', 'Badghis'), ('Baghlan', 'Baghlan'), ('Balkh', 'Balkh'),
        ('Bamyan', 'Bamyan'), ('Daykundi', 'Daykundi'), ('Farah', 'Farah'), ('Faryab', 'Faryab'),
        ('Ghazni', 'Ghazni'), ('Ghor', 'Ghor'), ('Helmand', 'Helmand'), ('Herat', 'Herat'), ('Jowzjan', 'Jowzjan'),
        ('Kabul', 'Kabul'), ('Kandahar', 'Kandahar'), ('Kapisa', 'Kapisa'), ('Khost', 'Khost'), ('Kunar', 'Kunar'),
        ('Kunduz', 'Kunduz'), ('Laghman', 'Laghman'), ('Logar', 'Logar'), ('Nangarhar', 'Nangarhar'),
        ('Nimroz', 'Nimroz'), ('Nuristan', 'Nuristan'), ('Paktia', 'Paktia'), ('Paktika', 'Paktika'),
        ('Panjshir', 'Panjshir'), ('Parwan', 'Parwan'), ('Samangan', 'Samangan'), ('Sar-e Pol', 'Sar-e Pol'),
        ('Takhar', 'Takhar'), ('Urozgan', 'Urozgan'), ('Wardak', 'Wardak'), ('Zabul', 'Zabul')
    ]
    province = fields.Selection(PROVINCES, string="Province")
    property_district_id = fields.Many2one('employee.district', string="District")
    property_village_id = fields.Many2one('employee.village', string="Village")
    deed_no = fields.Integer(string='Deed No')
    deed_date = fields.Date(string='Deed Date')
    property_remarks = fields.Text(string='Property Remarks')

    # =======================
    # PERSON GUARANTEE
    # =======================
    person_name = fields.Char(string='Name')
    last_name = fields.Char(string='Last Name')
    father_name = fields.Char(string='Father Name')
    grand_father_name = fields.Char(string='Grand Father Name')
    job_position = fields.Char(string='Job Position')
    organization_id = fields.Many2one('employee.organization', string="Organization")

    permanent_province = fields.Selection(PROVINCES, string="Permanent Province")
    permanent_district_id = fields.Many2one('employee.district', string="Permanent District")
    permanent_village_id = fields.Many2one('employee.village', string="Permanent Village")

    temporary_province = fields.Selection(PROVINCES, string="Temporary Province")
    temporary_district_id = fields.Many2one('employee.district', string="Temporary District")
    temporary_village_id = fields.Many2one('employee.village', string="Temporary Village")

    phone_no = fields.Char(string='Phone No')
    email = fields.Char(string='Email')
    person_remarks = fields.Text(string='Person Remarks')

    attachments = fields.Many2many('ir.attachment', string="Attachments")

    @api.constrains(
        'guarantee_type',
        'person_name',
        'last_name',
        'father_name',
        'grand_father_name',
        'job_position',
        'organization'
    )
    def _check_person_guarantee_only_characters(self):
        pattern = r'^[a-zA-Z ]+$'

        for record in self:
            # Apply validation ONLY for Person Guarantee
            if record.guarantee_type != 'person':
                continue

            invalid_fields = []

            fields_to_check = [
                'person_name',
                'last_name',
                'father_name',
                'grand_father_name',
                'job_position',
                'organization',
            ]

            for field_name in fields_to_check:
                value = getattr(record, field_name)
                if value and not re.match(pattern, value):
                    invalid_fields.append(record._fields[field_name].string)

            if invalid_fields:
                raise ValidationError(
                    "The following fields should contain only letters and spaces:\n- "
                    + "\n- ".join(invalid_fields)
                )



