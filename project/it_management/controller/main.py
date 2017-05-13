# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

import jinja2
import logging
import os
import json
import sys

try:
    import xlwt
except ImportError:
    xlwt = None

import openerp
from openerp import http

_logger = logging.getLogger(__name__)

if hasattr(sys, 'frozen'):
    # When running on compiled windows binary,
    # we don't have access to package loader.
    path = os.path.realpath(os.path.join(
        os.path.dirname(__file__), '..', 'view'))
    loader = jinja2.FileSystemLoader(path)
else:
    loader = jinja2.PackageLoader('openerp.addons.it_management', "view")

env = jinja2.Environment(loader=loader, autoescape=True)
env.filters["json"] = json.dumps


class DatabaseSelector(openerp.addons.web.controllers.main.Database):

    def _render_template(self, **d):
        """
        TO DO: Change database manager html
            Change Logo select database
            Change Title
        """
        d.setdefault('manage', True)
        d['insecure'] = openerp.tools.config['admin_passwd'] == 'admin'
        d['list_db'] = openerp.tools.config['list_db']
        d['langs'] = openerp.service.db.exp_list_lang()
        # databases list
        d['databases'] = []
        try:
            d['databases'] = http.db_list()
        except openerp.exceptions.AccessDenied:
            monodb = super(DatabaseSelector, self).db_monodb()
            if monodb:
                d['databases'] = [monodb]
        return env.get_template("database_manager.html").render(d)
