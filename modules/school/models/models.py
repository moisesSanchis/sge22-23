# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
    _name = 'school.student'
    _description = 'The students'

    name = fields.Char(string="Nombre", required=True)
    year = fields.Integer()
    topic_id = fields.Many2many("school.topic")
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

class topic(models.Model):
    _name = 'school.topic'
    _description = 'The topics'
    name = fields.Char(string="Topic name", required=True)
    student_ids = fields.Many2many("school.student")
    
class course(models.Model):
    _name = 'school.course'
    _description = 'Courses'
    name = fields.Char()
    topics = fields.Many2many("school.topic")
    students = fields.Many2many("school.student")
    repeaters = fields.Many2many(comodel_name='school.student', # El modelo en el que es relaciona
                            relation='course_students_repeaters_rel', # (opcional) el nombre del la tabla en medio
                            column1='couse_id', # (opcional) el nombre en la tabla en medio de la columna de este modelo
                            column2='student_id')  # (opcional) el nombre de la columna de el otro modelo.