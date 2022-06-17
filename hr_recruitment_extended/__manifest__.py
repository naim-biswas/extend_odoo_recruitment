# -*- coding: utf-8 -*-
{
    'name': "Recruitment Extended",

    'summary': """
        Multiple Emergency Contact, Educational Qualification and Leave Allocation""",

    'description': """
        Multiple Emergency Contact, Educational Qualification and Leave Allocation
    """,

    'author': "Naim Biswas",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '13.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_recruitment', 'hr_holidays'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hr_recruitment_view.xml',
        'views/hr_employee_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
