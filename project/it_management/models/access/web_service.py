# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
from odoo import api, fields, models


class WebService(models.Model):
    _name = "web.service"
    _description = "Web Service"
    _order = 'name'

    name = fields.Char('Domain', required=True)
    ip_addr = fields.Char('IP Address', required=True)
    panel = fields.Char('Panel', required=True)
    login = fields.Char('login', required=True)
    pwd = fields.Char('Password', required=True)
