# -*- coding: utf-8 -*-

from odoo import models, fields, api

class player(models.Model):
    _name = 'dungeons.player'
    _description = 'players'

    name = fields.Char()
    avatar = fields.Image(max_width = 200, max_height = 200) #Atributo avatar que es una imagen y tiene un tamaño predeterminado.
    login = fields.Char()
    password = fields.Char()
    hearts_player = fields.One2many('dungeons.heart', 'player') #Relacion entre jugadores y mazmorras

class heart (models.Model):
    _name = 'dungeons.dungeon'
    _description = 'dungeons'
    
    name = fields.Char()
    
