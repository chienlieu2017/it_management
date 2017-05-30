# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

import base64
import cStringIO
import collections
from datetime import datetime
import logging

from openerp import models, fields, api
from xlrd import open_workbook
import xlrd
import xlwt
from odoo.modules.module import get_module_resource
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ImportProductWizard(models.Model):
    _name = 'import.product.wizard'

    data_file = fields.Binary(
        string="File to import (.xlsx OR .xls)",
        required=True)
    template_file = fields.Binary(
        string="Template file")
    error_file = fields.Binary(
        readonly=True)
    error_file_name = fields.Char(default='Errors.txt')
    template_file_name = fields.Char(default='Errors.txt')
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.partner")
    categ_type = fields.Selection([('hardware', 'Device'),
                                   ('software', 'Software')],
        default="hardware",
        string="Device / Software ?")

    def _is_number(self, number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True

    @api.model
    def default_get(self, fs):
        res = super(ImportProductWizard, self).default_get(fs)
        p = get_module_resource('it_management', 'data',
                                'Device - software Template.xlsx')
        file_content = open(p, 'rb').read()
        res.update({'template_file': base64.encodestring(file_content),
                    'template_file_name': 'Device - software Template.xlsx'})
        return res

    def clear_str(self, val):
        if self._is_number(val):
            val = str(val)
        elif isinstance(val, (str, unicode)):
            val = val.strip()
        return val

    @api.multi
    def action_import_product(self):
        self.output_file = u''

        logging.info('======= CHECK DATA AND IMPORT PRODUCT =======')

        xlsx_file = base64.b64decode(self.data_file)
        xlsx_file = open_workbook(file_contents=xlsx_file)

        header = 2

        sheet = xlsx_file.sheets()[0]
        cols = sheet.ncols
        lines = []
        attrs = []
        attrs_idx = 4
        refs = []
        user_names = []
        attr_names = []
        attr_values = []
        for row in range(sheet.nrows):

            row_value = sheet.row_values(row, start_colx=0, end_colx=cols)
            row_value = [bool(i) for i in row_value]

            if True not in row_value:
                continue
            if header:
                header -= 1
                if header == 0:
                    for _idx in range(attrs_idx, cols):
                        val = sheet.cell(row, _idx).value
                        if val not in attrs:
                            attrs.append(val)
                continue

            line = {
                'ref': self.clear_str(sheet.cell(row, 0).value),
                'name': self.clear_str(sheet.cell(row, 1).value),
                'user_name': self.clear_str(sheet.cell(row, 2).value),
                'note': self.clear_str(sheet.cell(row, 3).value),
                'attrs': {}
            }

            if line['ref'] and line['ref'] not in refs:
                refs.append(line['ref'])
            if line['user_name'] and line['user_name'] not in user_names:
                user_names.append(line['user_name'])

            attrs_data = {}
            for _idx in range(attrs_idx, cols):
                i = _idx - attrs_idx
                aname = self.clear_str(sheet.cell(row, _idx).value)
                line['attrs'].update({attrs[i]: aname})
                if aname and aname not in attr_values:
                    attr_values.append(aname)
            lines.append(line)
        # Caching refs
        cache_ref = {}
        if refs:
            refs += ['', '']
            sql = '''
            SELECT id, default_code
            FROM product_template
            WHERE default_code IN %s
            '''
            self._cr.execute(sql, (tuple(refs),))
            data = self._cr.fetchall()
            for r in data:
                cache_ref.update({r[1]: r[0]})
        # Caching user name
        cache_users = {}
        if user_names:
            user_names += ['', '']
            sql = '''
            SELECT id, name
            FROM res_partner
            WHERE parent_id = {}
                AND name IN %s
            '''.format(self.company_id.id or 'NULL')
            self._cr.execute(sql, (tuple(user_names), ))
            data = self._cr.fetchall()
            for r in data:
                cache_users.update({r[1]: r[0]})
        # Caching attributes
        cache_attrs = {}
        if attrs:
            attrs += ['', '']
            sql = '''
            SELECT id, name
            FROM product_attribute
            WHERE name IN %s
            '''
            self._cr.execute(sql, (tuple(attrs),))
            data = self._cr.fetchall()
            for r in data:
                cache_attrs.update({r[1]: r[0]})
        # Caching attribute value
        cache_attr_values = {}
        if attr_values:
            attr_values += ['', '']
            sql = '''
            SELECT id, name || '--' || attribute_id
            FROM product_attribute_value
            WHERE name IN %s
            '''
            self._cr.execute(sql, (tuple(attr_values), ))
            data = self._cr.fetchall()
            for r in data:
                cache_attr_values.update({r[1]: r[0]})          

        categ = self.env['product.category'].search([('categ_type', '=',
                                                      self.categ_type)],
                                                    limit=1)
        if not categ:
            raise UserError(_('''Cannot find the category with type {}'''
                              .format(self.categ_type)))

        PTemplate = self.env['product.template']
        # Create / Update product
        for line in lines:
            vals = {'name': line['name'],
                    'description': line['note'],
                    'categ_id': categ.id,
                    'partner_id': self.company_id.id}
            if line['user_name']:
                if line['user_name'] in cache_users:
                    vals.update({'contact_partner_id':
                                 cache_users[line['user_name']]})
                else:
                    # Create new one
                    u_vals = {'name': line['user_name'],
                              'parent_id': self.company_id.id
                              }
                    n_user = self.env['res.partner'].create(u_vals)
                    vals.update({'contact_partner_id': n_user.id})
                    # Update caches
                    cache_users.update({line['user_name']: n_user.id})
            if line['ref'] and line['ref'] in cache_ref:
                # Update product
                # Don't update attribute, it can cause losing data of variant
                template = PTemplate.browse(cache_ref[line['ref']])
                template.write(vals)
            else:
                if line['ref']:
                    vals.update({'default_code': line['ref']})
                # Create new template
                if line['attrs']:
                    l_attrs = []
                    for att_name, att_val in line['attrs'].iteritems():
                        if not att_val or not att_name:
                            continue
                        # Check attibute
                        att_id = None
                        if att_name in cache_attrs:
                            att_id = cache_attrs[att_name]
                        else:
                            # Create new
                            n_att = self.env['product.attribute'
                                             ].create({'name': att_name})
                            att_id = n_att.id
                            # Update cache
                            cache_attrs.update({att_name: att_id})
                        # Check attribute value
                        att_val_id = None
                        k = '--'.join([att_val, str(att_id)])
                        if k in cache_attr_values:
                            att_val_id = cache_attr_values[k]
                        else:
                            av_vals = {'attribute_id': att_id,
                                       'name': att_val}
                            n_attv = self.env['product.attribute.value'
                                              ].create(av_vals)
                            att_val_id = n_attv.id
                            # Update cache
                            cache_attr_values.update({k: att_val_id})
                        l_attr = [0, 0, {'attribute_id': att_id,
                                         'value_ids': [[6, 0, [att_val_id]]]}]
                        l_attrs.append(l_attr)
                    vals.update({'attribute_line_ids': l_attrs})
                template = PTemplate.create(vals)
