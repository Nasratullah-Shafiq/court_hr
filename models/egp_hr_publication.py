from odoo import api, fields, models


    # Your Python code (e.g., in a controller or model)

class EmployeePublication(models.Model):
    _name = 'employee.publication'
    _description = 'Publication'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee',tracking=True)
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

    publication_type = fields.Selection([('Book', 'Book'), ('َArticle', 'Article'), ('Subject', 'Subject'),
                                         ('Magazine', 'Magazine')], string="Publication Type",tracking=True)
    subject = fields.Char(string='Subject',tracking=True)
    publication_date = fields.Date(string='Publication Date',tracking=True)
    no_of_pages = fields.Integer(string='No of Pages',tracking=True)
    isbn = fields.Char(string='ISBN',tracking=True)

    remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)