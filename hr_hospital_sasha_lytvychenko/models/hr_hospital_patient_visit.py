import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class HospitalPatientVisit(models.Model):
    _name = 'hr.hospital.patient.visit'
    _description = 'Patient visits'
    _rec_name = 'ref'

    ref = fields.Char(
        string='Reference',
        default=lambda self: _('New'))
    visit_status = fields.Selection(selection=[
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')],
        default='planned'
    )
    planned_visit_date = fields.Datetime(
        required=True)
    visit_date = fields.Datetime(
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string="Patient",
        required=True)
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Treating doctor',
        required=True)
    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id'
    )
    active = fields.Boolean(
        default=True,

    )
    prescription = fields.Text(
    )

    def unlink(self):
        """Override unlink method to prevent deletion of visits with associated diagnoses.

                Raises:
                    ValidationError: If the visit has associated diagnoses.
                """
        if self.diagnosis_ids:
            raise ValidationError(_('You cannot delete visit with diagnosis'))
        res = super().unlink()
        return res

    def write(self, vals):
        if 'active' in vals and not vals['active']:
            for record in self:
                if record.diagnosis_ids:
                    raise (_(ValidationError
                             ('You cannot archive a visit with diagnosis')))
        return super().write(vals)

    @api.onchange('planned_visit_date', 'visit_date')
    def _check_statuses(self):
        """Update visit status based on planned visit date and actual visit date.

                Sets visit status to 'cancelled' if the planned date is in the past,
                and to 'completed' if the actual visit date matches the planned date.
                """
        for rec in self:
            if rec.planned_visit_date:
                if (fields.Date.today() >
                        fields.Date.from_string(rec.planned_visit_date)):
                    rec.visit_status = 'cancelled'
                elif rec.visit_date == rec.planned_visit_date:
                    rec.visit_status = 'completed'

    @api.constrains('doctor_id', 'visit_date')
    def _check_doctor_and_visit_date(self):
        """Check constraints for doctor and visit date upon completion.

               Raises:
                   ValidationError: If the visit is marked completed and there are
                   changes to the visit date or doctor.
               """
        for rec in self:
            if rec.visit_status == 'completed':
                if rec.visit_date and rec.visit_date != rec.planned_visit_date:
                    raise (_(ValidationError(
                        'You cannot change the visit date once '
                        'it is completed.')))
                if rec.doctor_id:
                    raise ValidationError(
                        _('You cannot change the doctor once '
                          'the visit is completed.'))

    @api.model
    def create(self, vals):
        planned_visit_date = (fields.Datetime.from_string
                              (vals.get('planned_visit_date')))
        existing_visits = self.search([
            ('patient_id', '=', vals.get('patient_id')),
            ('doctor_id', '=', vals.get('doctor_id')),
            ('planned_visit_date', '>=',
             planned_visit_date.replace(hour=0, minute=0, second=0)),
            ('planned_visit_date', '<=',
             planned_visit_date.replace(hour=23, minute=59, second=59)),
        ])
        if existing_visits:
            raise ValidationError(
                f"This patient is already booked with this "
                f"doctor for the selected date"
                f" - {planned_visit_date}.")
        return super().create(vals)

    @api.onchange('diagnosis_ids')
    def _onchange_diagnosis_ids(self):
        """Trigger a warning if any diagnosis in the visit is approved.

                Returns:
                    dict: Warning message if any diagnosis is approved.
                """
        for rec in self:
            if rec.diagnosis_ids:
                for diagnosis in rec.diagnosis_ids:
                    if diagnosis.is_approved:
                        return {
                            'warning': {
                                'title': 'Warning',
                                'message': (
                                    'Remember only doctor can approve '
                                    'diagnosis'
                                )
                            }
                        }
        return {}
