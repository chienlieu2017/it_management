# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import api, fields, models


class NetworkMap(models.Model):
    _name = "network.map"
    _description = "Network Map"

    name = fields.Char("Name", required=True)
    description = fields.Html('Description')
    user_id = fields.Many2one('res.users', 'User',
                              default=lambda self: self.env.uid)
    owner_ids = fields.Many2many(
        'res.users', string='Owner')
    partner_id = fields.Many2one('res.partner', 'Customer')
