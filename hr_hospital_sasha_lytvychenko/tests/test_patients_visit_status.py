from odoo.addons.hr_hospital.tests.common import TestPatientCommon
from odoo.tests import tagged
from datetime import datetime, timedelta

@tagged('post_install', '-at_install', 'visit_status')
class TestPatientVisitStatuses(TestPatientCommon):

    def test_visit_status_planned(self):
        future_date = datetime.now() + timedelta(days=5)
        visit = self.create_visit(planned_visit_date=future_date)
        visit._check_statuses()
        self.assertEqual(visit.visit_status, 'planned')

    def test_visit_status_cancelled(self):
        past_date = datetime.now() - timedelta(days=5)
        visit = self.create_visit(planned_visit_date=past_date)
        visit._check_statuses()
        self.assertEqual(visit.visit_status, 'cancelled')
    def test_visit_status_completed(self):
        today = datetime.now()
        visit = self.create_visit(planned_visit_date=today, visit_date=today)
        visit._check_statuses()
        self.assertEqual(visit.visit_status, 'completed')