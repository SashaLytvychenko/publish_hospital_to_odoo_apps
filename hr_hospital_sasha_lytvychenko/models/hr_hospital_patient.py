from datetime import datetime

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = 'hr.hospital.person'
    _description = 'Patient'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Treating doctor',
    )

    date_birth = fields.Date(
        string='Date of birth')
    age = fields.Integer(
        compute='_compute_age',
        store=True
    )
    email = fields.Char(
    )
    passport_code = fields.Char(
    )
    contact_person_ids = fields.Many2many(
        comodel_name='res.partner')
    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id')

    @api.constrains('date_birth')
    def _check_date_birth(self):
        """Check that the birth date is not in the future.

                Raises:
                    ValidationError: If the birth date is greater than today's date.
                """
        for rec in self:
            if rec.date_birth and rec.date_birth > fields.Date.today():
                raise ValidationError(
                    f'You cannot enter birth date more than today date:'
                    f' {fields.Date.today()}')

    @api.depends('date_birth')
    def _compute_age(self):
        """Compute the age of the patient based on the date of birth.

                The age is calculated by comparing the current date to the
                patient's date of birth. If the date of birth is not provided,
                the age will be set to 0.

                This method is automatically triggered whenever the
                'date_birth' field is modified.
                """
        for rec in self:
            if rec.date_birth:
                today = datetime.today()
                birth_date = rec.date_birth
                age = today.year - birth_date.year
                if ((today.month, today.day) <
                        (birth_date.month, birth_date.day)):
                    age -= 1
                rec.age = age
            else:
                rec.age = 0
