# -*- coding: utf-8 -*-
{
    'name': "Ahorasoft LATTI Subscription",

    'summary': """
        LATTI Module
===========================

Custom module for LATTI""",

    'description': """
LATTI Module
===========================

Custom module for LATTI
    """,

    'author': "Ahorasoft",
    'website': "http://www.ahorasoft.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.2',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/as_scheduler_email.xml',
        'data/data.xml',
    ],
}