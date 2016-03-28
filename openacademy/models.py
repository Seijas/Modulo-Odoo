# -*- coding: utf-8 -*-

from openerp import models, fields, api

class openacademy(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(String="Titulo", required=True)
    description = fields.Text()

    responsible_id = fields.Many2one('res.users',
    ondelete='set null', string="Responsable", index=True)

    session_ids = fields.One2many(
            'openacademy.session', 'course_id', string="Sesiones")

class Session(models.Model):
    _name = 'openacademy.session'
    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(default=True)

    instructor_id = fields.Many2one('res.partner', string="Instructor",
        domain=[('instructor', '=', True),
        ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('openacademy.course',
            ondelete='cascade', string="Curso", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats
