# -*- coding: utf-8 -*-
{
    'name': "Ahorasoft LATTI Payroll",

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
    'version': '1.2.2',

    # any module necessary for this one to work correctly
    'depends': ['base','l10n_cl_hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/as_hr_indicadores_previsionales_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}