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

    department_id = fields.Many2one(
        string="Department",
        comodel_name="res.partner.department")
