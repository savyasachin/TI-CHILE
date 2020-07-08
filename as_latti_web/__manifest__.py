# -*- coding: utf-8 -*-
{
    'name': "Ahorasoft Latti Web",
    'category': 'Web',
    'version': '1.0.4',
    'author': "Ahorasoft",
    'website': 'http://www.ahorasoft.com',
    "support": "soporte@ahorasoft.com",
    'summary': """
        Ahorasoft Latti Web""",
    'description': """
        Ahorasoft Latti Web
    """,
    "images": [],
    "depends": [
        "base","web","sale_subscription","helpdesk","sale"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/as_helpdesk_view.xml',
        'views/as_partner_view.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    
}