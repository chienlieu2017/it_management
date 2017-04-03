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
        'data/product_category_data.xml',
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
        'view/issue/issue_config_settings_views.xml',
        'view/issue/issue_report_view.xml',
        'view/sms/sms_sms_view.xml',
        'view/sms/sms_template_view.xml',
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
