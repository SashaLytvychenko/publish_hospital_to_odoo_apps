from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = 'hr.hospital.person'
    _description = 'Doctor'

    email = fields.Char()
    specialization = fields.Selection([('pediatrics', 'Pediatrics'),
                                       ('pathology', 'Pathology'),
                                       ('psychiatry', 'Psychiatry')],
                                      default='pediatrics')
    is_intern = fields.Boolean(
    )
    doctor_mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        domain="[('id', '!=', id), ('is_intern', '=', False)]",
    )
    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='doctor_mentor_id',
        string="Interns"
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True,
        default=lambda self: self.env.company,
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.patient.visit',
        inverse_name='doctor_id',
        string="Patient Visits"
    )

    def open_visit_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Запис до лікаря',
            'res_model': 'hr.hospital.patient.visit',
            'view_mode': 'form',
            'context': {
                'default_doctor_id': self.id,
            },
            'target': 'new',
        }

    def view_profile(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Doctor Profile',
            'res_model': 'hr.hospital.doctor',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
