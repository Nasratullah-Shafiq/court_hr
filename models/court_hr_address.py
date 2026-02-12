# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    district_ids = fields.One2many(
        'employee.district',
        'province_id',
        string='Districts',
        required=True
    )



class EmployeeDistrict(models.Model):
    _name = 'employee.district'
    _description = 'Employee District'

    name = fields.Char(string='District')
    province_id = fields.Many2one('res.country.state', string='Province', ondelete='cascade', required=True)

    # @api.constrains('name')
    # def _check_name_constraints(self):
    #     for record in self:
            # Ensure the name contains only letters and spaces
            # if not record.name.replace(" ", "").isalpha():
            #     raise ValidationError("The District name should only contain letters and spaces.")

            # Check for duplicates at the application level
            # if self.search_count([('name', '=', record.name)]) > 1:
            #     raise ValidationError("The District name must be unique! and should not be duplicated!")


class EmployeeVillage(models.Model):
    _name = 'employee.village'
    _description = 'Employee Village'

    name = fields.Char(string='Village')

    @api.constrains('name')
    def _check_name_constraints(self):
        for record in self:
            # Ensure the name contains only letters and spaces
            if not record.name.replace(" ", "").isalpha():
                raise ValidationError("The Village name should only contain letters and spaces.")

            # Check for duplicates at the application level
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The Village name must be unique! and should not be duplicated!")





# # address fields
#     street = fields.Char()
#     street2 = fields.Char()
#     zip = fields.Char(change_default=True)
#
#     country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',
#                                  default=lambda self: self.env.ref('base.af').id)
#     country_code = fields.Char(related='country_id.code', string="Country Code")
#     state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
#                                domain="[('country_id', '=?', country_id)]")
#     city_id = fields.Many2one('res.state.city', string="City", ondelete='restrict',
#                               domain="[('state_id', '=', state_id)]")




