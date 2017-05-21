
# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################


from odoo import fields, models


class ProductCategory(models.Model):
    _name = "product.software"
    _description = "Software Information"

    product_template_id = fields.Many2one(
        'product.template', 'Product Template')
    product_id = fields.Many2one(
        'product.product', 'Software')
    lisence_key = fields.Char('Lisence Key')
    expiration_date = fields.Date('Expiration Date')
    notes = fields.Char('Notes')
