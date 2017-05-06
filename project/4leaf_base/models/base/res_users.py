# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from itertools import repeat
from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    profile_id = fields.Many2one(
        string="Profile Group",
        comodel_name="res.groups")

    @api.model
    def create(self, values):
        values = self._update_profile_group(values)
        user = super(ResUsers, self).create(values)
        return user

    @api.multi
    def write(self, values):
        values = self._update_profile_group(values)
        res = super(ResUsers, self).write(values)
        return res

    @api.multi
    def _update_profile_group(self, values):
        if 'profile_id' not in values:
            return values
        add, rem = [values['profile_id']], []
        for r in self:
            if r.profile_id:
                rem.append(r.profile_id.id)

        if add == rem:
            return values

        gs = list(values.get('groups_id', []))

        values['groups_id'] = gs + zip(repeat(3), rem) + zip(repeat(4), add)

        return values