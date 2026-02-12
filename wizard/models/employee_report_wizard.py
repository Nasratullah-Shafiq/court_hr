# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EmployeeReportWizard(models.TransientModel):
    _name = 'employee.report.wizard'
    _description = 'Employee Report Wizard'

    # =========================
    # Filters
    # =========================
    job_province = fields.Many2one('res.country.state', string='Province')
    court_level = fields.Selection([
        ('مرکز', 'مرکز'),
        ('تمیز مرکزی', 'تمیز مرکزی'),
        ('تمیز زون قندهار', 'تمیز زون قندهار'),
        ('مرافعه', 'مرافعه'),
        ('ابتداییه', 'ابتداییه'),
        ('نظامی', 'نظامی')
    ], string='Court Level')

    job_status = fields.Selection([
        ('برحال', 'برحال'),
        ('منفصل', 'منفصل'),
        ('منفک', 'منفک'),
        ('معزول', 'معزول'),
        ('بی سرنوشت', 'بی سرنوشت'),
        ('متقاعد', 'متقاعد'),
        ('وفات', 'وفات')
    ], string='Job Status')

    recruitment_type = fields.Selection(
        [('حکمی', 'حکمی'), ('رقابتی', 'رقابتی')],
        string='Recruitment Type'
    )

    execution_type = fields.Selection(
        [('جدیدالتقرر', 'جدیدالتقرر'),
         ('تقرر مجدد', 'تقرر مجدد'),
         ('تبدیل', 'تبدیل'),
         ('انفصال', 'انفصال'),
         ('انفکاک', 'انفکاک'),
         ('عزل', 'عزل')],
        string='Execution Type'
    )

    ethnicity = fields.Selection(
        [
            ('pashtun', 'Pashtun'),
            ('tajik', 'Tajik'),
            ('hazara', 'Hazara'),
            ('uzbek', 'Uzbek'),
            ('turkmen', 'Turkmen'),
            ('aimak', 'Aimak'),
            ('baloch', 'Baloch'),
            ('nuristani', 'Nuristani'),
            ('pashai', 'Pashai'),
            ('sadat', 'Sadat / Sayyid'),
            ('qizilbash', 'Qizilbash'),
            ('pamiri', 'Pamiri'),
            ('bayat', 'Bayat'),
            ('arab', 'Arab'),
            ('gujar', 'Gujar'),
            ('brahui', 'Brahui'),
        ],
        string='Ethnicity'
    )

    category = fields.Selection([
        ('administrative', 'Administrative'),
        ('service', 'Service'),
        ('judicial', 'Judicial'),
        ('military', 'Military')
    ], string='Category')

    resign_date = fields.Date(string='Resign Date')

    job_id = fields.Many2one('hr.job', string='Job')
    grade_id = fields.Many2one('employee.grade', string='Grade')
    step_id = fields.Many2one('employee.step', string='Step')

    total_records = fields.Integer(readonly=True)

    employee_lines = fields.One2many(
        'employee.report.line',
        'wizard_id',
        readonly=True
    )

    # =========================
    # Logic
    # =========================
    def generate_report(self):
        self.ensure_one()

        domain = []

        if self.job_province:
            domain.append(('job_province', '=', self.job_province.id))
        if self.court_level:
            domain.append(('court_level', '=', self.court_level))
        if self.job_status:
            domain.append(('job_status', '=', self.job_status))
        if self.recruitment_type:
            domain.append(('recruitment_type', '=', self.recruitment_type))
        if self.execution_type:
            domain.append(('execution_type', '=', self.execution_type))
        if self.ethnicity:
            domain.append(('ethnicity', '=', self.ethnicity))
        if self.category:
            domain.append(('category', '=', self.category))
        if self.resign_date:
            domain.append(('resign_date', '=', self.resign_date))
        if self.job_id:
            domain.append(('job_id', '=', self.job_id.id))
        if self.grade_id:
            domain.append(('grade_id', '=', self.grade_id.id))
        if self.step_id:
            domain.append(('step_id', '=', self.step_id.id))

        employees = self.env['hr.employee'].search(domain)

        self.employee_lines.unlink()

        for emp in employees:
            self.env['employee.report.line'].create({
                'wizard_id': self.id,
                'employee_id': emp.id,
                'job_id': emp.job_id.id,
                'grade_id': emp.grade_id.id,
                'step_id': emp.step_id.id,
                'court_level': emp.court_level,
                'job_status': emp.job_status,
                'category': emp.category,
            })

        self.total_records = len(employees)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'employee.report.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def print_pdf_report(self):
        self.generate_report()
        return self.env.ref(
            'court_hr.action_employee_report'
        ).report_action(self)


class EmployeeReportLine(models.TransientModel):
    _name = 'employee.report.line'
    _description = 'Employee Report Line'

    wizard_id = fields.Many2one('employee.report.wizard', ondelete='cascade')

    employee_id = fields.Many2one('hr.employee', string='Employee')
    job_id = fields.Many2one('hr.job', string='Job')
    grade_id = fields.Many2one('employee.grade', string='Grade')
    step_id = fields.Many2one('employee.step', string='Step')

    court_level = fields.Char()
    job_status = fields.Char()
    category = fields.Char()
