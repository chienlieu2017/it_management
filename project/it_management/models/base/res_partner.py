# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    supporter_id = fields.Many2one(
        string="Supporter",
        comodel_name="res.users")
    data_folder_ids = fields.One2many('data.folder', 'company_id', 'Folders')
    product_ids = fields.One2many('product.product', 'partner_id', 'Devices')
    department_id = fields.Many2one(
        string="Department",
        comodel_name="res.partner.department")
    send_monthly_report = fields.Boolean('Send monthly report?',
                                         default=True)
