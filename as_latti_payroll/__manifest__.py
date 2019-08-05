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
    'version': '1.2.6',
    'website': "http://www.ahorasoft.com",
    'category': 'Uncategorized',
    'depends': ['base','l10n_cl_hr'],
    'data': [
        # 'security/ir.model.access.csv',
        'data/data.xml',
        'views/as_hr_indicadores_previsionales_view.xml',
        'views/templates.xml',
        'views/as_hr_contract_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}