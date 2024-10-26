from odoo import models, fields


class HospitalPerson(models.AbstractModel):
    _name = 'hr.hospital.person'
    _inherit = 'mail.thread'
    _description = 'Person'
    _rec_name = 'surname_name'

    surname_name = fields.Char(required=True)
    phone = fields.Char(
    )
    image = fields.Image(
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ], default='male')
    user_id = fields.Many2one(
        comodel_name='res.users',
        string="Person related to this user:",
    )