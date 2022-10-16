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
    iron = fields.Integer(default = 100)
    coal = fields.Integer(default = 50)
    steel = fields.Integer(default = 10)
 
 class ironmine(models.Model):
     _name = 'ironmine' 
     _description = 'Ironmines'  

