from odoo import models, fields


class EmployeeCriminalInfo(models.Model):
    _name = 'employee.criminal.info'
    _description = 'Employee Criminal Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # =========================
    # Basic Information
    # =========================
    employee_id = fields.Many2one('hr.employee', string='Employee', tracking=True)

    letter_no = fields.Char(string='Letter Number', required=True, tracking=True)
    responsibility = fields.Text(string='Responsibility', tracking=True)
    non_responsibility = fields.Text(string='Non-Responsibility', tracking=True)
    letter_date = fields.Date(string='Document Date', tracking=True)
    remarks = fields.Text(string='Remarks')
    attachments = fields.Many2many('ir.attachment', string='Attachments')
