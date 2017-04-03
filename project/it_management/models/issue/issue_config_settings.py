# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class IssueConfigSettings(models.TransientModel):
    _name = 'issue.config.settings'
    _inherit = 'res.config.settings'

    issue_report_count_down_time = fields.Float(
        'Report Issue Count Down Time')
    issue_raise_phone = fields.Char(
        'Receive Issue Mobile Phone Nb')
    is_raise_phone = fields.Boolean(
        'Send Notify SMS?')

    @api.model
    def get_default_is_raise_phone(self, fields):
        """
        Read default value from system parameter
        """
        Param = self.env['ir.config_parameter']
        config = Param.get_param('is_raise_phone', '0')
        return {
            'is_raise_phone': eval(config),
        }

    @api.multi
    def set_default_is_raise_phone(self):
        """
        Update changing configurations to system parameter
        """
        self.ensure_one()
        Param = self.env['ir.config_parameter']
        config = self.is_raise_phone or '0'
        Param.set_param('is_raise_phone', config)

    @api.model
    def get_default_issue_raise_phone(self, fields):
        """
        Read default value from system parameter
        """
        Param = self.env['ir.config_parameter']
        config = Param.get_param('issue_raise_phone')
        return {
            'issue_raise_phone': config,
        }

    @api.multi
    def set_default_issue_raise_phone(self):
        """
        Update changing configurations to system parameter
        """
        self.ensure_one()
        Param = self.env['ir.config_parameter']
        config = self.issue_raise_phone or '0'
        Param.set_param('issue_raise_phone', config)

    @api.model
    def get_default_issue_report_count_down_time(self, fields):
        """
        Read default value from system parameter
        """
        Param = self.env['ir.config_parameter']
        config = Param.get_param('issue_report_count_down_time')

        try:
            config = float(config)
        except:
            config = 0.0

        return {
            'issue_report_count_down_time': config,
        }

    @api.multi
    def set_default_issue_report_count_down_time(self):
        """
        Update changing configurations to system parameter
        """
        self.ensure_one()
        Param = self.env['ir.config_parameter']
        config = self.issue_report_count_down_time or 0.0

        Param.set_param('issue_report_count_down_time', config)
