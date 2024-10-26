from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease.type'
    _description = 'Types of diseases'

    name = fields.Char(string='Name of disease', required=True)
    description = fields.Text(string='Disease description')
    disease_category_id = fields.Many2one(
        comodel_name='hr.hospital.disease.category',

    )
