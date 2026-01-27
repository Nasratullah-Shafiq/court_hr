# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import datetime


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    reward_ids = fields.One2many('employee.reward', 'employee_id', string='reward')


# Your Python code (e.g., in a controller or model)

class EmployeeReward(models.Model):
    _name = 'employee.reward'
    _description = 'Employee Reward'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')
    reward_type = fields.Selection([('sign', 'Sign'), ('medal', 'Medal'), ('cash', 'Cash'),
                                    ('one_month_salary', 'One Month Salary'),
                                    ('honorary_letter_of_appreciation', 'Honorary Letter of Appreciation'),
                                    ('encouragement_of_civil_services_workers',
                                     'Encouragement of civil service workers'),
                                    ('first_degree_of_appreciation', 'First degree of appreciation'),
                                    ('second_degree_of_appreciation', 'Second degree of appreciation'),
                                    ('third_degree_of_appreciation', 'Third degree of appreciation')],
                                   string="Reward Type", default='medal')
    amount_of_cash_for_reward = fields.Integer(string='Amount of Cash for Reward')
    order_no = fields.Integer(string='Order No')
    order_date = fields.Date(string='Order Date')
    organization_id = fields.Many2one('employee.organization', string="Appreciation of the Organization")
    reason = fields.Char(string='Reason')

    attachments = fields.Many2many('ir.attachment', string="Attachments")

    # =========================
    # Reward Month / Year
    # =========================

    reward_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Reward Month",
        compute="_compute_reward_year_month",
        store=True
    )

    reward_year = fields.Selection(
        selection=lambda self: [
            (str(y), str(y)) for y in
            range(datetime.date.today().year - 30,
                  datetime.date.today().year + 10)
        ],
        string="Reward Year",
        compute="_compute_reward_year_month",
        store=True
    )

    @api.depends('order_date')
    def _compute_reward_year_month(self):
        for rec in self:
            if rec.order_date:
                rec.reward_month = str(rec.order_date.month)
                rec.reward_year = str(rec.order_date.year)
            else:
                rec.reward_month = False
                rec.reward_year = False
