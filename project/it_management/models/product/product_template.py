# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    partner_id = fields.Many2one('res.partner', 'Partner')
    is_warning = fields.Boolean('Warning')
    warning_message = fields.Text('Warning Message')
