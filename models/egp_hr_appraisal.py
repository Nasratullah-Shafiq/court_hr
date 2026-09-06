# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date, datetime, timedelta
import datetime

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    appraisal_ids = fields.One2many('employee.appraisal', 'employee_id', string='Appraisal', tracking=True)


# Your Python code (e.g., in a controller or model)
class EmployeeAppraisal(models.Model):
    _name = 'employee.appraisal'
    _description = 'Employee Appraisal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # employee basic info part.
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




    appraisal_type = fields.Selection([('trail', 'Trail'), ('annual', 'Annual'), ('monthly', 'Monthly'),
                                       ('trail_according_to_the_plan', 'Trail According To The Plan'),
                             ('quarterly', 'Quarterly')], string="Appraisal Type", default='annual', tracking=True)
    total_marks = fields.Integer(string='Total Marks', tracking=True)
    head_details = fields.Selection([('head', 'Head'), ('external_head', 'External Head'), ('superior_head', 'Superior Head'),
                                       ('supervisor', 'Supervisor'),
                                       ('quarterly', 'Quarterly')], string="Head Details", default='superior_head', tracking=True)

    basic_objective_of_work_plan = fields.Selection([('yes', 'Yes'), ('no', 'No')],
                                                    string="Basic objective of work plan", default='yes', tracking=True)
    head_opinion = fields.Text(string='Head Opinion', tracking=True)
    superior_head_opinion = fields.Text(string='Superior Head', tracking=True)
    appraisal_date = fields.Date(string='Appraisal Date', tracking=True)
    is_action_plan_accommodated = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Action Plan Accommodation",
                                                   default='yes', tracking=True)
    final_result = fields.Selection([('2nd_step', 'Upgrade to the Second step'),
                                     ('3rd_step', 'Upgrade to the Third step'),
                                     ('4th_step', 'Upgrade to the Fourth step'),
                                     ('5th_step', 'Upgrade to the Fifth step'),
                                     ('conversion_to_province', 'Discipline (conversion to provinces)'),
                ('continuation_position', 'Continuation of duty in the current position'),
                ('job_announcement', 'Job Announcement'),
                ('introduce_to_capacity_building', 'Continuation of duty in active duties and steps and introduction to education')],
                                    string="Final Result", default='2nd_step', tracking=True)
    employee_opinion = fields.Text(string='Employee Opinion', tracking=True)
    is_agree_with_the_result = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Agree with the result",
                                                   default='yes', tracking=True)

    employee_opinion_again = fields.Text(string='Employee Opinion', tracking=True)
    supervisor_opinion = fields.Text(string='Superior Head', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)

    appraisal_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Appraisal Month",
        compute="_compute_appraisal_year_month",
        store=True, tracking=True
    )

    appraisal_year = fields.Selection(
        selection=lambda self: [
            (str(y), str(y)) for y in
            range(datetime.date.today().year - 30,
                  datetime.date.today().year + 10)
        ],
        string="Appraisal Year",
        compute="_compute_appraisal_year_month",
        store=True, tracking=True
    )

    # -------------------------------------------------
    # Compute Method
    # -------------------------------------------------
    @api.depends('appraisal_date')
    def _compute_appraisal_year_month(self):
        for rec in self:
            if rec.appraisal_date:
                rec.appraisal_month = str(rec.appraisal_date.month)
                rec.appraisal_year = str(rec.appraisal_date.year)
            else:
                rec.appraisal_month = False
                rec.appraisal_year = False



