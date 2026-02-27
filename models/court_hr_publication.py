from odoo import api, fields, models

class EgpHrInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    publication_ids = fields.One2many('employee.publication', 'employee_id', string='Publication')

    # Your Python code (e.g., in a controller or model)

class EmployeePublication(models.Model):
    _name = 'employee.publication'
    _description = 'Publication'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee')
    publication_type = fields.Selection([('Book', 'Book'), ('َArticle', 'Article'), ('Subject', 'Subject'),
                                         ('Magazine', 'Magazine')], string="Publication Type")
    subject = fields.Char(string='Subject')
    publication_date = fields.Date(string='Publication Date')
    no_of_pages = fields.Integer(string='No of Pages')
    isbn = fields.Char(string='ISBN')

    attachments = fields.Many2many('ir.attachment', string="Attachments")