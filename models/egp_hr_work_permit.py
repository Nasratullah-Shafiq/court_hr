# -*- coding: utf-8 -*-

from odoo import models, fields


class EmployeeWorkPermit(models.Model):
    _name = 'employee.work.permit'
    _description = 'Employee Work Permit'
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


    letter_no = fields.Char(string='Letter Number', required=True, tracking=True)
    letter_date = fields.Date(string='Letter Date', tracking=True)
    permit_no = fields.Char(string='Work Permit Number', required=True, tracking=True)
    remarks = fields.Text(string='Remarks', tracking=True)
    attachments = fields.Many2many('ir.attachment', string='Attachments', tracking=True)
