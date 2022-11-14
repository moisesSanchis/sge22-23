# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError



class player(models.Model):
    _name = 'dungeons.player'
    _description = 'players'

    name = fields.Char()
    avatar = fields.Image(max_width=200,
                          max_height=200)  # Atributo avatar que es una imagen y tiene un tamaño predeterminado.
    login = fields.Char()
    password = fields.Char()
    heart_player = fields.One2many(comodel_name='dungeons.heart',
                                   inverse_name='player')  # Relacion entre jugadores y mazmorras


class heart(models.Model):
    _name = 'dungeons.heart'
    _description = 'Hearts'

    name = fields.Char()
    avatar_heart = fields.Image(max_width=200, max_height=200)
    player = fields.Many2one('dungeons.player', ondelete='cascade')
    life = fields.Integer(default=2000)
    iron = fields.Integer(default=100)
    coal = fields.Integer(default=50)
    steel = fields.Integer(default=10)
    defense_creature = fields.Integer(default=0)
    magical_creature = fields.Integer(default=0)
    warrior_creature = fields.Integer(default=0)
    buildings = fields.One2many('dungeons.buildings', 'heart')

    @api.constrains('iron')
    def _check_something(self):
        for record in self:
            if record.iron > 3000:
                raise ValidationError("You have too much iron %s" % record.iron)

    @api.constrains('coal')
    def _check_something(self):
        for record in self:
            if record.coal > 3000:
                raise ValidationError("You have too much coal %s" % record.coal)

    @api.constrains('steel')
    def _check_something(self):
        for record in self:
            if record.steel > 3000:
                raise ValidationError("You have too much steel %s" % record.steel)


class buildings(models.Model):
    _name = 'dungeons.buildings'
    _description = 'Buildings'

    name = fields.Char()
    level = fields.Integer()
    heart = fields.Many2one('dungeons.heart', ondelete='restrict')
    building_type = fields.Many2one('dungeons.building_type', ondelete='restrict')
    image_building = fields.Image(max_width=200, max_height=200, related='building_type.image_building')
    production_iron = fields.Float(related='building_type.production_iron')
    production_coal = fields.Float(related='building_type.production_coal')
    production_steel = fields.Float(related='building_type.production_steel')
    consume_iron = fields.Float(related='building_type.consume_iron')
    consume_coal = fields.Float(related='building_type.consume_coal')
    production_magical_creatures = fields.Float(related='building_type.production_magical_creatures')
    production_warrior_creatures = fields.Float(related='building_type.production_warrior_creatures')
    production_defense_creatures = fields.Float(related='building_type.production_defense_creatures')

    @api.constrains('level')
    def check_level(self):
        for record in self:
            if record.level > 15:
                raise ValidationError("Level cant be more than 15 %s" % record.level)


class building_type(models.Model):
    _name = 'dungeons.building_type'
    _description = 'Building types'

    name = fields.Char(string='type')
    image_building = fields.Image()
    production_iron = fields.Float()
    production_coal = fields.Float()
    production_steel = fields.Float()
    consume_iron = fields.Float()
    consume_coal = fields.Float()
    production_magical_creatures = fields.Float()
    production_warrior_creatures = fields.Float()
    production_defense_creatures = fields.Float()
    creature_type = fields.One2many('dungeons.creature_type', 'building_type')


class creature_type(models.Model):
    _name = 'dungeons.creature_type'
    _description = 'Creatures types'

    name = fields.Char(string='Creatures type')
    image_creature = fields.Image()
    life = fields.Float()
    defense = fields.Float()
    attack = fields.Float()
    building_type = fields.Many2one('dungeons.building_type', ondelete='set null')




class battle(models.Model):
    _name = 'dungeons.battle'
    _description = 'Battles'

    name = fields.Char()
    date_start = fields.Datetime()
    date_end = fields.Datetime()
    player1 = fields.Many2one('dungeons.player')
    player2 = fields.Many2one('dungeons.player')
    heart1 = fields.Many2one('dungeons.heart')
    heart2 = fields.Many2one('dungeons.heart')
    creature1_list = fields.Many2many('dungeons.creatures')

    @api.onchange('player1')
    def onchange_player1(self):
        self.name = self.player1.name
        return {
            'domain': {
                'heart1': [('id', 'in', self.player1.hearts.ids)],
                'heart2': [('id', '!=', self.player1.id)],
            }
        }

class creatures(models.Model):
    _name = 'dungeons.creatures'
    _description = 'Creatures'

    name = fields.Char()
    image = fields.Image(max_width=200, max_height=200)
    life = fields.Float()
    attack = fields.Float()
    defense = fields.Float()
    creation_time = fields.Float(compute='_get_creation_time')

    def _get_creation_time(self):
        for record in self:
            record.time = (record.attack + 2*record.life + 2*record.defense)

    def create(self):
        for s in self:
            print('Crea',self.env.context['ctx_heart'])
            heart= self.env['dungeons.heart'].browse(self.env.context['ctx_heart'])
            creature_type_rel = heart.creatures.filtered(lambda c: c.creature_id.id == s.id)
            if(len(creature_type_rel)== 0):
                creature_type_rel = self.env['dungeons.heart_creatures_rel'].create({
                    "creature_id": s.id,
                    "heart_id": heart.id,
                    "qty": 0
                })
            self.env['dungeons.heart_creatures_creation'].create({
                "creature_id": creature_type_rel.id,
                "progress": 0
            }) 
"""
class heart_creatures_rel(models.Model):
    _name = 'dungeons.heart_creatures_rel'
    _description = 'heart_creatures_rel'

    name = fields.Char(related="creatures_id.name")
    creature_id = fields.Many2one('dungeons.creatures')
    heart_id = fields.Many2one('dungeons.heart')
    qty = fields.Integer()
    creations = fields.One2many('dungeons.heart_creatures_creation', 'creatures_id')
    creations_queue = fields.Integer(compute="_get_creations_queue")
    creations_progress = fields.Float(compute="_get_creations_queue")

    def _get_creations_queue(self):
        for record in self:
            record.creations_queue = len(record.creations)
            record.fabrications_progress = record.creations[0].progress
"""
"""
class heart_creatures_creation(models.Model):
    _name = 'dungeons.heart_creatures_creation'
    _description = 'Creatures creation model'

    name = fields.Char(related="creatures_id.name")
    creatures_id = fields.Many2one('dungeons.heart_creatures_rel')
    progress = fields.Float()
"""