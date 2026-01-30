{
    "name": "Court HR Employee",
    "version": "17.0.1.0.0",
    "summary": "EGP Human Resource Module",
    'sequence': -250,
    'category': 'Human Resources',
    "description": "",
    'depends': ['hr', 'mail', 'hr_recruitment', 'court_hr_org_structure', 'hr_skills', 'gamification', 'maintenance'],
    'data': [
        'security/court_hr_employee_security.xml',
        'security/ir.model.access.csv',
        'views/court_hr_employee.xml',
        'data/court_hr_employee_default_data.xml',
        'data/cron.xml',

        'report/court_hr_employee_report.xml',
        'report/court_hr_report_paper_format.xml',

        # view files
        'views/court_hr_print_action.xml',
        'views/court_hr_resume.xml',
        'views/employee_search.xml',
        'views/court_hr_retirement_views.xml',
        'views/court_hr_fire_views.xml',
        'views/court_hr_reward_views.xml',
        'views/court_hr_punishment_views.xml',
    ],
    "assets": {
        'web.assets_backend': [
            # 'court_hr/static/src/css/attachment_preview.css',
            # 'court_hr/static/src/js/qcent_many2many_attachment_preview.js',
            # 'court_hr/static/src/xml/qcent_many2many_attachment_preview_template.xml',
        ],
    },
    "author": "Nasratullah Shafiq",
    "website": "https://mcit.gov.af/",
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": 'OPL-1',
}
