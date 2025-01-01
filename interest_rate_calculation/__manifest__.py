# -*- coding: utf-8 -*-

{
    'name': 'Interest Rate Calculation',
    'version': '1.1',
    'category': 'Account/Account',
    'summary': 'Account Management',
    'author': 'Pann Phyu',
    'description': """
    This module contains the interest rate calculation for invoices.
    """,
    'depends':  ['base', 'account','product','sale','purchase'],
    'data': [
        'view/res_config_settings_view.xml',
        'view/account_move_view.xml',
        'data/interest_product_data.xml',
    ],

    'installable': True,
    'auto_install': False
}
