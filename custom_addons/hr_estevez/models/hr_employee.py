from odoo import api, models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    names = fields.Char(string='Nombres')

    direction_id = fields.Many2one('hr.direction', string='Dirección')
    area_id = fields.Many2one('hr.area', string='Area')

    work_phone = fields.Char(string='Work Phone', compute=False, store=False)
    coach_id = fields.Many2one('hr.employee', string='Instructor', compute=False, store=False)

    @api.model
    def create(self, vals):
        employee = super(HrEmployee, self).create(vals)
        if 'direction_id' in vals and vals['direction_id']:
            direction = self.env['hr.direction'].browse(vals['direction_id'])
            direction.director_id = employee.id
        return employee

    def write(self, vals):
        for record in self:
            if 'direction_id' in vals:
                # Si el empleado ya tiene una dirección, desasocia el director de la dirección anterior
                if record.direction_id:
                    old_direction = self.env['hr.direction'].browse(record.direction_id.id)
                    old_direction.director_id = False

                # Asocia el director a la nueva dirección
                if vals['direction_id']:
                    new_direction = self.env['hr.direction'].browse(vals['direction_id'])
                    new_direction.director_id = record.id

        res = super(HrEmployee, self).write(vals)
        return res