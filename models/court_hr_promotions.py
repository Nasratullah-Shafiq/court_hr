# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

# Your Python code (e.g., in a controller or model)

class EmployeePromotion(models.Model):
    _name = 'employee.promotions'
    _description = 'Employee Promotions'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')

    approval_no = fields.Char(string='Approval No', Tracking='true')
    proposal_no = fields.Char(string='Proposal No', Tracking='true')
    order_no = fields.Integer(string='Order No', Tracking='true')

    rank_promotion = fields.Char(string='Rank Promotion', Tracking='true')

    offer_date = fields.Date(string='Offer Date', Tracking='true')
    proposal_date = fields.Date(string='Proposal Date', Tracking='true')
    order_date = fields.Date(string='Order Date', Tracking='true')
    approval_date = fields.Date(string='Approval Date', Tracking='true')

    promotion_remarks = fields.Text(string='Remarks', Tracking='true')

    attachments = fields.Many2many('ir.attachment', string="Attachments")

