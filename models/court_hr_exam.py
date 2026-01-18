# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    exam_ids = fields.One2many('employee.exam', 'employee_id', string='Exam')

# Your Python code (e.g., in a controller or model)

class EmployeeExam(models.Model):
    _name = 'employee.exam'
    _description = 'Employee Exam'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    exam_subject = fields.Char(string='Subject')
    exam_type = fields.Selection([('written_test', 'Written Test'), ('interview', 'Interview'),
                                  ('technical', 'Technical (Special Interview)'),
                                  ('computerized_exam', 'Computerized Exam'), ('english', 'English')], string="Exam Type",
                                 default='written_test')
    exam_date = fields.Date(string='Exam Date')
    exam_result = fields.Char(string='Result')
    exam_score = fields.Integer(string='Score')
    exam_remarks = fields.Text(string='Remarks')

    @api.constrains('exam_score')
    def _check_exam_score(self):
        for record in self:
            if not isinstance(record.exam_score, int):
                raise ValidationError("The score must be a valid integer.")
            if record.exam_score < 0 or record.exam_score > 100:
                raise ValidationError("The score must be between 0 and 100.")











