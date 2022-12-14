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

class heart(models.Model): #falta que no se puedan modificar los campos y añadir las relaciones entre edificios y heart
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
    
"""
class building(models.Model):
     _name = 'dungeons.building' 
    _description = 'Building'
     
    level = fields.Integer(default = 1)
    production_iron = fields.Integer(default = 1)
    production_coal = fields.Integer(default = 1)
    production_steel = fields.Integer(default = 1)
    consume_iron = fields.Integer(default = 1)
    consume_coal = fields.Integer(default = 2)
    producton_magical_creatures = fields.Integer()
    producton_warrior_creatures = fields.Integer()
    producton_defense_creatures = fields.Integer()
"""
 
class ironmine(models.Model):
     _name = 'dungeons.ironmine' 
     _description = 'Ironmines'  
     
     level = fields.Integer(default = 1)
     production_iron = fields.Integer(default = 1) #falta poner el tiempo
     
class coalmine(models.Model):
     _name = 'dungeons.coalmine' 
     _description = 'Coalmines'  
     
     level = fields.Integer(default = 1)
     production_coal = fields.Integer(default = 1)
     
class forge(models.Model):
     _name = 'dungeons.forge' 
     _description = 'Forge'  
     
     level = fields.Integer(default = 1)
     production_steel = fields.Integer(default = 1)
     consume_iron = fields.Integer(default = 1)
     consume_coal = fields.Integer(default = 2)
     
class hatchery (models.Model):
    _name = 'dungeons.hatchery' 
    _description = 'Hatchery'
     
    level = fields.Integer(default = 1)
    producton_magical_creatures = fields.Integer()
    producton_warrior_creatures = fields.Integer()
    producton_defense_creatures = fields.Integer()
    
class defense_creatures (models.Model):
    _name = 'dungeons.defense_creatures' 
    _description = 'Defense Creatures'
    
    life = fields.Integer(default = 50)
    
    
class magical_creatures (models.Model):
    _name = 'dungeons.magical_creatures' 
    _description = 'Magical Creatures'
    
    attack = fields.Integer(default = 100)
    
class warrior_creatures (models.Model):
    _name = 'dungeons.warrior_creatures' 
    _description = 'Warrior Creatures'
    
    attack = fields.Integer(default = 20)