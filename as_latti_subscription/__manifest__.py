# -*- coding: utf-8 -*-
{
    'name': "Ahorasoft LATTI Subscription",
    'version': '1.2.2',

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
    'category': 'Uncategorized',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts','sale_subscription'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/as_scheduler_email.xml',
        'views/as_mail_activity.xml',
        'data/data.xml',
    ],
}