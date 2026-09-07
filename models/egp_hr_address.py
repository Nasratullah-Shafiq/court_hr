# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    name = fields.Char(
        string='State Name',
        required=True,
        translate=True, tracking=True
    )

    district_ids = fields.One2many(
        'employee.district',
        'province_id',
        string='Districts',
        required=True, tracking=True
    )




class EmployeeDistrict(models.Model):
    _name = 'employee.district'
    _description = 'Employee District'

    name = fields.Char(string='District', translate=True, tracking=True)
    province_id = fields.Many2one('res.country.state', string='Province', ondelete='cascade', required=True, tracking=True)



class EmployeeVillage(models.Model):
    _name = 'employee.village'
    _description = 'Employee Village'

    name = fields.Char(string='Village',tracking=True)

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            if not record.name.replace(" ", "").isalpha():
                raise ValidationError("The Village name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Village name must be unique! and should not be duplicated!")
