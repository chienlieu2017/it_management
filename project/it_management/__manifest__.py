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
        'mrp', 'document',
    ],
    'data': [
        # ============================================================
        # SECURITY SETTING - GROUP - PROFILE
        # ============================================================
        # 'security/',
        'security/res_groups_data.xml',
        # ============================================================
        # DATA
        # ============================================================
        # 'data/',
        'data/email_template_data.xml',
        'data/product_category_data.xml',
        'data/ir_cron_data.xml',
        'data/res_company_data.xml',
        'data/ir_config_parameter_data.xml',
        'data/ir_sequence_data.xml',
        'data/sms_template_data.xml',
        # WIZARD
        # ============================================================
        # 'wizard/',
        # REPORT
        # ============================================================
        # 'report/',
        # ============================================================
        # VIEWS
        # ============================================================
        # 'view/',
        'view/access/access_system_view.xml',
        'view/access/internet_provider_view.xml',
        'view/access/web_service_view.xml',
        'view/access/data_right_access_view.xml',
        'view/base/res_partner_view.xml',
        'view/issue/issue_config_settings_views.xml',
        'view/issue/issue_report_view.xml',
        'view/sms/sms_sms_view.xml',
        'view/sms/sms_template_view.xml',
        'view/network/network_map_view.xml',
        'view/contract/partner_contract_view.xml',
        # ============================================================
        # MENU
        # ============================================================
        # 'menu/',
        'menu/menu_view.xml',
        # ============================================================
        # FUNCTION USED TO UPDATE DATA LIKE POST OBJECT
        # ============================================================
        # "data/ubiz_spa_update_functions_data.xml",
    ],

    'test': [],
    'demo': [],

    'installable': True,
    'active': False,
    'application': True,
}
