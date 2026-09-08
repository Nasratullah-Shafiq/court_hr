# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re
from datetime import datetime


class EmployeeGuarantee(models.Model):
    _name = 'employee.guarantee'
    _description = 'Employee Guarantee'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    guarantee_type = fields.Selection([
        ('cash', 'Cash Guarantee'),
        ('property', 'Property Guarantee'),
        ('person', 'Person Guarantee'),
    ], string="Guarantee Type", required=True, tracking=True)

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True)
    job_id = fields.Many2one('hr.job', string='Job', related='employee_id.job_id', store=True, readonly=True,
                             tracking=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department',
                                    tracking=True)
    father_names = fields.Char(
        string='Father Name',
        related='employee_id.father_name',
        store=True,
        readonly=True
    )

    grand_father_names = fields.Char(
        string='Grand Father Name',
        related='employee_id.grand_father_name',
        store=True,
        readonly=True
    )


    # =======================
    # CASH GUARANTEE
    # =======================
    amount_of_cash = fields.Integer(string='Amount of Cash', tracking=True)
    bank_name = fields.Char(string='Bank Name', tracking=True)
    bank_slip_no = fields.Integer(string='Bank Slip No', tracking=True)


    # =======================
    # PROPERTY GUARANTEE
    # =======================

    country_id = fields.Many2one(
        'res.country',
        string="Country",
        tracking=True,
        default=lambda self: self.env.ref('base.af', raise_if_not_found=False)
    )
    province_id = fields.Many2one("res.country.state", string='Province', ondelete='restrict',
                                  domain="[('country_id', '=?', country_id)]", tracking=True)
    property_district_id = fields.Many2one(
        'employee.district',
        string="District",
        tracking=True,
        domain="[('province_id', '=', province_id)]"
    )
    property_village_id = fields.Many2one('employee.village', string="Village", tracking=True)
    deed_no = fields.Integer(string='Deed No', tracking=True)
    deed_date = fields.Date(string='Deed Date', tracking=True)


    # =======================
    # PERSON GUARANTEE
    # =======================
    person_name = fields.Char(string='Name', tracking=True)
    last_name = fields.Char(string='Last Name', tracking=True)
    father_name = fields.Char(string='Father Name', tracking=True)
    grand_father_name = fields.Char(string='Grand Father Name', tracking=True)
    job_position = fields.Char(string='Job Position', tracking=True)
    organization_id = fields.Many2one('employee.organization', string="Organization", tracking=True)

    permanent_province_id = fields.Many2one("res.country.state", string='Permanent Province', ondelete='restrict',
                                  domain="[('country_id', '=?', country_id)]", tracking=True)

    permanent_district_id = fields.Many2one(
        'employee.district',
        string="Permanent District",
        tracking=True,
        domain="[('province_id', '=', permanent_province_id)]"
    )
    permanent_village_id = fields.Many2one('employee.village', string="Permanent Village", tracking=True)

    temporary_province_id = fields.Many2one("res.country.state", string='Temporary Province', ondelete='restrict',
                                  domain="[('country_id', '=?', country_id)]", tracking=True)

    temporary_district_id = fields.Many2one(
        'employee.district',
        string="Temporary District",
        tracking=True,
        domain="[('province_id', '=', temporary_province_id)]"
    )
    temporary_village_id = fields.Many2one('employee.village', string="Temporary Village", tracking=True)

    phone_no = fields.Char(string='Phone No', tracking=True)
    email = fields.Char(string='Email', tracking=True)

    remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)

    @api.constrains(
        'guarantee_type',
        'person_name',
        'last_name',
        'father_name',
        'grand_father_name',
        'job_position',
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



