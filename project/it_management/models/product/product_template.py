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
    contact_partner_id = fields.Many2one('res.partner', 'Employee')
    is_warning = fields.Boolean('Warning')
    warning_message = fields.Text('Warning Message')
    software_ids = fields.One2many('product.software', 'product_template_id',
                                   'Softwares')
    categ_type = fields.Selection([('hardware', 'Hardware'),
                                   ('software', 'Software')],
                                  string="Current Type",
                                  related="categ_id.categ_type")
