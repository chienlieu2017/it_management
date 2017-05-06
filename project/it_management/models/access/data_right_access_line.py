# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class DataRightAccessLine(models.Model):
    _name = "data.right.access.line"
    _description = "Data Right Access Line"
    _order = 'data_access_id'

    data_access_id = fields.Many2one('data.right.access', 'Data Access',
                                     ondelete='cascade')
    folder_id = fields.Many2one('data.folder', 'Folder')
    p_read = fields.Boolean('Read')
    p_write = fields.Boolean('Write')
    p_create = fields.Boolean('Create')
    p_delete = fields.Boolean('Delete')
    notes = fields.Char('Notes')
