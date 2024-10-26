from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta

class TestPatientCommon(TransactionCase):

    def setUp(self):
        super(TestPatientCommon, self).setUp()
        self.patient = self.env['hr.hospital.patient'].create({
            'surname_name': 'Test Patient',
            'date_birth': datetime.today() - timedelta(days=365 * 30),  # Возраст 30 лет
        })


        self.doctor = self.env['hr.hospital.doctor'].create({
            'surname_name': 'Test Doctor',
        })

    def create_visit(self, planned_visit_date, visit_date=None):
        return self.env['hr.hospital.patient.visit'].create({
            'patient_id': self.patient.id,
            'doctor_id': self.doctor.id,
            'planned_visit_date': planned_visit_date,
            'visit_date': visit_date,
        })


