# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
from odoo import api, fields, models


class InternetProvider(models.Model):
    _name = "internet.provider"
    _description = "Internet Provider"
    _order = 'name'

    name = fields.Char('Name', required=True)
    login = fields.Char('Internet Login', required=True)
    pwd = fields.Char('Internet Password', required=True)
    support_tel = fields.Char('Tel Support')
    connexion = fields.Char('Connexion')
    speed = fields.Char('Speed')
    connexion_type = fields.Char('Connexion Type')
