# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class AccessSystem(models.Model):
    _name = "access.system"
    _description = "Access System"
    _order = 'name'

    name = fields.Char('Name', required=True)
    remote_info = fields.Char('Remote Info', required=True)
    local_ip = fields.Char('Local IP', required=True)
    login = fields.Char('Login', required=True)
    password = fields.Char('Password', required=True)
    remark = fields.Text('Remark')
    type = fields.Selection([('server', 'Server'),
                             ('system', 'System')],
                            string="Type")
