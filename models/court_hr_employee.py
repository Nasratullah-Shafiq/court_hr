# -*- coding: utf-8 -*-
from email.policy import default
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    _description = "Human Resource"

    father_name = fields.Char(string='Father Name', tracking=True,
                              groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    grand_father_name = fields.Char(string='Grand Father Name',
                                    groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    job_step = fields.Selection([
        ('first_step', 'First Step'),
        ('second_step', 'Second Step'),
        ('third_step', 'Third Step'),
        ('fourth_step', 'Fourth Step'),
        ('fourth_step', 'Fourth Step'),
        ('fifth_step', 'Fifth Step'),
        ('sixth_step', 'Sixth Step'),
        ('seventh_step', 'Seventh Step'),
        ('eight_step', 'Eight Step'),
        ('ninth_step', 'Ninth Step'),
        ('tenth_step', 'Tenth Step'),
        ('first_rank', 'First Rank'),
        ('second_rank', 'Second Rank'),
        ('third_rank', 'Third Rank'),
        ('fourth_rank', 'Fourth Rank'),
        ('fourth_rank', 'Fourth Rank'),
        ('fifth_rank', 'Fifth Rank'),
        ('sixth_rank', 'Sixth Rank'),
        ('seventh_rank', 'Seventh Rank'),
        ('eight_rank', 'Eight Rank'),
        ('ninth_rank', 'Ninth Rank'),
        ('tenth_rank', 'Tenth Rank'),
        ('super_rank', 'Super Rank'),
        ('superior_rank', 'Superior Rank'),
        ('unranked', 'Unranked'),
        ('prof', 'Professor'),
        ('scholar', 'Scholar'),
        ('phanmal', 'Pohanmal'),
        ('pohand', 'Pohand')
    ], string="Step / Rank", groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    job_id = fields.Many2one('hr.job')

    position_type = fields.Selection(
        related='job_id.position_type',
        string='Position Type',
        store=True,
        readonly=True
    )

    recruitment_type = fields.Selection([
        ('حکمی', 'حکمی'),
        ('رقابتی', 'رقابتی')
    ], default="رقابتی", string="Recruitment Type",
        groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    execution_type = fields.Selection([
        ('جدیدالتقرر', 'جدیدالتقرر'),
        ('تقرر مجدد', 'تقرر مجدد'),
        ('تبدیل', 'تبدیل'),
        ('انفصال', 'انفصال'),
        ('انفکاک', 'انفکاک'),
        ('عزل', 'عزل')
    ], default="جدیدالتقرر", string="Execution Type",
        groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    p2_form_no = fields.Char(string='P2 Form Number',
                             groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    p2_approval_date = fields.Date(string='P2 Approval Date',
                                   groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    court_level = fields.Selection([
        ('مرکز', 'مرکز'),
        ('تمیز مرکزی', 'تمیز مرکزی'),
        ('تمیز زون قندهار', 'تمیز زون قندهار'),
        ('مرافعه', 'مرافعه'),
        ('ابتداییه', 'ابتداییه'),
        ('نظامی', 'نظامی')
    ], default="مرکز", string="Court Level",
        groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    job_status = fields.Selection([
        ('برحال', 'برحال'),
        ('منفصل', 'منفصل'),
        ('منفک', 'منفک'),
        ('معزول', 'معزول'),
        ('بی سرنوشت', 'بی سرنوشت'),
        ('متقاعد', 'متقاعد'),
        ('وفات', 'وفات')
    ], default="برحال", string="Job Status",
        groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    message_main_attachment_id = fields.Many2one(
        groups="base.group_erp_manager,court_hr.group_employee_officers,court_hr.group_employee_expert")

    approval_date = fields.Date(string='Approval Date',
                                groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    recruitment_date = fields.Date(string='Recruitment Date',
                                   groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    approver = fields.Char(string='Approver',
                           groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    pezhand_department = fields.Char(string='Pezhand Department',
                                     groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    deputy_ministry_procurement = fields.Char(string='Deputy Ministry of Procurement',
                                              groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('widow', 'Widow'),
    ], string="Marital Status", groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    blood_group = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string="Blood Group", groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    start_date = fields.Date(string='Start Date',
                             groups="court_hr.group_employee_officers,court_hr.group_employee_expert"),
    end_date = fields.Date(string='End Date', groups="court_hr.group_employee_officers,court_hr.group_employee_expert"),

    identification_type = fields.Selection([('paper_id_card', 'Paper ID card'),
                                            ('electronic_id_card', 'Electronic ID Card')],
                                           string='ID Card',
                                           groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    identification_no = fields.Char(string='Identification No',
                                    groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    identification_print_date = fields.Date(string='Print Date',
                                            groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    identification_expiry_date = fields.Date(string='Expire Date',
                                             groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    identification_chapter = fields.Integer(string='Chapter',
                                            groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    identification_page_no = fields.Integer(string='Page No',
                                            groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    # permanent_province = fields.Many2one('res.country.state', string="Permanent Province", tracking=True, ondelete='cascade')
    # temporary_province = fields.Many2one('res.country.state', string="Temporary Province", tracking=True, ondelete='cascade')
    # Use the same variable for both fields

    permanent_district = fields.Many2one('employee.district', string="Permanent District", tracking=True,
                                         ondelete='cascade',
                                         groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    temporary_district = fields.Many2one('employee.district', string="Temporary District", tracking=True,
                                         ondelete='cascade',
                                         groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    permanent_village = fields.Char(string='Permanent Village', tracking=True,
                                    groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    temporary_village = fields.Char(string='Temporary Village', tracking=True,
                                    groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    home_number = fields.Integer(string='Home Number', tracking=True,
                                 groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    permanent_street = fields.Char(string='Permanent Street', tracking=True,
                                   groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    private_streets = fields.Char(string='Private Street', tracking=True,
                                  groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    passport_print_date = fields.Date(string='Print Date', tracking=True,
                                      groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    passport_end_date = fields.Date(string='Expiry Date', tracking=True,
                                    groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    passport_type = fields.Selection(
        [('ordinary_passport', 'Ordinary Passport'), ('diplomatic_passport', 'Diplomatic Passport'),
         ('service_official_passport', 'Service (Official) Passport'), ('special_passport', 'Special Passport')],
        string='Passport Type',
        tracking=True,
        groups="court_hr.group_employee_officers,court_hr.group_employee_expert", default='ordinary_passport')

    emp_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender',
                                  tracking=True,
                                  groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    emp_date_of_birth = fields.Date(string='Date Of Birth', tracking=True,
                                    groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    emp_country_of_birth = fields.Many2one('res.country', string="Country of Birth", tracking=True, ondelete='cascade',
                                           groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    emp_place_of_birth = fields.Many2one('res.country.state', string="Place of Birth", tracking=True,
                                         ondelete='cascade', domain="[('country_id', '=', emp_country_of_birth)]",
                                         groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    emp_nationality = fields.Many2one('res.country', string="Nationality", tracking=True, ondelete='cascade',
                                      groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    religion = fields.Char(string='Religion', tracking=True,
                           groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    today_date = fields.Date(string="Today's Date", tracking=True, default=fields.Date.today,
                             groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    # Define the list of provinces once
    PROVINCES = [
        ('Badakhshan', 'Badakhshan'),
        ('Badghis', 'Badghis'),
        ('Baghlan', 'Baghlan'),
        ('Balkh', 'Balkh'),
        ('Bamyan', 'Bamyan'),
        ('Daykundi', 'Daykundi'),
        ('Farah', 'Farah'),
        ('Faryab', 'Faryab'),
        ('Ghazni', 'Ghazni'),
        ('Ghor', 'Ghor'),
        ('Helmand', 'Helmand'),
        ('Herat', 'Herat'),
        ('Jowzjan', 'Jowzjan'),
        ('Kabul', 'Kabul'),
        ('Kandahar', 'Kandahar'),
        ('Kapisa', 'Kapisa'),
        ('Khost', 'Khost'),
        ('Kunar', 'Kunar'),
        ('Kunduz', 'Kunduz'),
        ('Laghman', 'Laghman'),
        ('Logar', 'Logar'),
        ('Nangarhar', 'Nangarhar'),
        ('Nimroz', 'Nimroz'),
        ('Nuristan', 'Nuristan'),
        ('Paktia', 'Paktia'),
        ('Paktika', 'Paktika'),
        ('Panjshir', 'Panjshir'),
        ('Parwan', 'Parwan'),
        ('Samangan', 'Samangan'),
        ('Sar-e Pol', 'Sar-e Pol'),
        ('Takhar', 'Takhar'),
        ('Urozgan', 'Urozgan'),
        ('Wardak', 'Wardak'),
        ('Zabul', 'Zabul')
    ]
    permanent_province = fields.Selection(PROVINCES, string="Province",
                                          groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    temporary_province = fields.Selection(PROVINCES, string="Province",
                                          groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    job_province = fields.Selection(PROVINCES, string="Province",
                                    groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    job_district = fields.Many2one('employee.district', string="Permanent District", tracking=True,
                                   ondelete='cascade',
                                   groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    passport_place_of_issue = fields.Selection(PROVINCES, string="Place of Issue",
                                               groups="court_hr.group_employee_officers,court_hr.group_employee_expert")
    nic_place_of_issue = fields.Selection(PROVINCES, string="Place of Issue",
                                          groups="court_hr.group_employee_officers,court_hr.group_employee_expert")

    age = fields.Integer(
        string="Age",
        compute="_compute_age",
        store=True
    )

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
        string="Single Fire Record"
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
        compute="_compute_has_equipment_records",
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
