# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError
import random
from datetime import datetime, timedelta




class player(models.Model):
    _name = 'res.partner'
    _description = 'players'
    _inherit = 'res.partner'# Indica que el modelo hereda de res.partner

    #name = fields.Char()
    avatar = fields.Image(max_width=200,
                          max_height=200)  # Atributo avatar que es una imagen y tiene un tamaño predeterminado.
    login = fields.Char()
    password = fields.Char()
    is_player = fields.Boolean(default=False)
    heart_player = fields.One2many(comodel_name='dungeons.heart',
                                   inverse_name='player')  # Relacion entre jugadores y mazmorras


class heart(models.Model):
    _name = 'dungeons.heart'
    _description = 'Hearts'

    name = fields.Char()
    avatar_heart = fields.Image(max_width=200, max_height=200)
    player = fields.Many2one('res.partner', domain="[('is_player','=',True)]", ondelete='cascade')
    life = fields.Integer(default=2000)
    iron = fields.Integer(default=100)
    coal = fields.Integer(default=50)
    steel = fields.Integer(default=10)
    gold = fields.Float(default=1000)
    location = fields.Integer(default=random.randint(1, 999))  # distancia random

    defense_creature = fields.Integer(default=0)
    magical_creature = fields.Integer(default=0)
    warrior_creature = fields.Integer(default=0)
    buildings = fields.One2many('dungeons.buildings', 'heart')
    creatures = fields.One2many('dungeons.creatures', 'heart')
    available_buildings = fields.Many2many('dungeons.building_type',
                                           compute="_get_available_buildings")  # Edificios disponibles.
    level_building_avaliable = fields.Many2many('dungeons.buildings', compute="_get_upgrade_buildings")

    production_coal = fields.Float(compute='_get_total_productions')
    production_iron = fields.Float(compute='_get_total_productions')
    production_steel = fields.Float(compute='_get_total_productions')
    production_magical_creatures = fields.Float(compute='_get_total_productions')
    production_warrior_creatures = fields.Float(compute='_get_total_productions')
    production_defense_creatures = fields.Float(compute='_get_total_productions')

    @api.depends('gold')  # Funcion para mostrar los edificios segun el oro disponible.
    def _get_available_buildings(self):
        for c in self:
            c.available_buildings = self.env['dungeons.building_type'].search([('gold_cost_base', '<=', c.gold)])


    def _get_upgrade_buildings(self):
        for c in self:
            c.level_building_avaliable = self.env['dungeons.buildings'].search([('heart', '<=', c.id)])

    @api.constrains('iron')  # funcion para restringir la cantidad de hierro que se puede tener.
    def _check_iron(self):
        for record in self:
            if record.iron > 3000:
                raise ValidationError("You have too much iron %s" % record.iron)

    @api.constrains('coal')
    def _check_coal(self):
        for record in self:
            if record.coal > 3000:
                raise ValidationError("You have too much coal %s" % record.coal)

    @api.constrains('steel')
    def _check_steel(self):
        for record in self:
            if record.steel > 3000:
                raise ValidationError("You have too much steel %s" % record.steel)

    @api.depends('buildings')  # Funcion para sumar al heart las producciones de todos los edificios.
    def _get_total_productions(self):
        for h in self:
            h.production_coal = sum(h.buildings.mapped('production_coal'))
            h.production_iron = sum(h.buildings.mapped('production_iron'))
            h.production_steel = sum(h.buildings.mapped('production_steel'))
            h.production_magical_creatures = sum(h.buildings.mapped('production_magical_creatures'))
            h.production_warrior_creatures = sum(h.buildings.mapped('production_warrior_creatures'))
            h.production_defense_creatures = sum(h.buildings.mapped('production_defense_creatures'))

           # h.env['dungeons.creatures'].create({
            #   "heart": h.id,
           #    "creature_type": h.env['dungeons.creature_type'].ids[0]
            #})
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
            gold = heart.gold + 10

            heart.write({
                "iron": iron,
                "coal": coal,
                "steel": steel,
                "magical_creature": magical,
                "defense_creature": defense,
                "warrior_creature": warrior,
                "gold": gold

            })

    def distance(self, other_heart):  # Define la distancia entre un heart y otro
        distance = 0
        if len(self) > 0 and len(other_heart) > 0:
            distance = abs(self.location - other_heart.location)
        return distance


