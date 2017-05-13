# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
from datetime import date, datetime, timedelta
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class MonthlyReport(models.TransientModel):
    _name = 'monthly.report'

    month_nb = fields.Selection(
        selection='_get_month',
        string='Month',
        required=True)
    year_nb = fields.Selection(
        selection='_get_year',
        string='Year',
        required=True)
    customer_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner")

    @api.model
    def _get_month(self):
        return [(i, str(i)) for i in range(1, 13)]

    @api.model
    def _get_year(self):
        y = date.today().year
        l = range(y - 9, y + 1)
        l.reverse()
        return [(i, str(i)) for i in l]

    @api.multi
    def get_date_data(self):
        self.ensure_one()
        from_date = '{}-{}-1 00:00:00'.format(self.year_nb, self.month_nb)
        to_date = date(int(self.year_nb), int(self.month_nb) + 1, 1) - timedelta(days=1)
        to_date = '{}-{}-{} 23:59:59'.format(self.year_nb, self.month_nb,
                                             to_date.day)
        Converter = self.env['ir.fields.converter']
        from_date = Converter._str_to_datetime(None, None, from_date)[0]
        to_date = Converter._str_to_datetime(None, None, to_date)[0]
        d = datetime.strptime(to_date, DTF)
        data = {'to_date': to_date,
                'from_date': from_date,
                'customer_id': self.customer_id.id,
                'period': '{}-{}'.format(self.month_nb, self.year_nb),
                'period_str': d.strftime('%B %Y').upper()}
        return data

    @api.multi
    def get_monthly_data_header(self):
        params = self.get_date_data()
        from_date = fields.Datetime.from_string(params['from_date'])
        from_date = fields.Datetime.context_timestamp(self, from_date)
        from_date = from_date.strftime('%d/%m/%Y')
        to_date = fields.Datetime.from_string(params['to_date'])
        to_date = fields.Datetime.context_timestamp(self, to_date)
        to_date = to_date.strftime('%d/%m/%Y')
        res = {'from_date': from_date,
               'to_date': to_date,
               'customer_name': self.customer_id.name or '',
               'phone': self.customer_id.phone or '',
               'email': self.customer_id.email or ''
               }
        return res

    @api.multi
    def get_monthly_data_access_right(self):
        params = self.get_date_data()
        w_clause = ''
        if params['customer_id']:
            w_clause = 'WHERE dra.company_id = {0}'.format(params['customer_id'])
        sql = '''
        SELECT df.name,
            rp.name,
            dral.p_read,
            dral.p_create,
            dral.p_write,
            dral.p_delete,
            dral.notes
        FROM data_right_access dra
        LEFT JOIN data_right_access_line dral
            ON dral.data_access_id = dra.id
        LEFT JOIN res_partner rp
            ON rp.id = dra.partner_id
        LEFT JOIN data_folder df
            ON df.id = dral.folder_id
        {}
        ORDER BY df.name
        '''.format(w_clause)
        self._cr.execute(sql)
        datas = self._cr.fetchall()
        return datas

    @api.model
    def get_product_by_category(self, categ_type, params):
        w_clause = ''
        if params['customer_id']:
            w_clause = 'AND pt.partner_id = {}'.format(params['customer_id'])
        sql = '''
        SELECT pt.name,
            rp.name,
            pt.id,
            pt.warning_message
        FROM  product_template pt
        JOIN product_category pc
            ON pc.id = pt.categ_id
        LEFT JOIN res_partner rp
            ON rp.id = pt.contact_partner_id
        WHERE pc.categ_type = '{0}'
        {1}
        ORDER BY pt.name
        '''.format(categ_type, w_clause)
        self._cr.execute(sql)
        datas = self._cr.fetchall()
        return datas


    @api.multi
    def get_product_detail(self, product_tmpl_id):
        template = self.env['product.template'].browse(product_tmpl_id)
        if not template:
            return res
        atts = []
        for att in template.attribute_line_ids:
            val = []
            att_name = att.attribute_id.name
            att_lines = [l.name for l in att.value_ids if l.name]
            if att_name:
                val.append(att_name)
            if att_lines:
                val.append(', '.join(att_lines))
            if val:
                atts.append(': '.join(val))
        return atts

    @api.multi
    def get_monthly_devices(self):
        params = self.get_date_data()
        categ_type = ['hardware', 'software']
        categ_type_dict = {'hardware': 'DEVICE LIST',
                           'software': 'SOFTWARE LIST'}
        datas = []
        for ctype in categ_type:
            prod_data = self.get_product_by_category(ctype, params)
            datas.append([categ_type_dict[ctype], prod_data])
        return datas

    @api.multi
    def btn_print(self):
        self.ensure_one()
        ctx = self._context
        if ctx.get('report_template'):
            return self.env['report'].get_action(self, ctx['report_template'])

    @api.model
    def _send_monthly_report(self):
        partners = self.env['res.partner'].search([('send_monthly_report', '=',
                                                    True),
                                                   ('customer', '=', True)])
        if not partners:
            return False
        Network = self.env['network.map']
        Attachement = self.env['ir.attachment']
        tday = fields.Datetime.context_timestamp(self, datetime.now())
        vals = {'month_nb': int(tday.strftime('%m')) - 1,
                'year_nb': int(tday.strftime('%Y')),
                'customer_id': None}
        mail_tmpl = \
            self.env.ref('it_management.email_template_issue_report_monthly')
        for p in partners:
            vals.update({'customer_id': p.id})
            new_r = self.create(vals)
            new_mail_id = mail_tmpl.send_mail(new_r.id)
            new_mail = self.env['mail.mail'].browse(new_mail_id)
            # search network
            network = Network.search([('partner_id', '=', p.id)], limit=1)
            if network:
                attachments = Attachement.search([('res_model', '=',
                                                   'network.map'),
                                                  ('res_id', '=', network.id)])
                if attachments:
                    new_mail.attachment_ids += attachments
            new_mail.send()
