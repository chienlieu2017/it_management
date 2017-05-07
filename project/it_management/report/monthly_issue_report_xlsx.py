# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################

from odoo.addons.report_xlsx.report.report_xlsx import ReportXlsx
from collections import OrderedDict
from datetime import datetime, timedelta
import pytz, re
from odoo import fields
from ..models.issue.issue_report import RP_ISSUE_STATES


class MonthlyIssueReportXlsx(ReportXlsx):

    def generate_xlsx_report(self, workbook, data, o):
        if not o:
            return False
        date_data = o.get_date_data()

        sheet = workbook.add_worksheet(u'MONTHLY ISSUE REPORT')

        format_font = workbook.add_format()
        format_font.set_font_name('Times New Roman')
        format_font.set_font_size(10)
        header_format = workbook.add_format({'border': 1, 'align': 'center',
                                             'valign': 'vcenter'})
        header_brown = workbook.add_format({'border': 1,
                                            'align': 'center',
                                            'valign': 'vcenter',
                                            'bg_color': '#d4cbc6'})
        header_light_brown = workbook.add_format({'border': 1,
                                                  'align': 'center',
                                                  'valign': 'vcenter',
                                                  'bg_color': '#bdbdbd'})
        r_idx = 1
        col_nb = 5
        sheet.set_column(0, 11, 20)
        sheet.set_row(r_idx, 45)
        sheet.set_row(r_idx + 2, 20)
        sheet.set_row(r_idx + 3, 20)
        sheet.set_row(r_idx + 4, 20)
        sheet.merge_range(r_idx, 0, r_idx, 3, u'''
        MAINTENANCE SCHEDULE
        BÁO CÁO BẢO TRÌ
        ''', header_format)
        sheet.merge_range(r_idx, 4, r_idx, 11, u'''
        MONTHLY REPORT {}
        BÁO CÁO THÁNG {}
        '''.format(date_data.get('period_str'), date_data.get('period')),
        workbook.add_format({'bold': True, 'border': 1, 'align': 'center',
                             'valign': 'vcenter', 'bg_color': '#bdbdbd'
        }))
        r_idx += 2
        sheet.merge_range(r_idx, 0, r_idx + 2, 0, u'''
        WORKING STATION
        BỘ PHẬN
        ''', header_brown)
        sheet.merge_range(r_idx, 1, r_idx + 2, 1, u'''
        CURRENT #
        SỐ MÁY
        ''', header_brown)
        sheet.merge_range(r_idx, 2, r_idx + 2, 2, u'''
        USER
        NGƯỜI DÙNG
        ''', header_brown)
        sheet.merge_range(r_idx, 3, r_idx + 2, 3, u'''
        ASSIGNEE
        NV BẢO TRÌ
        ''', header_brown)        
        sheet.merge_range(r_idx, 4, r_idx, 11, 
                          u'Tháng {}'.format(date_data.get('period')),
                          workbook.add_format({'border': 1, 'align': 'center',
                                               'valign': 'vcenter',
                                               'bold': True}))
        r_idx += 1
        sheet.merge_range(r_idx, 4, r_idx + 1, 4, u'DATE',
                          header_brown)
        sheet.merge_range(r_idx, 5, r_idx, 6, u'REASON',
                          header_light_brown)
        sheet.merge_range(r_idx, 7, r_idx, 8, u'SOLUTION',
                          header_light_brown)
        sheet.merge_range(r_idx, 9, r_idx + 1, 9, u'TIME SPEND (HOUR)',
                          header_brown)
        sheet.merge_range(r_idx, 10, r_idx + 1, 10, u'STATUS',
                          header_brown)
        sheet.merge_range(r_idx, 11, r_idx + 1, 11, u'NOTE',
                          header_brown)
        r_idx += 1
        sheet.write(r_idx, 5, u'SOFTWARE', header_brown)
        sheet.write(r_idx, 6, u'HARDWARE', header_brown)
        sheet.write(r_idx, 7, u'SOFTWARE', header_brown)
        sheet.write(r_idx, 8, u'HARDWARE', header_brown)
        issues = self.get_datas(date_data)
        state_dict = dict(RP_ISSUE_STATES)
        format_idx = [0, 1, 2, 3, 5, 6, 7, 10]
        format_date = [4]
        format_state = [10]
        format_strip_tag = [5, 6, 7, 8, 11]
        for issue in issues:
            r_idx += 1
            i = 0
            for l in issue:
                val = l
                if val:
                    if i in format_idx:
                        val = u'' + val
                    if i in format_date:
                        val = fields.Datetime.from_string(val)
                        val = val.strftime('%d/%m/%Y')
                    if i in format_state:
                        val = state_dict.get(val, val)
                    if i in format_strip_tag:
                        val = re.sub('<[^<]+?>', '', val).strip()
                sheet.write(r_idx, i, val)
                i += 1

    def get_datas(self, data):
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        sql = '''
        SELECT rpd.name,
            CASE WHEN pp.default_code ISNULL
                THEN pt.name 
                ELSE '['||pp.default_code||'] '||pt.name
            END AS prod_name,
            rp.name,
            rp2.name,
            ic.create_date,
            CASE WHEN pc.categ_type = 'software'
                THEN ic.reason
                ELSE NULL
            END AS task_software,
            CASE WHEN pc.categ_type = 'hardware'
                THEN ic.reason
                ELSE NULL
            END AS task_hardware,
            CASE WHEN pc.categ_type = 'software'
                THEN ic.solution
                ELSE NULL
            END AS solution_software,
            CASE WHEN pc.categ_type = 'hardware'
                THEN ic.solution
                ELSE NULL
            END AS solution_hardware,
            COALESCE(ic.time_spent, 0.0) as time_spent,
            ir.state,
            ic.note
        FROM issue_report ir
        LEFT JOIN res_partner_department rpd
            ON ir.department_id = rpd.id
        LEFT JOIN product_product pp
            ON ir.product_id = pp.id
        LEFT JOIN product_template pt
            ON pt.id = pp.product_tmpl_id
        LEFT JOIN product_category pc
            ON pc.id = pt.categ_id
        LEFT JOIN res_partner rp
            ON ir.partner_id = rp.id
        LEFT JOIN issue_comment ic
            ON ir.id = ic.issue_id
        LEFT JOIN res_users ru
            ON ic.create_uid = ru.id OR ir.assignee_id = ru.id
        LEFT JOIN res_partner rp2
            ON rp2.id = ru.partner_id
        WHERE state != 'cancel'
            AND ir.create_date BETWEEN '{0}' AND '{1}'
        '''.format(from_date, to_date)
        self.env.cr.execute(sql)
        res = self.env.cr.fetchall()
        return res

MonthlyIssueReportXlsx('report.monthly_issue_report_xlsx',
                         'monthly.report.issue')