class buildings(models.Model):
    _name = 'dungeons.buildings'
    _description = 'Buildings'

    name = fields.Char()
    level = fields.Integer(default=1)
    heart = fields.Many2one('dungeons.heart', ondelete='restrict')
    building_type = fields.Many2one('dungeons.building_type', ondelete='restrict')
    image_building = fields.Image(max_width=200, max_height=200, related='building_type.image_building')

    gold_cost_base = fields.Float(related='building_type.gold_cost_base')
    coal_cost_base = fields.Float()
    iron_cost_base = fields.Float()
    steel_cost_base = fields.Float()

    required_coal_levelup = fields.Float(compute='_get_required_coal_levelup')
    required_iron_levelup = fields.Float(compute='_get_required_iron_levelup')
    required_steel_levelup = fields.Float(compute='_get_required_steel_levelup')

    production_iron = fields.Float(compute="_get_productions")
    production_coal = fields.Float(compute="_get_productions")
    production_steel = fields.Float(compute="_get_productions")
    production_magical_creatures = fields.Float(compute="_get_productions")
    production_warrior_creatures = fields.Float(compute="_get_productions")
    production_defense_creatures = fields.Float(compute="_get_productions")



    def _get_required_coal_levelup(self):
        for b in self:
            b.required_coal_levelup = 4 ** b.level

    def _get_required_iron_levelup(self):
        for b in self:
            b.required_iron_levelup = 4 ** b.level

    def _get_required_steel_levelup(self):
        for b in self:
            b.required_steel_levelup = 4 ** b.level

    def levelupgrade_building(self):
        for b in self:
            required_coal = b.required_coal_levelup
            available_coal = b.heart.coal

            required_steel = b.required_steel_levelup
            available_steel = b.heart.steel

            required_iron = b.required_iron_levelup
            available_iron = b.heart.iron

            if (required_coal <= available_coal and required_iron <= available_iron and required_steel <= available_steel):
                b.level += 1
                b.heart.coal = b.heart.coal - required_coal
                b.heart.steel = b.heart.steel - required_steel
                b.heart.iron = b.heart.coal - required_iron

            else:
                raise ValidationError("You don't have enough coal or steel or iron")

    @api.constrains('level')
    def check_level(self):
        for record in self:
            if record.level > 15:
                raise ValidationError("Level cant be more than 15 %s" % record.level)

    def _get_productions(self):
        for b in self:
            level = b.level
            # Expected productions
            production_coal = b.building_type.production_coal * level
            production_iron = b.building_type.production_iron * level
            production_steel = b.building_type.production_steel * level
            production_magical_creatures = b.building_type.production_magical_creatures * level
            production_warrior_creatures = b.building_type.production_warrior_creatures * level
            production_defense_creatures = b.building_type.production_defense_creatures * level

            if production_coal + b.heart.coal >= 0 and production_iron + b.heart.iron >= 0 and production_steel +\
                    b.heart.steel >= 0 and production_magical_creatures + b.heart.magical_creature >= 0 and \
                    production_warrior_creatures + b.heart.warrior_creature >= 0 and production_defense_creatures +\
                    b.heart.defense_creature >= 0:
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
    speed = fields.Float(default=5)
    creation_time = fields.Float(compute='_get_creation_time')
    heart = fields.Many2one('dungeons.heart')
    creature_type = fields.Many2one('dungeons.creature_type')


