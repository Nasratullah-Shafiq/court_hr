# -*- coding: utf-8 -*-

from odoo import models, fields


class EmployeeWorkPermit(models.Model):
    _name = 'employee.work.permit'
    _description = 'Employee Work Permit'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)

    letter_no = fields.Char(string='Letter Number', required=True, tracking=True)
    letter_date = fields.Date(string='Letter Date', tracking=True)
    permit_no = fields.Char(string='Work Permit Number', required=True, tracking=True)
    remarks = fields.Text(string='Remarks')
    attachments = fields.Many2many('ir.attachment', string='Attachments')
