from odoo import api, fields, models



# Your Python code (e.g., in a controller or model)

class EmployeeHealth(models.Model):
    _name = 'employee.health'
    _description = 'Health'

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

    health_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('stable', 'Stable'),
        ('under_treatment', 'Under Treatment'),
        ('under_operation', 'Under Operation'),
        ('recovering', 'Recovering'),
        ('chronic_condition', 'Chronic Condition'),
        ('temporary_illness', 'Temporary Illness'),
        ('injured', 'Injured'),
        ('disabled', 'Disabled'),
        ('medical_leave', 'On Medical Leave'),
        ('critical', 'Critical'),
    ], string="Health Status", tracking=True)
    health_report_date = fields.Date(string='Report Date', tracking=True)
    health_remarks = fields.Text(string='Remarks', tracking=True)

    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)
