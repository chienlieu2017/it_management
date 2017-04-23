# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
from datetime import date, datetime, timedelta
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF


class MonthlyReportIssue(models.TransientModel):
    _name = 'monthly.report.issue'

    month_nb = fields.Selection(
        selection='_get_month',
        string='Month',
        required=True)
    year_nb = fields.Selection(
        selection='_get_year',
        string='Year',
        required=True)

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
                'period': '{}-{}'.format(self.month_nb, self.year_nb),
                'period_str': d.strftime('%B %Y').upper()}
        return data

    @api.multi
    def btn_print(self):
        self.ensure_one()
        return self.env['report'].get_action(self, 'monthly_issue_report_xlsx')
