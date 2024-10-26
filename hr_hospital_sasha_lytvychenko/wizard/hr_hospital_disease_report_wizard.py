import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors'
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease.type',
        string='Diseases'
    )
    date_from = fields.Date(
        string='From',
        required=True
    )
    date_to = fields.Date(
        string='To',
        required=True
    )

    def get_report(self):

        domain = [('visit_id.visit_date', '>=', self.date_from),
                  ('visit_id.visit_date', '<=', self.date_to)]

        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))

        if self.disease_ids:
            domain.append(('disease_ids', 'in', self.disease_ids.ids))

        diagnoses = self.env['hr.hospital.diagnosis'].search(domain)

        _logger.info(f"Diagnoses found: {diagnoses}")

        return {
            'name': 'Disease Report',
            'view_mode': 'tree,form',
            'res_model': 'hr.hospital.diagnosis',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', diagnoses.ids)],
        }
