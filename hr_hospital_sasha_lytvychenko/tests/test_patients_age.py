# test_patient_methods.py
from odoo.addons.hr_hospital.tests.common import TestPatientCommon
from odoo.tests import tagged
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

@tagged('post_install', '-at_install', 'patient')
class TestPatientMethods(TestPatientCommon):

    def test_01_check_date_birth(self):
        with self.assertRaises(ValidationError):
            self.patient.date_birth= datetime.today() + timedelta(days=1)
            self.patient._check_date_birth()

    def test_02_compute_age(self):
        self.patient.date_birth = datetime.today() - relativedelta(years=30)
        self.patient._compute_age()
        self.assertEqual(self.patient.age, 30)



        self.patient.date_birth = datetime.today() - relativedelta(years=25)
        self.patient._compute_age()
        self.assertEqual(self.patient.age, 25)