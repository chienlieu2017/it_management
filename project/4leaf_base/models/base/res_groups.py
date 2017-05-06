# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"


    def get_application_groups(self, domain):
        """ Return the non-share groups that satisfy ``domain``. """
        return self.search(domain + [('share', '=', False),
                                     ('category_id.ignore_in_user_form', '=',
                                      False)])
