# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import datetime

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    punishment_ids = fields.One2many('employee.punishment', 'employee_id', string='Punishment')


# Your Python code (e.g., in a controller or model)

class EmployeePunishment(models.Model):
    _name = 'employee.punishment'
    _description = 'Employee punishment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')

    punishment_type = fields.Selection([
        ('removal_of_duty_job', 'Removal of Duty Job'),
        ('removal_of_current_rank', 'Removal of Current Rank'),
        ('fine', 'Fine'),
        ('salary_deduction', 'Salary Deduction'),
        ('dismissal_of_duty', 'Dismissal of Duty'),
        ('recommendation', 'Recommendation'),
        ('warning', 'Warning'),
        ('change_of_duty', 'Change of Duty'),
        ('contract_cancelled', 'Contract Cancelled')], string="Punishment Type")

    violation_type = fields.Selection([
        ('uniform', 'Uniform'),
        ('educational', 'Educational'),
        ('behavioral', 'Behavioral'),
        ('administrative', 'Administrative'),
        ('traffics', 'Traffics'),
        ('holiday', 'Holiday'),
        ('religious affairs', 'Religious ََAffairs'),
        ('missing_card', 'Missing Card'),
        ('murder', 'Murder')], string="Violation Type")

    order = fields.Char(string='Order')

    punishment_start_date = fields.Date(string='Start Date')
    punishment_end_date = fields.Date(string='End Date')
    punishment_date = fields.Date(string='Date Of Punishment')

    attachments = fields.Many2many('ir.attachment', string="Attachments")

    punishment_remarks = fields.Text(string='Remarks')

    punishment_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Punishment Month",
        compute="_compute_punishment_year_month",
        store=True
    )

    punishment_year = fields.Selection(
        selection=lambda self: [
            (str(y), str(y)) for y in
            range(datetime.date.today().year - 30,
                  datetime.date.today().year + 10)
        ],
        string="Punishment Year",
        compute="_compute_punishment_year_month",
        store=True
    )

    @api.depends('punishment_end_date')
    def _compute_punishment_year_month(self):
        for rec in self:
            if rec.punishment_end_date:
                rec.punishment_month = str(rec.punishment_end_date.month)
                rec.punishment_year = str(rec.punishment_end_date.year)
            else:
                rec.punishment_month = False
                rec.punishment_year = False








