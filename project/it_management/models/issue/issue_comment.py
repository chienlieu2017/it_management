# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo import fields, models


class IssueComment(models.Model):
    _name = "issue.comment"
    _description = "Issue Comment"

    create_date = fields.Datetime(
        string="Creation Date",
        default=fields.Datetime.now,
        readonly=True)
    reason = fields.Char(
        string="Reason")
    create_uid = fields.Many2one(
        string="User",
        comodel_name="res.users",
        default=lambda self: self.env.uid)
    time_spent = fields.Float(
        string="Time spent")
    solution = fields.Html(
        string="Solution")
    issue_id = fields.Many2one(
        string="Report Issue",
        comodel_name="issue.report")
    note = fields.Html(
        string="Note")