# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class DataRightAccess(models.Model):
    _name = "data.right.access"
    _description = "Data Right Access"
    _order = 'name'

    name = fields.Char('Name', required=True)
    company_id = fields.Many2one(
        'res.partner', string='Company', reuqired=True,
        domain=[('company_type', '=', 'company')])
    partner_id = fields.Many2one(
        'res.partner', 'Employee Name', required=True)
    line_ids = fields.One2many(
        'data.right.access.line', 'data_access_id', 'Lines')
