# -*- coding: utf-8 -*-
from odoo import fields, models, api

# Your Python code (e.g., in a controller or model)

class EmployeeProperty(models.Model):
    _name = 'employee.property'
    _description = 'Employee Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

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

    property_type = fields.Selection(
        [('movable_property', 'Movable Property'), ('nonmovable_peroperty', 'Non Movable Property'),
         ('car', 'Car'), ('land', 'Land'), ('home', 'Home'), ('market', 'Market'),
         ('garden', 'Garden'), ('cash', 'Cash'), ('jewelery', 'Jewelery'), ('house', 'House'),
         ('other', 'other')], string="Property", tracking=True)

    price = fields.Integer(string='Price', tracking=True)
    remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)












