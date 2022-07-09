# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo.exceptions import UserError
from odoo import _, models, fields, api
import base64
import qrcode

from io import BytesIO


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"


    experience_ids = fields.One2many('employee.experience', 'employee_id', string='Experience', tracking=True)
    promotion_ids = fields.One2many('employee.promotions', 'employee_id', string='Fire', tracking=True)
    exam_ids = fields.One2many('employee.exam', 'employee_id', string='Exam', tracking=True)
    fire_ids = fields.One2many('employee.fire', 'employee_id', string='Fire', tracking=True)
    guarantee_ids = fields.One2many('employee.guarantee', 'employee_id', string='Guarantee', tracking=True)
    travel_ids = fields.One2many('employee.travel', 'employee_id', string='Travel', tracking=True)
    training_ids = fields.One2many('employee.training', 'employee_id', string='Training')
    reward_ids = fields.One2many('employee.reward', 'employee_id', string='reward', tracking=True)
    retirement_ids = fields.One2many('employee.retirement', 'employee_id', string='Retirement', tracking=True)
    relationship_ids = fields.One2many('employee.relatives', 'employee_id', string='Relatives', tracking=True)
    punishment_ids = fields.One2many('employee.punishment', 'employee_id', string='Punishment', tracking=True)
    publication_ids = fields.One2many('employee.publication', 'employee_id', string='Publication')
    property_ids = fields.One2many('employee.property', 'employee_id', string='Property', tracking=True)
    language_ids = fields.One2many('employee.language', 'employee_id', string='Language', tracking=True)
    health_ids = fields.One2many('employee.health', 'employee_id', string='Health', tracking=True)

    modern_education_ids = fields.One2many('employee.education', 'employee_id', string="Modern Education",
        domain=[('education_type','=','modern_education')]
    )

    islamic_education_ids = fields.One2many('employee.education', 'employee_id', string="Islamic Education",
        domain=[('education_type','=','islamic_education')]
    )

    military_education_ids = fields.One2many('employee.education', 'employee_id', string="Military Education",
        domain=[('education_type','=','military_education')]
    )

    cash_guarantee_ids = fields.One2many('employee.guarantee', 'employee_id', string="Cash Guarantees",
        domain=[('guarantee_type', '=', 'cash')], tracking=True
    )

    property_guarantee_ids = fields.One2many('employee.guarantee', 'employee_id', string="Property Guarantees",
        domain=[('guarantee_type', '=', 'property')], tracking=True
    )

    person_guarantee_ids = fields.One2many('employee.guarantee', 'employee_id', string="Person Guarantees",
        domain=[('guarantee_type', '=', 'person')], tracking=True

    )
    job_id = fields.Many2one('hr.job', string='Job', tracking=True)
    department_id = fields.Many2one('hr.department', string='Department', tracking=True)
    attachments = fields.Many2many('ir.attachment', string="Attachments", tracking=True)
    remarks = fields.Text(string='Remarks', tracking=True)
    employment_reference_number = fields.Char(
        string='Employment Number',
        copy=False,
        tracking=True,
        default='New',
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    #
    # @api.model
    # def create(self, vals):
    #     if vals.get('employment_reference_number', 'New') == 'New':
    #         vals['employment_reference_number'] = self.env['ir.sequence'].next_by_code(
    #             'employee.employment.reference'
    #         )
    #     return super().create(vals)
    #
    father_name = fields.Char(
        string='Father Name', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    grand_father_name = fields.Char(
        string='Grand Father Name', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    english_name = fields.Char(
        string='English Name', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    english_father_name = fields.Char(
        string='English Father Name', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    english_job_position = fields.Char(
        string='English Job Position', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    # ===============================
    # Personal Information
    # ===============================
    emp_gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    emp_date_of_birth = fields.Date(
        string='Date Of Birth', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    age = fields.Integer(
        string="Age", compute="_compute_age", store=True, tracking=True
    )

    retirement_count = fields.Integer(
        string="Retirement",
        compute="_compute_retirement_count",
    )

    def _compute_retirement_count(self):
        retirement_model = self.env['employee.retirement']

        for employee in self:
            employee.retirement_count = retirement_model.search_count([
                ('employee_id', '=', employee.id)
            ])

    def action_view_retirement(self):
        self.ensure_one()

        retirement = self.env['employee.retirement'].search([
            ('employee_id', '=', self.id)
        ], limit=1)

        if retirement:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Employee Retirement',
                'res_model': 'employee.retirement',
                'view_mode': 'form',
                'res_id': retirement.id,
                'target': 'current',
            }

        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Retirement',
            'res_model': 'employee.retirement',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'target': 'current',
        }
        # Automatic retirement

    @api.model
    def _cron_create_retirement_records(self):

        employees = self.search([
            ('age', '>=', 65),
            ('active', '=', True),
        ])

        retirement_model = self.env['employee.retirement']

        for employee in employees:

            existing_retirement = retirement_model.search([
                ('employee_id', '=', employee.id)
            ], limit=1)

            if existing_retirement:
                continue

            retirement_model.create({
                'employee_id': employee.id,
                'retirement_end_date': fields.Date.today(),
            })

    education_count = fields.Integer(
        string="Education",
        compute="_compute_education_count",
    )

    def _compute_education_count(self):
        education_model = self.env['employee.education']

        for employee in self:
            employee.education_count = education_model.search_count([
                ('employee_id', '=', employee.id)
            ])

    def action_view_education(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Education',
            'res_model': 'employee.education',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'target': 'current',
        }

    experience_count = fields.Integer(
        string="Experience",
        compute="_compute_experience_count",
    )

    def _compute_experience_count(self):
        experience_model = self.env['employee.experience']

        for employee in self:
            employee.experience_count = experience_model.search_count([
                ('employee_id', '=', employee.id)
            ])

    def action_view_experience(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Experience',
            'res_model': 'employee.experience',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'target': 'current',
        }

    language_count = fields.Integer(
        string="Language",
        compute="_compute_language_count",
    )

    def _compute_language_count(self):
        language_model = self.env['employee.language']

        for employee in self:
            employee.language_count = language_model.search_count([
                ('employee_id', '=', employee.id)
            ])

    def action_view_language(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Language',
            'res_model': 'employee.language',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id)],
            'target': 'current',
        }






    emp_country_of_birth = fields.Many2one(
        'res.country', string="Country of Birth", tracking=True, ondelete='cascade',
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    emp_place_of_birth = fields.Many2one(
        'res.country.state', string="Place of Birth", tracking=True, ondelete='cascade',
        domain="[('country_id', '=', emp_country_of_birth)]",
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    emp_nationality = fields.Many2one(
        'res.country', string="Nationality", tracking=True, ondelete='cascade',
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    blood_group = fields.Selection(
        [('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'),
         ('ab+', 'AB+'), ('ab-', 'AB-'), ('o+', 'O+'), ('o-', 'O-')],
        string="Blood Group", tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    marital_status = fields.Selection(
        [('single', 'Single'), ('married', 'Married'), ('widow', 'Widow')], string="Marital Status",
        tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )


    # ===============================
    # Job Information
    # ===============================
    job_id = fields.Many2one('hr.job')
    position_type = fields.Selection(
        related='job_id.position_type', string='Position Type', store=True, readonly=True, tracking=True
    )
    grade_id = fields.Many2one('employee.grade', string="Grade", tracking=True)
    step_id = fields.Many2one('employee.step', string="Step", tracking=True)

    transfer_date = fields.Date(string='Transfer Date', tracking=True)
    transfer_reason = fields.Text(string='Transfer Reason', tracking=True)
    organizer = fields.Char(string='Organizer', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert")
    arranger_id = fields.Char(string='Agreed By', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert")
    approver = fields.Char(
        string='Approver', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    resign_date = fields.Date(string='Resign Date', tracking=True)
    jihad_experience = fields.Text(string='Jihad Experience', tracking=True)
    cartotech_number = fields.Char(string='Cartotech No', tracking=True)
    category = fields.Selection([
        ('administrative', 'Administrative'),
        ('service', 'Service'),
        ('judicial', 'Judicial'),
        ('military', 'Military')
    ], string='Category', tracking=True)

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
        string='Ethnicity',
        tracking=True
    )
    language_id = fields.Many2one('employee.language.master', string='Language', tracking=True)

    religion_id = fields.Many2one('employee.religion', string='Religion', tracking=True)

    recruitment_type = fields.Selection(
        [('حکمی', 'حکمی'), ('رقابتی', 'رقابتی')],
        default="رقابتی", string="Recruitment Type", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    execution_type = fields.Selection(
        [('جدیدالتقرر', 'جدیدالتقرر'), ('تقرر مجدد', 'تقرر مجدد'), ('تبدیل', 'تبدیل'),
         ('انفصال', 'انفصال'), ('انفکاک', 'انفکاک'), ('عزل', 'عزل')],
        default="جدیدالتقرر", string="Execution Type", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    job_status = fields.Selection(
        [('برحال', 'برحال'), ('منفصل', 'منفصل'), ('منفک', 'منفک'), ('معزول', 'معزول'),
         ('بی سرنوشت', 'بی سرنوشت'), ('متقاعد', 'متقاعد'), ('وفات', 'وفات')],
        default="برحال", string="Job Status", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    court_level = fields.Selection(
        [('مرکز', 'مرکز'), ('تمیز مرکزی', 'تمیز مرکزی'), ('تمیز زون قندهار', 'تمیز زون قندهار'),
         ('مرافعه', 'مرافعه'), ('ابتداییه', 'ابتداییه'), ('نظامی', 'نظامی')],
        default="مرکز", string="Court Level", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    job_province = fields.Many2one(
        "res.country.state", string='Job Province', ondelete='restrict', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    job_district = fields.Many2one(
        'employee.district', string="Job District", tracking=True, ondelete='cascade',
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    # ===============================
    # Address Information
    # ===============================

    country_id = fields.Many2one(
        'res.country', string="Country", tracking=True,
        default=lambda self: self.env.ref('base.af', raise_if_not_found=False),
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    # Employee Permanent address information

    province_id = fields.Many2one(
        "res.country.state", string='Permanent Province', ondelete='restrict',
        domain="[('country_id', '=?', country_id)]", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    permanent_province = fields.Many2one(
        "res.country.state", string='Permanent Province', ondelete='restrict',
        domain="[('country_id', '=?', country_id)]", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    permanent_district = fields.Many2one(
        "employee.district", string='Permanent District', ondelete='restrict', tracking=True,
        domain="[('permanent_province', '=?', province_id)]",
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    permanent_village = fields.Char(
        string='Permanent Village', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    permanent_street = fields.Char(
        string='Permanent Street', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    # Employee Temporary Address

    temporary_province = fields.Many2one(
        "res.country.state", string='Temporary Province', ondelete='restrict',
        domain="[('country_id', '=?', country_id)]", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    temporary_district = fields.Many2one(
        'employee.district', string="Temporary District", tracking=True, ondelete='cascade',
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    temporary_village = fields.Char(
        string='Temporary Village', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    private_streets = fields.Char(
        string='Private Street', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    home_number = fields.Integer(
        string='Home Number', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    # ===============================
    # Identification / Passport
    # ===============================
    identification_type = fields.Selection(
        [('paper_id_card', 'Paper ID card'), ('electronic_id_card', 'Electronic ID Card')],
        string='ID Card', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    qr_code = fields.Binary(
        string="QR Code",
        compute="_compute_qr_code",
        store=False
    )

    @api.depends('name', 'father_name', 'job_id')
    def _compute_qr_code(self):
        for employee in self:
            employee_name = employee.name or ''
            father_name = employee.father_name or ''

            job_name = (
                employee.job_id.name
                if employee.job_id
                else ''
            )

            # Data stored inside QR code
            data = (
                f"اسم: {employee_name}\n"
                f"ولد: {father_name}\n"
                f"وظیفه: {job_name}"
            )

            employee.qr_code = employee._generate_qr_code(data)

    def _generate_qr_code(self, data):

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        buffered = BytesIO()

        img.save(
            buffered,
            format="PNG"
        )

        return base64.b64encode(
            buffered.getvalue()
        )

    identification_no = fields.Char(string='Identification No', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert")



    @api.onchange('identification_no')
    def _onchange_identification_no(self):
        for record in self:
            if record.identification_no:
                value = record.identification_no.replace('-', '')
                value = ''.join(c for c in value if c.isdigit())
                value = value[:13]

                if len(value) > 8:
                    record.identification_no = f"{value[:4]}-{value[4:8]}-{value[8:]}"
                elif len(value) > 4:
                    record.identification_no = f"{value[:4]}-{value[4:]}"
                else:
                    record.identification_no = value

    def action_print_employee_card(self):
        self.ensure_one()

        if self.category == 'administrative':
            return self.env.ref(
                'egp_hr_recruitment.action_administrative_employee_card'
            ).report_action(self)

        elif self.category == 'service':
            return self.env.ref(
                'egp_hr_recruitment.action_service_employee_card'
            ).report_action(self)

        elif self.category == 'judicial':
            return self.env.ref(
                'egp_hr_recruitment.action_judical_employee_card'
            ).report_action(self)

        elif self.category == 'military':
            return self.env.ref(
                'egp_hr_recruitment.action_military_employee_card'
            ).report_action(self)

        raise UserError(
            _('Please select an employee category before printing the employee card.')
        )


    identification_print_date = fields.Date(
        string='Print Date', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    identification_expiry_date = fields.Date(
        string='Expire Date', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    identification_chapter = fields.Integer(
        string='Chapter', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    identification_page_no = fields.Integer(
        string='Page No', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    passport_no = fields.Char(
        string='Passport No', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    work_permit_no = fields.Char(
        string='Work Permit No', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    passport_type = fields.Selection(
        [('ordinary_passport', 'Ordinary Passport'), ('diplomatic_passport', 'Diplomatic Passport'),
         ('service_official_passport', 'Service (Official) Passport'), ('special_passport', 'Special Passport')],
        string='Passport Type', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert", default='ordinary_passport'
    )
    passport_print_date = fields.Date(
        string='Print Date', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    passport_end_date = fields.Date(
        string='Expiry Date', tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    passport_place_of_issue = fields.Many2one(
        "res.country.state", string='Place of Issue', ondelete='restrict',
        domain="[('country_id', '=?', country_id)]", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    nic_place_of_issue = fields.Many2one(
        "res.country.state", string='Place of Issue', ondelete='restrict',
        domain="[('country_id', '=?', country_id)]", tracking=True,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    # ===============================
    # Other Fields
    # ===============================
    p2_form_no = fields.Char(
        string='P2 Form Number', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    p2_approval_date = fields.Date(
        string='P2 Approval Date', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    approval_date = fields.Date(
        string='Approval Date', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    recruitment_date = fields.Date(
        string='Recruitment Date', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )

    pezhand_department = fields.Char(
        string='Pezhand Department', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    deputy_ministry_procurement = fields.Char(
        string='Deputy Ministry of Procurement', tracking=True, groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    message_main_attachment_id = fields.Many2one(
        groups="base.group_erp_manager,egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )
    today_date = fields.Date(
        string="Today's Date", tracking=True, default=fields.Date.today,
        groups="egp_hr.group_employee_officers,egp_hr.group_employee_expert"
    )


    # ===============================
    # Onchange Methods for Districts
    # ===============================
    @api.onchange('permanent_province')
    def _onchange_permanent_province(self):
        if self.permanent_province:
            return {'domain': {'permanent_district': [('province_id', '=', self.permanent_province.id)]}}
        else:
            return {'domain': {'permanent_district': []}}

    @api.onchange('temporary_province')
    def _onchange_temporary_province(self):
        if self.temporary_province:
            return {'domain': {'temporary_district': [('province_id', '=', self.temporary_province.id)]}}
        else:
            return {'domain': {'temporary_district': []}}

    def cron_retirement_toast(self):
        today = date.today()
        employees = self.search([('emp_date_of_birth', '!=', False)])

        hr_users = self.env.ref('hr.group_hr_user').users

        for emp in employees:
            age = today.year - emp.emp_date_of_birth.year - (
                    (today.month, today.day) < (emp.emp_date_of_birth.month, emp.emp_date_of_birth.day)
            )

            # Retirement warning at age 64
            if age == 64:
                for user in hr_users:
                    user.notify_warning(
                        message=f"{emp.name} will retire next year.",
                        title="Retirement Warning",
                        sticky=False  # This makes it toast-style
                    )

            # Automatic retirement at age 65
            if age >= 65:
                exists = self.env['employee.retirement'].search([('employee_id', '=', emp.id)], limit=1)
                if not exists:
                    self.env['employee.retirement'].create({
                        'employee_id': emp.id,
                        'retirement_end_date': today,
                        'retirement_remarks': 'Automatically retired at age 65'
                    })
                    for user in hr_users:
                        user.notify_success(
                            message=f"{emp.name} has been retired automatically (age {age}).",
                            title="Employee Retired",
                            sticky=False
                        )

    @api.depends('emp_date_of_birth')
    def _compute_age(self):
        today = date.today()
        for emp in self:
            if emp.emp_date_of_birth:
                emp.age = relativedelta(today, emp.emp_date_of_birth).years
            else:
                emp.age = 0

    single_fire_record = fields.Char(
        compute='_compute_single_fire_record',
        string="Single Fire Record", tracking=True
    )

    def custom_filter_action(self):
        # Implement custom action when the button is clicked
        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Employees',
            'res_model': 'hr.employee',
            'view_mode': 'tree,form',
            'domain': [('job_id', '!=', False)],  # Example filter condition
            'target': 'current',
        }

    def _compute_single_fire_record(self):
        for record in self:
            # Check the record count in the employee.fire model for the current employee
            fire_count = self.env['employee.fire'].search_count([('employee_id', '=', record.id)])
            record.single_fire_record = (fire_count == 1)

    def fired_employee(self):
        print("These are the fired employees!")

    def active_employee(self):
        print("These are the active employees!")

    def besarnawesht_employee(self):
        print("These are the Besarnawesht employees!")

    def waiting_employee(self):
        print("These are the waiting employees!")

    def retire_employee(self):
        print("These are the retire employees!")

    def dead_employee(self):
        print("These are the dead employees!")

    def removed_employee(self):
        print("These are the Removed employees!")

    has_equipment_records = fields.Char(
        string="Has Equipment Records",
        compute="_compute_has_equipment_records", tracking=True,
        # No need to store this computed value
    )

    @api.depends_context('uid')  # Recomputes the value when the context changes
    def _compute_has_equipment_records(self):
        """
        Compute whether there are any maintenance.equipment records.
        """
        for record in self:
            record.has_equipment_records = bool(
                self.env['maintenance.equipment'].search_count([('employee_id', '=', record.id)])
            )
            # print('equipment printed')

    def notify_inventory(self):
        """
        Notify all maintenance equipment records.
        """
        # Search for all maintenance equipment records
        equipment_record = self.env['maintenance.equipment'].search([])

        if equipment_record:
            # Prepare the message
            message = "This is to notify that this user is fired, and you can check."

            # Post the message to the chatter
            equipment_record.message_post(
                body=message,
                message_type='comment',
                subtype_id=self.env.ref('mail.mt_note').id,
            )
            print("Message sent to the maintenance equipment!")
        else:
            print("No maintenance equipment record found.")

    def action_send_message(self):
        for employee in self:
            message = "Hello, this is a predefined message!"
            self.send_message_to_employee(employee.id, message)

    # this code send a message for a specific employee
    @api.model
    def send_message_to_employee(self, employee_id, message):
        employee = self.env['hr.employee'].browse(employee_id)
        if employee.user_id:
            self.env['mail.message'].create({
                'subject': 'Message',
                'body': message,
                'message_type': 'comment',
                'subtype_id': self.env.ref('mail.mt_comment').id,
                'model': 'res.users',
                'res_id': employee.user_id.id,
                'author_id': self.env.user.partner_id.id,
            })
        else:
            raise ValueError('The selected employee does not have an associated user.')






class EmployeeStep(models.Model):
    _name = 'employee.step'
    _description = 'Employee Step'

    name = fields.Char(string='Step', tracking=True, translate=True, unique=True)



class EmployeeReligion(models.Model):
    _name = 'employee.religion'
    _description = 'Religion'

    name = fields.Char(string='Religion', translate=True, unique=True, tracking=True)
