# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class ResPartnerDepartment(models.Model):
    _name = "res.partner.department"
    _description = "Department of Customer"

    name = fields.Char(
        string="Name")
