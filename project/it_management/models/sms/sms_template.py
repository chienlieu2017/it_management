# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class SmsTemplate(models.Model):
    _name = "sms.template"
    _description = "SMS Template"

    name = fields.Char('Name', readonly=True)
    content = fields.Text('Template')
