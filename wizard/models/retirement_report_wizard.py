from odoo import models, fields, api
from odoo.exceptions import ValidationError
import datetime


class RetirementReportWizard(models.TransientModel):
    _name = 'retirement.report.wizard'
    _description = 'Employee Retirement Report Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    retirement_type_id = fields.Many2one(
        'employee.retirement.type',
        string="Retirement Type"
    )

    total_retirements = fields.Integer(
        string="Total Retirements",
        readonly=True
    )

    retirement_lines = fields.One2many(
        'retirement.report.line',
        'wizard_id',
        string="Retirement Details",
        readonly=True
    )

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError("End Date cannot be earlier than Start Date.")

    def generate_report(self):
        self.ensure_one()

        Retirement = self.env['employee.retirement']

        domain = [
            ('retirement_end_date', '>=', self.start_date),
            ('retirement_end_date', '<=', self.end_date),
        ]

        if self.retirement_type_id:
            domain.append(('retirement_type_id', '=', self.retirement_type_id.id))

        retirements = Retirement.search(domain, order='retirement_end_date asc')

        # Clear old data
        self.retirement_lines.unlink()

        for rec in retirements:
            self.env['retirement.report.line'].create({
                'wizard_id': self.id,
                'employee_id': rec.employee_id.id,
                'retirement_type_id': rec.retirement_type_id.id,
                'retirement_reason_id': rec.retirement_reason_id.id,
                'retirement_end_date': rec.retirement_end_date,
                'retirement_month': rec.retirement_month,
                'retirement_year': rec.retirement_year,
                'remarks': rec.retirement_remarks,
            })

        self.total_retirements = len(retirements)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'retirement.report.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def print_pdf_report(self):
        self.generate_report()
        return self.env.ref(
            'court_hr.action_retirement_report'
        ).report_action(self)


class RetirementReportLine(models.TransientModel):
    _name = 'retirement.report.line'
    _description = 'Employee Retirement Report Line'

    wizard_id = fields.Many2one(
        'retirement.report.wizard',
        ondelete='cascade'
    )

    employee_id = fields.Many2one('hr.employee', string="Employee")
    retirement_type_id = fields.Many2one('employee.retirement.type', string="Type")
    retirement_reason_id = fields.Many2one('employee.retirement.reason', string="Reason")

    retirement_end_date = fields.Date(string="End Date")

    retirement_month = fields.Selection(
        [
            ('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'),
            ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'),
            ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')
        ],
        string="Month"
    )

    retirement_year = fields.Char(string="Year")
    remarks = fields.Text(string="Remarks")
