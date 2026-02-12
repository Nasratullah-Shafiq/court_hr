# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EducationReportWizard(models.TransientModel):
    _name = 'education.report.wizard'
    _description = 'Employee Education Report Wizard'

    university_id = fields.Many2one(
        'employee.university',
        string='University'
    )

    degree_id = fields.Many2one(
        'employee.degree',
        string='Degree'
    )

    faculty_id = fields.Many2one(
        'employee.faculty',
        string='Faculty'
    )

    total_records = fields.Integer(
        string="Total Records",
        readonly=True
    )

    education_lines = fields.One2many(
        'education.report.line',
        'wizard_id',
        string="Education Details",
        readonly=True
    )

    def generate_report(self):
        self.ensure_one()

        Education = self.env['employee.education']

        domain = []

        if self.university_id:
            domain.append(('university_id', '=', self.university_id.id))

        if self.degree_id:
            domain.append(('degree_id', '=', self.degree_id.id))

        if self.faculty_id:
            domain.append(('faculty_id', '=', self.faculty_id.id))

        educations = Education.search(domain)

        # Clear old lines
        self.education_lines.unlink()

        for edu in educations:
            self.env['education.report.line'].create({
                'wizard_id': self.id,
                'employee_id': edu.employee_id.id,
                'country_id': edu.country_id.id,
                'province_id': edu.province_id.id,
                'degree_id': edu.degree_id.id,
                'university_id': edu.university_id.id,
                'faculty_id': edu.faculty_id.id,
                'major': edu.major,
                'education_start_date': edu.education_start_date,
                'education_end_date': edu.education_end_date,
                'batch_no': edu.batch_no,
                'remarks': edu.education_remarks,
            })

        self.total_records = len(educations)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'education.report.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def print_pdf_report(self):
        self.generate_report()
        return self.env.ref(
            'court_hr.action_employee_education_report'
        ).report_action(self)

class EducationReportLine(models.TransientModel):
    _name = 'education.report.line'
    _description = 'Employee Education Report Line'

    wizard_id = fields.Many2one(
        'education.report.wizard',
        ondelete='cascade'
    )

    employee_id = fields.Many2one('hr.employee', string="Employee")

    country_id = fields.Many2one('res.country', string="Country")
    province_id = fields.Many2one('res.country.state', string="Province")

    degree_id = fields.Many2one('employee.degree', string="Degree")
    university_id = fields.Many2one('employee.university', string="University")
    faculty_id = fields.Many2one('employee.faculty', string="Faculty")

    major = fields.Char(string="Major")

    education_start_date = fields.Date(string="Start Date")
    education_end_date = fields.Date(string="End Date")

    batch_no = fields.Integer(string="Batch No")
    remarks = fields.Text(string="Remarks")
