# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017 4Leaf Team
#
##############################################################################
{
    'name': 'IT Management Module',
    'version': '1.0',
    'category': 'IT',
    'description': """
IT Management Module
    """,
    'author': '4Leaf Team',
    'website': '',
    'depends': [
        'mrp',
        'document',
        'report_xlsx',
        '4leaf_base',
        'base',
        'web',
        'im_livechat',
        'mail',
    ],
    'data': [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        'view/base/web_template.xml',
        'view/base/qweb.xml',
        # ============================================================
        # 'security/',
        'security/res_groups_data.xml',
        'security/ir.model.access.csv',
        'security/ir_rule_data.xml',
        # ============================================================
        # DATA
        # ============================================================
        # 'data/',
        
        'data/product_category_data.xml',
        'data/ir_cron_data.xml',
        'data/res_company_data.xml',
        'data/ir_config_parameter_data.xml',
        'data/ir_sequence_data.xml',
        'data/sms_template_data.xml',

        # WIZARD
        # ============================================================
        'wizards/import_product_wizard_view.xml',

        # REPORT
        # ============================================================
        # 'report/',
        'report/report_paper_format.xml',
        'report/monthly_data_access_right_report.xml',
        'report/monthly_device_report.xml',
        'report/monthly_issue_report_xlsx.xml',
        # ============================================================
        # VIEWS
        # ============================================================
        # 'view/',
        'view/access/access_system_view.xml',
        'view/access/internet_provider_view.xml',
        'view/access/web_service_view.xml',
        'view/access/data_right_access_view.xml',
        'view/access/data_folder_view.xml',
        'view/base/res_partner_view.xml',
        'view/base/month_report_view.xml',
        'view/issue/issue_config_settings_views.xml',
        'view/issue/issue_report_view.xml',
        'view/sms/sms_sms_view.xml',
        'view/sms/sms_template_view.xml',
        'view/network/network_map_view.xml',
        'view/contract/partner_contract_view.xml',
        'view/product/product_template_view.xml',
        'view/product/product_category_view.xml',
        
        # ============================================================
        # MENU
        # ============================================================
        # 'menu/',
        'menu/menu_view.xml',
        'data/email_template_data.xml',
        # ============================================================
        # FUNCTION USED TO UPDATE DATA LIKE POST OBJECT
        # ============================================================
        # "data/ubiz_spa_update_functions_data.xml",
    ],

    'test': [],
    'demo': [],
    'qweb': [
        'static/src/xml/web_dialog_size.xml',
        'view/base/base_view.xml',
    ],
    'installable': True,
    'active': False,
    'application': True,
}
