# -*- coding: utf-8 -*-

from odoo import models, fields, api

class player(models.Model):
    _name = 'dungeons.player'
    _description = 'players'

    name = fields.Char()
    avatar = fields.Image(max_width = 200, max_height = 200) #Atributo avatar que es una imagen y tiene un tamaño predeterminado.
    login = fields.Char()
    password = fields.Char()
    heart_player = fields.One2many('dungeons.heart', 'player') #Relacion entre jugadores y mazmorras

class heart(models.Model): 
    _name = 'dungeons.heart'
    _description = 'Hearts'
    
    name = fields.Char()
    player = fields.Many2one('dungeons.player')
    life = fields.Integer(default = 2000)
    iron = fields.Integer(default = 100)
    coal = fields.Integer(default = 50)
    steel = fields.Integer(default = 10)
    defense_creature = fields.Integer(default = 0)
    magical_creature = fields.Integer(default = 0)
    warrior_creature = fields.Integer(default = 0)
    buildings = fields.One2many('dungeons.buildings', 'heart')
    
class buildings(models.Model):
    _name = 'dungeons.buildings' 
    _description = 'Buildings'
    
    name = fields.Char() 
    level = fields.Integer()
    heart = fields.Many2one('dungeons.heart')
    building_type = fields.One2many('dungeons.building_type', 'buildings')
    production_iron = fields.Integer(related = '')
    production_coal = fields.Integer()
    production_steel = fields.Integer()
    consume_iron = fields.Integer()
    consume_coal = fields.Integer()
    producton_magical_creatures = fields.Integer()
    producton_warrior_creatures = fields.Integer()
    producton_defense_creatures = fields.Integer()
    
    
 
class building_type(models.Model):
    _name = 'dungeons.building_type'
    _description = 'Building types'
     
    name = fields.Char()
    production_iron = fields.Integer()
    production_coal = fields.Integer()
    production_steel = fields.Integer()
    consume_iron = fields.Integer()
    consume_coal = fields.Integer()
    producton_magical_creatures = fields.Integer()
    producton_warrior_creatures = fields.Integer()
    producton_defense_creatures = fields.Integer()
   