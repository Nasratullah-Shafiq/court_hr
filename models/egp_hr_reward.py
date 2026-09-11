# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import datetime

# Your Python code (e.g., in a controller or model)

class EmployeeReward(models.Model):
    _name = 'employee.reward'
    _description = 'Employee Reward'
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


    reward_type = fields.Selection([('sign', 'Sign'), ('medal', 'Medal'), ('cash', 'Cash'),
                                    ('one_month_salary', 'One Month Salary'),
                                    ('honorary_letter_of_appreciation', 'Honorary Letter of Appreciation'),
                                    ('encouragement_of_civil_services_workers',
                                     'Encouragement of civil service workers'),
                                    ('first_degree_of_appreciation', 'First degree of appreciation'),
                                    ('second_degree_of_appreciation', 'Second degree of appreciation'),
                                    ('third_degree_of_appreciation', 'Third degree of appreciation')],
                                   string="Reward Type", default='medal', tracking=True)
    amount_of_cash_for_reward = fields.Integer(string='Amount of Cash for Reward', tracking=True)
    order_no = fields.Integer(string='Order No', tracking=True)
    order_date = fields.Date(string='Order Date', tracking=True)
    organization_id = fields.Many2one('employee.organization', string="Appreciation of the Organization", tracking=True)
    reason = fields.Char(string='Reason', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)

    reward_remarks = fields.Text(string='Remarks', tracking=True)

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
        store=True, tracking=True
    )

    reward_year = fields.Selection(
        selection=lambda self: [
            (str(y), str(y)) for y in
            range(datetime.date.today().year - 30,
                  datetime.date.today().year + 10)
        ],
        string="Reward Year",
        compute="_compute_reward_year_month",
        store=True, tracking=True
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