class battle(models.Model):  # falta terminar
    _name = 'dungeons.battle'
    _description = 'Battles'

    name = fields.Char()
    image_battle = fields.Image(max_width=200, max_height=200)
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now)
    date_end = fields.Datetime(compute='_get_time')
    time = fields.Float(compute='_get_time')
    distance = fields.Float(compute='_get_time')
    progress = fields.Float()
    state = fields.Selection([('1', 'Preparation'), ('2', 'Send'), ('3', 'Finished')], default='1')
    player1 = fields.Many2one('res.partner')
    player2 = fields.Many2one('res.partner')
    heart1 = fields.Many2one('dungeons.heart')
    heart2 = fields.Many2one('dungeons.heart')
    creatures1_list = fields.One2many('dungeons.battle_creatures_rel', 'battle_id')
    creatures1_available = fields.Many2many('dungeons.heart_creatures_rel', compute='_get_creatures_available')
    total_power = fields.Float()  # ORM Mapped
    # winner = fields.Many2one()
    draft = fields.Boolean()

    @api.depends('creatures1_list', 'heart2', 'heart1')
    def _get_time(self):
        for b in self:
            b.time = 0
            b.distance = 0
            b.date_end = fields.Datetime.now()
            if len(b.heart1) > 0 and len(b.heart2) > 0 and len(b.creatures1_list) > 0 and len(
                    b.creatures1_list.creatures_id) > 0:
                b.distance = b.heart1.distance(b.heart2)
                min_speed = b.creatures1_list.creatures_id.sorted(lambda s: s.speed).mapped('speed')[0]
                b.time = b.distance / min_speed
                b.date_end = fields.Datetime.to_string(
                    fields.Datetime.from_string(b.date_start) + timedelta(minutes=b.time))

    @api.onchange('player1')
    def onchange_player1(self):
        if len(self.player1) > 0:
            self.name = self.player1.name
            return {
                'domain': {
                    'heart1': [('id', 'in', self.player1.heart_player.ids)],
                    'player2': [('id', '!=', self.player1.id)],
                }
            }

    @api.onchange('player2')
    def onchange_player2(self):
        if len(self.player2) > 0:
            return {
                'domain': {
                    'heart2': [('id', 'in', self.player2.heart_player.ids)],
                    'player1': [('id', '!=', self.player2.id)],
                }
            }

    @api.depends('heart1')
    def _get_creatures_available(self):

        for b in self:
            print(b.heart1.creatures.ids)
            b.creatures1_available = b.heart1.creatures.ids

    def launch_battle(self):
        for b in self:
            if len(b.heart1) == 1 and len(b.heart2) == 1 and len(b.creatures1_list) > 0 and b.state == '1':
                print("entra")
                b.date_start = fields.Datetime.now()
                b.progress = 0
                for s in b.creatures1_list:
                    creatures_available = \
                        b.creatures1_available.filtered(lambda s_a: s_a.creatures_id.id == s.creatures_id.id)[0]
                    creatures_available.qty -= s.qty
                b.state = '2'

    def back(self):
        for b in self:
            if b.state == '2':
                b.state = '1'



    def execute_battle(self):
        print("execute")

    def back(self):
        print("back")

    def simulate_battle(self):
        print("simulate")
       # b = self
       # winner = False
        #draft = False
       # creatures1 = b.creatures1_list.mapped(lambda s:[s.creatures_id.read(['id', 'life', 'attack', 'defense'])])


class battle_creatures_rel(models.Model):
    _name = 'dungeons.battle_creatures_rel'
    _description = 'battle_creatures_rel'

    name = fields.Char(related="creatures_id.name")
    creatures_id = fields.Many2one('dungeons.creatures')
    battle_id = fields.Many2one('dungeons.battle')
    qty = fields.Integer()


class heart_creatures_rel(models.Model):
    _name = 'dungeons.heart_creatures_rel'
    _description = 'heart_creatures_rel'

    name = fields.Char(related="creatures_id.name")
    creatures_id = fields.Many2one('dungeons.creatures')
    heart_id = fields.Many2one('dungeons.heart')
    qty = fields.Integer()

    def add_to_battle(self):  # ORM
        for c in self:
            if (c.qty > 0):
                battle_id = self.env['dungeons.battle'].browse(self.env.context['ctx_battle'])[0]
                current_creatures = battle_id.creatures1_list.filtered(
                    lambda s: s.creatures_id.id == c.creatures_id.id)
                if len(current_creatures) == 0:
                    current_creatures = self.env['dungeons.battle_creatures_rel'].create({
                        "creatures_id": c.creatures_id.id,
                        "battle_id": battle_id.id,
                        "qty": 0
                    })
                if current_creatures.qty < c.qty:
                    current_creatures.qty += 1
                # c.qty -= 1
