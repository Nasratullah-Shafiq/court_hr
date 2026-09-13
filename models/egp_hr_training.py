# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

# Your Python code (e.g., in a controller or model)

class EmployeeTraining(models.Model):
    _name = 'employee.training'
    _description = 'Employee Training'
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


    course_id = fields.Many2one('employee.course', string="Course", tracking=True)
    training_location = fields.Char(string='Training Location', tracking=True)
    training_start_date = fields.Date(string='Start Date', tracking=True)
    training_end_date = fields.Date(string='End Date', tracking=True)
    training_type = fields.Selection([('administrative', 'Administrative'), ('judicial', 'Judicial'),
                                      ('military', 'Military')], string="Training Type",
                                       tracking=True)
    training_result = fields.Selection([('supreme', 'Supreme'), ('Excellent', 'Excellent'), ('Good', 'Good'),
                                        ('medium', 'medium'), ('elementary', 'elementary')], string="Training Result", tracking=True)
    letter_no = fields.Char(string='Letter No', tracking=True)
    letter_date = fields.Date(string='Letter Date')
    training_certification = fields.Char(string='Certification', tracking=True)
    training_remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)



class EmployeeCourse(models.Model):
    _name = 'employee.course'
    _description = 'Employee Course'

    name = fields.Char(string='Course')

    @api.constrains('name')
    def _check_unique_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name)]) > 1:
                raise ValidationError("The course name must be unique!")



























