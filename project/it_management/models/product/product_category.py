# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    categ_type = fields.Selection([('hardware', 'Hardware'),
                                   ('software', 'Software')],
                                  string="Current Type",
                                  default=lambda *x: 'software')
