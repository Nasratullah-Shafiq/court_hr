# -*- coding: utf-8 -*-
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import datetime

# Your Python code (e.g., in a controller or model)

class EmployeeExam(models.Model):
    _name = 'employee.exam'
    _description = 'Employee Exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)
    job_id = fields.Many2one('hr.job', string='Job', related='employee_id.job_id', store=True, readonly=True, tracking=True)
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string='Department', tracking=True)
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

    exam_subject = fields.Char(string='Subject', tracking=True)
    exam_type = fields.Selection([('written_test', 'Written Test'), ('interview', 'Interview'),
                                  ('technical', 'Technical (Special Interview)'),
                                  ('computerized_exam', 'Computerized Exam'), ('english', 'English')], string="Exam Type",
                                 default='written_test', tracking=True)
    exam_date = fields.Date(string='Exam Date', tracking=True)
    exam_result = fields.Char(string='Result', tracking=True)
    exam_score = fields.Integer(string='Score', tracking=True)
    exam_remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)

    @api.constrains('exam_score')
    def _check_exam_score(self):
        for record in self:
            if not isinstance(record.exam_score, int):
                raise ValidationError("The score must be a valid integer.")
            if record.exam_score < 0 or record.exam_score > 100:
                raise ValidationError("The score must be between 0 and 100.")











