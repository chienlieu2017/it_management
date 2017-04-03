# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
from datetime import timedelta
from odoo import api, fields, models


RP_ISSUE_STATES = [('draft', 'Draft'),
                   ('assign', 'Assigned'),
                   ('wip', 'WIP'),
                   ('fix', 'Fixed'),
                   ('confirm', 'Customer Confirmed'),
                   ('close', 'Closed'),
                   ('cancel', 'Cancelled')]

class IssueReport(models.Model):
    _name = "issue.report"
    _inherit = ['mail.thread']
    _description = "Report Issue"

    name = fields.Char(
        string="Name",
        default="/",
        readonly=True)
    estimated_time = fields.Float(
        track_visibility='onchange',
        string="Estimated Time")
    partner_id = fields.Many2one(
        string="Customer",
        track_visibility='onchange',
        comodel_name="res.partner",
        required=True)
    summary = fields.Char(
        string="Summary",
        track_visibility='onchange',
        required=True)
    create_date = fields.Datetime(
        string="Creation Date",
        track_visibility='onchange',
        readonly=True,
        default=fields.Datetime.now)
    date_done = fields.Datetime(
        string="Completed Date",
        track_visibility='onchange')
    description = fields.Text(
        string="Description",
        track_visibility='onchange',)
    assignee_id = fields.Many2one(
        string="Assigned to",
        comodel_name="res.users",
        track_visibility='onchange',)
    create_uid = fields.Many2one(
        string="Reporter",
        comodel_name="res.users",
        default=lambda self: self.env.uid,
        readonly=True)
    count_down = fields.Float(
        string="Count Down",
        compute="_compute_count_down",
        track_visibility='onchange',)
    feedback = fields.Text(
        string="Feedback",
        track_visibility='onchange',)
    state = fields.Selection(RP_ISSUE_STATES,
        string='Status',
        track_visibility='onchange',
        default='draft')
    comment_ids = fields.One2many(
        string="Comments",
        comodel_name="issue.comment",
        inverse_name="issue_id"
        )

    @api.multi
    def _compute_count_down(self):
        countdown = self._get_count_down_time()
        for r in self:
            val = 0.0
            if r.create_date:
                n = fields.Datetime.now()
                n = fields.Datetime.from_string(n)
                c = fields.Datetime.from_string(r.create_date)
                diff = n - c
                secs = diff.total_seconds()
                mins = int(secs/60)
                val = countdown - mins
            r.count_down = val
    
    @api.model
    def _get_count_down_time(self):
        Parameter = self.env['ir.config_parameter'].sudo()
        countdown = Parameter.get_param('issue_report_count_down_time')
        countdown = countdown and float(countdown) or 0.0
        return countdown

    @api.model
    def create(self, vals):
        next_sequence = self.env['ir.sequence'].next_by_code('ISS')
        vals.update({'name': next_sequence})
        res = super(IssueReport, self).create(vals)
        # Send notify sms
        Param = self.env['ir.config_parameter']
        send_notify = Param.get_param('is_raise_phone', '0')
        try:
            send_notify = eval(send_notify)
        except:
            send_notify = 0
        if send_notify:
            mobile = Param.get_param('issue_raise_phone')
            if mobile:
                sms_tmpl = self.env.ref('it_management.sms_template_default')
                vals = {'sms_template_id': sms_tmpl.id,
                        'mobile_phone': mobile,
                        'message': u'[{}] {}'.format(res.name, res.summary)}
                sms = self.env['sms.sms'].create(vals)
                sms.button_send()
        return res

    @api.multi
    def action_cancel(self):
        for r in self:
            if r.state in ('draft', 'assign', 'wip'):
                r.state = 'cancel'

    @api.multi
    def action_draft(self):
        for r in self:
            if r.state in ('cancel',):
                r.state = 'draft'

    @api.multi
    def action_assign(self):
        for r in self:
            if r.state in ('draft',):
                r.state = 'assign'

    @api.multi
    def action_wip(self):
        for r in self:
            if r.state in ('assign',):
                r.state = 'wip'

    @api.multi
    def action_fix(self):
        for r in self:
            if r.state in ('wip',):
                r.state = 'fix'

    @api.multi
    def action_confirm(self):
        for r in self:
            if r.state in ('fix',):
                r.state = 'confirm'

    @api.multi
    def action_close(self):
        for r in self:
            if r.state in ('confirm',):
                r.state = 'close'

    @api.multi
    def action_reopen(self):
        for r in self:
            if r.state in ('close',):
                r.state = 'assign'
