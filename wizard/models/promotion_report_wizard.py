# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PromotionReportWizard(models.TransientModel):
    _name = 'promotion.report.wizard'
    _description = 'Employee Promotion Report Wizard'

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    total_promotions = fields.Integer(
        string="Total Promotions",
        readonly=True
    )

    promotion_lines = fields.One2many(
        'promotion.report.line',
        'wizard_id',
        string="Promotion Details",
        readonly=True
    )

    @api.constrains('start_date', 'end_date')
    def _check_date_range(self):
        for rec in self:
            if rec.end_date < rec.start_date:
                raise ValidationError("End Date cannot be earlier than Start Date.")

    def generate_report(self):
        self.ensure_one()

        Promotion = self.env['employee.promotions']

        domain = [
            ('approval_date', '>=', self.start_date),
            ('approval_date', '<=', self.end_date),
        ]

        promotions = Promotion.search(domain, order='approval_date asc')

        # Clear old lines
        self.promotion_lines.unlink()

        for rec in promotions:
            self.env['promotion.report.line'].create({
                'wizard_id': self.id,
                'employee_id': rec.employee_id.id,
                'approval_no': rec.approval_no,
                'proposal_no': rec.proposal_no,
                'order_no': rec.order_no,
                'rank_promotion': rec.rank_promotion,
                'offer_date': rec.offer_date,
                'proposal_date': rec.proposal_date,
                'order_date': rec.order_date,
                'approval_date': rec.approval_date,
                'remarks': rec.promotion_remarks,
            })

        self.total_promotions = len(promotions)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'promotion.report.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def print_pdf_report(self):
        self.generate_report()
        return self.env.ref(
            'court_hr.action_promotion_report'
        ).report_action(self)


class PromotionReportLine(models.TransientModel):
    _name = 'promotion.report.line'
    _description = 'Employee Promotion Report Line'

    wizard_id = fields.Many2one(
        'promotion.report.wizard',
        ondelete='cascade'
    )

    employee_id = fields.Many2one('hr.employee', string="Employee")

    approval_no = fields.Char(string="Approval No")
    proposal_no = fields.Char(string="Proposal No")
    order_no = fields.Integer(string="Order No")

    rank_promotion = fields.Char(string="Rank Promotion")

    offer_date = fields.Date(string="Offer Date")
    proposal_date = fields.Date(string="Proposal Date")
    order_date = fields.Date(string="Order Date")
    approval_date = fields.Date(string="Approval Date")

    remarks = fields.Text(string="Remarks")
