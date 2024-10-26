{
    'name': 'Hospital',
    'version': '17.0.1.0.0',
    'author': 'Sasha Lytvychenko',
    'website': 'https://odoo.school/',
    'category': 'Customizations',
    'license': 'OPL-1',
    'depends': [
        'base',
        'mail',
    ],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_hospital_security.xml',
        'views/hr_hospital_menu.xml',
        'wizard/hr_hospital_reappointment_doctor_wizard_views.xml',
        'wizard/hr_hospital_disease_report_wizard_views.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_visit_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_type_views.xml',
        'views/hr_hospital_diagnosis_views.xml',
        'data/hr_hospital_disease_type.xml',
        'views/hr_hospital_disease_category_views.xml',
        'report/hr_hospital_test_doctor_report.xml',

    ],
    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr.hospital.patient.csv',
        'demo/hr_hospital_disease_category_demo.xml',
        'demo/hr.hospital.patient.visit.csv',
        'demo/hr.hospital.diagnosis.csv',

    ],

    'installable': True,
    'auto_install': False,
    'images': [
        'static/description/icon.png'
    ]
}
