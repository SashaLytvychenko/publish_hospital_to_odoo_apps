from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Diagnosis'

    name = fields.Char(
        required=True,
    )
    visit_id = fields.Many2one(
        comodel_name='hr.hospital.patient.visit',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease.type',
    )
    description = fields.Text(
    )
    is_approved = fields.Boolean(
    )
