from odoo import models, fields, api


class HospitalDiseaseCategory(models.Model):
    _name = 'hr.hospital.disease.category'
    _description = 'Diseases category'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'complete_name'
    _order = 'complete_name'

    name = fields.Char(index='trigram', required=True)
    complete_name = fields.Char(
        compute='_compute_complete_name', recursive=True,
        store=True)
    description = fields.Text(
    )
    parent_id = fields.Many2one('hr.hospital.disease.category',
                                'Parent Category',
                                index=True,
                                ondelete='cascade')
    parent_path = fields.Char(index=True, unaccent=False)

    # child_id = fields.One2many('hr.hospital.disease.category',
    # 'parent_id', 'Child Categories')


@api.depends('name', 'parent_id.complete_name')
def _compute_complete_name(self):
    for category in self:
        if category.parent_id:
            category.complete_name = '{} / {}'.format(
                category.parent_id.complete_name, category.name)
        else:
            category.complete_name = category.name
