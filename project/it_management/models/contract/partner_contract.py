# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import api, fields, models


class PartnerContract(models.Model):
    _name = "partner.contract"
    _description = "Partner Contract"
    _inherit = ['mail.thread']
    _order = "id desc"

    partner_id = fields.Many2one(
        'res.partner', 'Customer', domain=[('customer', '=', True)],
        required=True, track_visibility='onchange')
    phone = fields.Char('Phone', related="partner_id.phone", readonly=True)
    mobile = fields.Char('Mobile', related="partner_id.mobile", readonly=True)
    email = fields.Char('Email', related="partner_id.email", readonly=True)
    name = fields.Char(
        'Contract Number', required=True, track_visibility='onchange')
    description = fields.Html('Description')
    user_id = fields.Many2one('res.users', 'User',
                              default=lambda self: self.env.uid)
    owner_ids = fields.Many2many(
        'res.users', string='Owner')
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To')
