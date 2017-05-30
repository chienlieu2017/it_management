# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2016 Trobz (<http://trobz.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not see <http://www.gnu.org/licenses/>.
#
##############################################################################

import base64
import cStringIO
import collections
from datetime import datetime
import logging

from openerp import models, fields, api, _
from xlrd import open_workbook
import xlrd
import xlwt
from odoo.modules.module import get_module_resource
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF


class ImportSoftwareInfoWizard(models.Model):
    _name = 'import.software.info.wizard'

    data_file = fields.Binary(
        string="File to import (.xlsx OR .xls)",
        required=True)
    template_file = fields.Binary(
        string="Template file")
    error_file = fields.Binary(
        readonly=True)
    error_file_name = fields.Char(default='Errors.txt')
    template_file_name = fields.Char(default='Errors.txt')

    @api.model
    def default_get(self, fs):
        res = super(ImportSoftwareInfoWizard, self).default_get(fs)
        p = get_module_resource('it_management', 'data',
                                'Software Info Template.xlsx')
        file_content = open(p, 'rb').read()
        res.update({'template_file': base64.encodestring(file_content),
                    'template_file_name': 'Device - software Template.xlsx'})
        return res

    def _is_number(self, number):
        try:
            int(number)
        except ValueError:
            return False
        else:
            return True

    def clear_str(self, val):
        if self._is_number(val):
            val = str(val)
        elif isinstance(val, (str, unicode)):
            val = val.strip()
        return val

    def convert_to_date(self, excel_date):
        py_date = False
        try:
            py_date = xlrd.xldate.xldate_as_datetime(
                excel_date, self.date_mode)
        except:
            pass

        return py_date and py_date.date()

    @api.multi
    def action_import(self):
        self.output_file = u''

        logging.info('======= CHECK DATA AND IMPORT Software info =======')

        xlsx_file = base64.b64decode(self.data_file)
        xlsx_file = open_workbook(file_contents=xlsx_file)
        self.date_mode = xlsx_file.datemode

        header = 1

        sheet = xlsx_file.sheets()[0]
        cols = sheet.ncols
        lines = []
        device_refs = software_refs = []
        error_product = ''
        refs = {}
        for row in range(sheet.nrows):

            row_value = sheet.row_values(row, start_colx=0, end_colx=cols)
            row_value = [bool(i) for i in row_value]

            if True not in row_value:
                continue
            if header:
                header -= 1
                continue

            line = {
                'd_ref': self.clear_str(sheet.cell(row, 0).value),
                'd_name': self.clear_str(sheet.cell(row, 1).value),
                's_ref': self.clear_str(sheet.cell(row, 2).value),
                's_name': self.clear_str(sheet.cell(row, 3).value),
                'license': self.clear_str(sheet.cell(row, 4).value),
                'expiration': self.clear_str(sheet.cell(row, 5).value),
                'note': self.clear_str(sheet.cell(row, 6).value),
            }
            if line['expiration']:
                try:
                    expri = self.convert_to_date(line['expiration'])
                    line['expiration'] = fields.Date.to_string(expri)
                except:
                    error_product += '''Expiration date is invalid at the line {}\n
                    '''.format(row + 1)
            else:
                del line['expiration']
            lines.append(line)
            if not line['d_ref']:
                error_product += '''Device Reference is empty at the line {}\n
                '''.format(row + 1)
            if not line['s_ref']:
                error_product += '''Software Reference is empty at the line {}
                \n'''.format(row + 1)
            if line['d_ref'] not in refs or line['s_ref'] not in refs:
                dcode = ['', '']
                if line['d_ref'] not in refs:
                    dcode.append(line['d_ref'])
                if line['s_ref'] not in refs:
                    dcode.append(line['s_ref'])
                sql = '''
                    SELECT id, default_code
                    FROM product_product
                    WHERE default_code in %s
                    LIMIT 2
                    '''
                self._cr.execute(sql, (tuple(dcode),))
                data = self._cr.fetchall()
                for l in data:
                    if l[1] not in refs:
                        refs[l[1]] = l[0]
                if line['d_ref'] not in refs:
                    error_product += '{0} {1}\n'.format(
                        _('Cannot find device reference in row:'),
                        row + 1)
                if line['s_ref'] not in refs:
                    error_product += '{0} {1}\n'.format(
                        _('Cannot find software reference in row:'),
                        row + 1)
        if error_product:
            # self.env.cr.rollback()
            self.error_file = base64.encodestring(error_product)

            view_id = self.env.ref('it_management.'
                                   'import_software_info_wizard')
            return {
                'type': 'ir.actions.act_window',
                'name': _('Import Software Info'),
                'res_model': 'import.software.info.wizard',
                'res_id': self.id,
                'view_id': view_id.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new'
            }
        else:
            # Update software info for device
            Psoftware = self.env['product.software']
            for line in lines:
                vals = {'product_template_id': refs[line['d_ref']],
                        'product_id': refs[line['s_ref']],
                        'lisence_key': line['license'],
                        'expiration_date': line.get('expiration'),
                        'notes': line['note']
                        }
                args = [('product_template_id', '=', refs[line['d_ref']]),
                        ('product_id', '=', refs[line['s_ref']])]
                exist = Psoftware.search(args, limit=1)
                if exist:
                    del vals['product_template_id']
                    del vals['product_id']
                    exist.write(vals)
                else:
                    Psoftware.create(vals)
