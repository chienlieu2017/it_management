# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import api, fields, models

SMS_STATES = [('draft', 'Draft'),
              ('100', 'Sent'),
              ('104', 'Brand name is not exits'),
              ('118', 'Message Invalid'),
              ('119', 'Brand name at least 20 number phones'),
              ('131', 'Brand name over 422 characters')]


class SmsSms(models.Model):
    _name = "sms.sms"
    _description = "SMS"

    name = fields.Char('Name', readonly=True)
    mobile_phone = fields.Integer('Mobile Phone', required=True)
    message = fields.Text('Message Content', required=True)
    datetime_sent = fields.Datetime('Datetime Sent', readonly=True)
    state = fields.Selection(SMS_STATES, 'Status', default='draft')
    error_message = fields.Text('Error Message')
    sms_template_id = fields.Many2one('sms.template', 'SMS Template')

    @api.model
    def create(self, vals):
        """
            TO DO:
            Get sequence for SMS
        """
        next_sequence = self.env['ir.sequence'].next_by_code('sms.sms')
        vals.update({'name': next_sequence})
        return super(SmsSms, self).create(vals)
