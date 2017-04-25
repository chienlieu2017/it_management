# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import api, fields, models


class DataFolder(models.Model):
    _name = "data.folder"
    _description = "Data Folder"
    _order = 'name'
    _rec_name = 'display_name'

    @api.multi
    @api.depends('parent_id', 'parent_id.name', 'name')
    def _compute_display_name(self):
        def get_names(folder):
            """ Return the list [data.name, data.parent_id.name, ...] """
            res = []
            while folder:
                res.append(folder.name)
                folder = folder.parent_id
            return res
        for record in self:
            record.display_name = " / ".join(reversed(get_names(record)))

    name = fields.Char('Name', required=True)
    company_id = fields.Many2one('res.partner', 'Company', required=True,
                                 domain=[('company_type', '=', 'company')])
    display_name = fields.Char(
        string='Display Name',
        readonly=True, store=True, translate=True,
        compute='_compute_display_name'
    )
    parent_id = fields.Many2one('data.folder', 'Parent')
