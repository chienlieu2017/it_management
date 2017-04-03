# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
import unicodedata
from odoo import api, fields, models
import requests

SMS_STATES = [('draft', 'Draft'),
              ('100', 'Sent'),
              ('103', 'Empty Money'),
              ('104', 'No Brand Name'),
              ('118', 'Message Invalid'),
              ('119', 'Need more than 20'),
              ('131', 'Brand name too long')]

SmsXmlData = """<RQST>
                <APIKEY>%s</APIKEY>
                <SECRETKEY>%s</SECRETKEY>
                <NAME>HMS Esms</NAME>
                <CONTENT>%s</CONTENT>
                <CONTACTS>
                    <CUSTOMER>
                        <PHONE>%s</PHONE>
                    </CUSTOMER>"
                </CONTACTS>
            </RQST>"""


class SmsSms(models.Model):
    _name = "sms.sms"
    _description = "SMS"

    name = fields.Char('Name', readonly=True)
    sms_id = fields.Char('SMSID', readonly=True)
    mobile_phone = fields.Char('Mobile Phone', required=True)
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

    def convert_to_nomalize(self, name):
        name_convert = ''.join((c for c in unicodedata.normalize('NFD', name)
                                if unicodedata.category(c) != 'Mn'))
        str_name_convert = name_convert.encode('utf8')
        if 'Đ' in str_name_convert:
            name_convert = str_name_convert.replace('Đ', 'D')
        if 'đ' in str_name_convert:
            name_convert = str_name_convert.replace('đ', 'd') 
        return name_convert

    @api.multi
    def button_send(self):
        ApiKey = self.env['ir.config_parameter'].get_param('sms_api_key')
        SecretKey = self.env['ir.config_parameter'].get_param('sms_secret_key')
        SmsUrl = self.env['ir.config_parameter'].get_param('sms_url')
        for sms in self:
            message = sms.sms_template_id and sms.sms_template_id.content + \
                " " + sms.message or sms.message
            message = self.convert_to_nomalize(message)
            sms_data = SmsXmlData % (ApiKey, SecretKey, message,
                                     sms.mobile_phone)
            r = requests.post(SmsUrl, data=sms_data)
            str_result = r.text.encode('utf-8').replace('</', '<')
            list_result = str_result.split('<CodeResult>')
            code_result = False
            error_message = ''
            if list_result >= 3:
                code_result = list_result[1]
                if 'ErrorMessage' in list_result[2]:
                    error_message = list_result[2].split('<ErrorMessage>')[1]
            sms.write({'state': code_result and str(code_result) or 'draft',
                       'error_message': error_message})
