from odoo import api, fields, models

class EgpHrInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    travel_ids = fields.One2many('employee.travel', 'employee_id', string='Travel')

# Your Python code (e.g., in a controller or model)

class EmployeeTravel(models.Model):
    _name = 'employee.travel'
    _description = 'Travel'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    country = fields.Many2one('res.country', string="Country", tracking=True)
    # province = fields.Many2one('res.country.state', string="Province", tracking=True)
    province = fields.Many2one(
        'res.country.state',
        string="Province",
        tracking=True,
        domain="[('country_id', '=', country)]"
    )
    travel_start_date = fields.Date(string='Start Date')
    travel_end_date = fields.Date(string='End Date')
    remarks = fields.Text(string='Remarks')