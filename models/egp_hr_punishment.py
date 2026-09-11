# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import datetime


# Your Python code (e.g., in a controller or model)

class EmployeePunishment(models.Model):
    _name = 'employee.punishment'
    _description = 'Employee punishment'
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

    punishment_type = fields.Selection([
        ('removal_of_duty_job', 'Removal of Duty Job'),
        ('removal_of_current_rank', 'Removal of Current Rank'),
        ('fine', 'Fine'),
        ('salary_deduction', 'Salary Deduction'),
        ('dismissal_of_duty', 'Dismissal of Duty'),
        ('recommendation', 'Recommendation'),
        ('warning', 'Warning'),
        ('change_of_duty', 'Change of Duty'),
        ('contract_cancelled', 'Contract Cancelled')
    ], string="Punishment Type", tracking=True)

    violation_type = fields.Selection([
        ('uniform', 'Uniform'),
        ('educational', 'Educational'),
        ('behavioral', 'Behavioral'),
        ('administrative', 'Administrative'),
        ('traffics', 'Traffics'),
        ('holiday', 'Holiday'),
        ('religious affairs', 'Religious Affairs'),
        ('missing_card', 'Missing Card'),
        ('murder', 'Murder')
    ], string="Violation Type", tracking=True)

    order = fields.Char(string='Order', tracking=True)

    punishment_start_date = fields.Date(string='Start Date', tracking=True)

    punishment_end_date = fields.Date(string='End Date', tracking=True)

    punishment_date = fields.Date(string='Date Of Punishment', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)


    punishment_remarks = fields.Text(string='Remarks', tracking=True)

    punishment_month = fields.Selection(
        [
            ('1', 'January'),
            ('2', 'February'),
            ('3', 'March'),
            ('4', 'April'),
            ('5', 'May'),
            ('6', 'June'),
            ('7', 'July'),
            ('8', 'August'),
            ('9', 'September'),
            ('10', 'October'),
            ('11', 'November'),
            ('12', 'December')
        ],
        string="Punishment Month",
        compute="_compute_punishment_year_month",
        store=True,
        tracking=True
    )

    punishment_year = fields.Selection(
        selection=lambda self: [
            (str(y), str(y))
            for y in range(
                datetime.date.today().year - 30,
                datetime.date.today().year + 10
            )
        ],
        string="Punishment Year",
        compute="_compute_punishment_year_month",
        store=True,
        tracking=True
    )