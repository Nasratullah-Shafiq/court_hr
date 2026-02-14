from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re

class EgpHrInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    language_ids = fields.One2many('employee.language', 'employee_id', string='Language')


# Your Python code (e.g., in a controller or model)

class EmployeeLanguage(models.Model):
    _name = 'employee.language'
    _description = 'Language'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')

    language_id = fields.Many2one('employee.language.master', string='Language', required=True, tracking=True)

    LANGUAGE_LEVEL = [
        ('a1', 'A1 (Beginner)'),
        ('a2', 'A2 (Elementary)'),
        ('b1', 'B1 (Intermediate)'),
        ('b2', 'B2 (Upper-Intermediate)'),
        ('c1', 'C1 (Advanced)'),
        ('c2', 'C2 (Proficient)'),
        ('native', 'Native')
    ]

    # Language skill fields
    reading = fields.Selection(LANGUAGE_LEVEL, string="Reading", default='b2', tracking=True)
    speaking = fields.Selection(LANGUAGE_LEVEL, string="Speaking", default='b2', tracking=True)
    listening = fields.Selection(LANGUAGE_LEVEL, string="Listening", default='b2', tracking=True)
    writing = fields.Selection(LANGUAGE_LEVEL, string="Writing", default='b2', tracking=True)

    remarks = fields.Text(string="Remarks", tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments")

    class EmployeeLanguageMaster(models.Model):
        _name = 'employee.language.master'
        _description = 'Languages Master'

        name = fields.Char(string='Language', required=True, unique=True, translate=True)
        code = fields.Char(string='Code')  # Optional, e.g., EN, FR, PS, DA

        _sql_constraints = [
            ('unique_language', 'unique(name)', 'Language must be unique!')
        ]





