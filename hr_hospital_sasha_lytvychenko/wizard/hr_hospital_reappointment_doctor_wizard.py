import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class OSLAddReader(models.TransientModel):
    _name = 'hr.hospital.reappointment.doctor.wizard'
    _description = 'Reappoint doctor'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',

        # readonly=True,
    )
    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
    )

    def reappointment_doctor(self):
        self.patient_id.doctor_id = self.doctor_ids
