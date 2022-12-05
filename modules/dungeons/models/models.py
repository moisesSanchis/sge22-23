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
    gold = fields.Float(default=1000)
    defense_creature = fields.Integer(default=0)
    magical_creature = fields.Integer(default=0)
    warrior_creature = fields.Integer(default=0)
    buildings = fields.One2many('dungeons.buildings', 'heart')
    creatures = fields.One2many('dungeons.creatures', 'heart')
    available_buildings = fields.Many2many('dungeons.building_type', compute="_get_available_buildings")

    production_coal = fields.Float(compute='_get_total_productions')
    production_iron = fields.Float(compute='_get_total_productions')
    production_steel = fields.Float(compute='_get_total_productions')
    production_magical_creatures= fields.Float(compute='_get_total_productions')
    production_warrior_creatures = fields.Float(compute='_get_total_productions')
    production_defense_creatures= fields.Float(compute='_get_total_productions')


    @api.depends('gold')
    def _get_available_buildings(self):
        for c in self:
            c.available_buildings = self.env['dungeons.building_type'].search([('gold_cost_base', '<=', c.gold)])


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

    @api.depends('buildings')
    def _get_total_productions(self):
        for h in self:
            h.production_coal = sum(h.buildings.mapped('production_coal'))
            h.production_iron = sum(h.buildings.mapped('production_iron'))
            h.production_steel = sum(h.buildings.mapped('production_steel'))
            h.production_magical_creatures = sum(h.buildings.mapped('production_magical_creatures'))
            h.production_warrior_creatures = sum(h.buildings.mapped('production_warrior_creatures'))
            h.production_defense_creatures = sum(h.buildings.mapped('production_defense_creatures'))

    @api.model
    def produce(self):  # ORM CRON
        self.search([]).produce_heart()

    def produce_heart(self):
        for heart in self:
            coal = heart.coal + heart.production_coal
            steel = heart.steel + heart.production_steel
            iron = heart.iron + heart.production_iron
            magical = heart.magical_creature + heart.production_magical_creatures
            defense = heart.defense_creature + heart.production_defense_creatures
            warrior = heart.warrior_creature + heart.production_warrior_creatures

            heart.write({
                "iron": iron,
                "coal": coal,
                "steel": steel,
                "magical_creature": magical,
                "defense_creature": defense,
                "warrior_creature": warrior

            })

class buildings(models.Model):
    _name = 'dungeons.buildings'
    _description = 'Buildings'

    name = fields.Char()
    level = fields.Integer(default=1)
    heart = fields.Many2one('dungeons.heart', ondelete='restrict')
    building_type = fields.Many2one('dungeons.building_type', ondelete='restrict')
    image_building = fields.Image(max_width=200, max_height=200, related='building_type.image_building')
    gold_cost_base = fields.Float(related='building_type.gold_cost_base')
    production_iron = fields.Float(compute="_get_productions")
    production_coal = fields.Float(compute="_get_productions")
    production_steel = fields.Float(compute="_get_productions")
    production_magical_creatures = fields.Float(compute="_get_productions")
    production_warrior_creatures = fields.Float(compute="_get_productions")
    production_defense_creatures = fields.Float(compute="_get_productions")

    @api.constrains('level')
    def check_level(self):
        for record in self:
            if record.level > 15:
                raise ValidationError("Level cant be more than 15 %s" % record.level)

    def _get_productions(self):
        for b in self:
            level = b.level
            # Expected productions

            # Expected productions
            production_coal = b.building_type.production_coal * level
            production_iron = b.building_type.production_iron * level
            production_steel = b.building_type.production_steel * level
            production_magical_creatures = b.building_type.production_magical_creatures * level
            production_warrior_creatures = b.building_type.production_warrior_creatures * level
            production_defense_creatures = b.building_type.production_defense_creatures * level

            if production_coal + b.heart.coal >= 0 and production_iron + b.heart.iron >= 0 and production_steel + b.heart.steel >= 0 and   production_magical_creatures + b.heart.magical_creature >= 0 and  production_warrior_creatures + b.heart.warrior_creature  >= 0 and  production_defense_creatures + b.heart.defense_creature  >= 0:
                b.production_coal = production_coal
                b.production_iron = production_iron
                b.production_steel = production_steel
                b.production_magical_creatures = production_magical_creatures
                b.production_warrior_creatures = production_warrior_creatures
                b.production_defense_creatures = production_defense_creatures

            else:
                b.production_coal = 0
                b.production_iron = 0
                b.production_steel = 0
                b.production_magical_creatures = 0
                b.production_warrior_creatures = 0
                b.production_defense_creatures = 0



class building_type(models.Model):
    _name = 'dungeons.building_type'
    _description = 'Building types'

    name = fields.Char(string='type')
    image_building = fields.Image()
    production_iron = fields.Float()
    production_coal = fields.Float()
    production_steel = fields.Float()
    gold_cost_base = fields.Float()
    production_magical_creatures = fields.Float()
    production_warrior_creatures = fields.Float()
    production_defense_creatures = fields.Float()

    def create_building(self):
        for record in self:

            heart = self.env['dungeons.heart'].browse(self.env.context['ctx_heart'])[0]
            if heart.gold >= record.gold_cost_base:
                self.env['dungeons.buildings'].create({
                    "heart": heart.id,
                    "building_type": record.id
                })
                heart.gold -= record.gold_cost_base






class creature_type(models.Model):
    _name = 'dungeons.creature_type'
    _description = 'Creatures types'

    name = fields.Char(string='Creatures type')
    image_creature = fields.Image()
    life = fields.Float()
    defense = fields.Float()
    attack = fields.Float()





class creatures(models.Model):
    _name = 'dungeons.creatures'
    _description = 'Creatures'

    name = fields.Char()
    image = fields.Image(max_width=200, max_height=200)
    life = fields.Float()
    attack = fields.Float()
    defense = fields.Float()
    creation_time = fields.Float(compute='_get_creation_time')
    heart = fields.Many2one('dungeons.heart')
    creature_type = fields.Many2one('dungeons.creature_type')





