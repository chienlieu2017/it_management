# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class IrModuleCategory(models.Model):
    _inherit = "ir.module.category"

    ignore_in_user_form = fields.Boolean(
        string="Is Ignore In User Form?",
        default=False,
        copy=False)
