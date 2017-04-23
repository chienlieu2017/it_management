# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
from datetime import timedelta, datetime
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
    _order = 'id desc'

    name = fields.Char(
        string="Reference",
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
    product_id = fields.Many2one(
        string="Current",
        track_visibility='onchange',
        comodel_name="product.product",
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
    description = fields.Html(
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
    feedback = fields.Html(
        string="Feedback",
        track_visibility='onchange',)
    state = fields.Selection(RP_ISSUE_STATES,
        string='Status',
        track_visibility='onchange',
        default='draft')
    kpi = fields.Integer(
        string="KPI Coeficient",
        default=100)
    comment_ids = fields.One2many(
        string="Comments",
        comodel_name="issue.comment",
        inverse_name="issue_id"
        )
    department_id = fields.Many2one(
        string="Department",
        comodel_name="res.partner.department")

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
            r.count_down = val > 0.0 and val or 0.0
    
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
            mobile_str = Param.get_param('issue_raise_phone')
            if not mobile_str:
                return res
            sms_tmpl = self.env.ref('it_management.sms_template_default')
            mobiles = mobile_str.split(';')
            for mobile in mobiles:
                mobile = mobile.strip()
                vals = {'sms_template_id': sms_tmpl.id,
                        'mobile_phone': mobile,
                        'message': u'[{}] {} (KH: {})'.format(res.name,
                                                              res.summary,
                                                              res.partner_id.name
                                                              )}
                sms = self.env['sms.sms'].create(vals)
                sms.button_send()
        return res

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.supporter_id:
                self.assignee_id = self.partner_id.supporter_id
            if self.partner_id.department_id:
                self.department_id = self.partner_id.department_id

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
                if not r.assignee_id:
                    continue
                # send notify mail
                xmlid = 'it_management.email_template_issue_report_assigned'
                template = self.env.ref(xmlid)
                template.send_mail(r.id, force_send=True)

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

    @api.model
    def get_state_dict(self):
        res = dict(RP_ISSUE_STATES)
        return res

    @api.model
    def get_ratio(self, type='daily'):
        t_now = datetime.now()
        t_now_tz = fields.Datetime.context_timestamp(self, t_now)
        d_from = d_to = None
        d_to = t_now_tz.strftime('%Y-%m-%d 23:59:59')
        if type == 'daily':
            d_from = t_now_tz.strftime('%Y-%m-%d 00:00:00')
        else:  # Monthly
            d_from = t_now_tz.strftime('%Y-%m-01 00:00:00')
        Converter = self.env['ir.fields.converter']
        d_from = Converter._str_to_datetime(None, None, d_from)[0]
        d_to = Converter._str_to_datetime(None, None, d_to)[0]
        sql = '''
        SELECT state, COUNT(1) AS nb
        FROM issue_report
        WHERE create_date BETWEEN '{}' AND '{}'
        GROUP BY state
        '''.format(d_from, d_to)
        self.env.cr.execute(sql)
        lines = self.env.cr.dictfetchall()
        res = dict(RP_ISSUE_STATES)
        for k in res.keys():
            res[k] = 0.0
        l_sum = sum([float(l['nb']) for l in lines]) or 0.0
        for l in lines:
            if l['state'] not in res:
                continue
            res[l['state']] = (l['nb'] / l_sum) * 100
        return res

    @api.model
    def get_daily_report_recipient(self, g='Employees / Employee'):
        args = [('full_name', '=', g)]
        group = self.env['res.groups'].search(args, limit=1)
        res = ''
        if group:
            sql = '''
            SELECT uid
            FROM res_groups_users_rel
            WHERE gid = {}
            '''.format(group.id)
            self._cr.execute(sql)
            lines = self._cr.fetchall()
            uids = []
            for l in lines:
                uids.append(l[0])
            users = self.env['res.users'].browse(uids)
            emails = []
            for u in users:
                if u.active and u.email:
                    emails.append(u.email)
            res = emails and ', '.join(emails) or ''
        return res
        

    @api.model
    def _send_issue_statistics(self):
        mail_tmpl = \
            self.env.ref('it_management.email_template_issue_report_daily')
        mail_tmpl.send_mail(self.env.uid, force_send=True)
