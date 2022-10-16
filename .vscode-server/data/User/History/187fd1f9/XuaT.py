# -*- coding: utf-8 -*-

from odoo import models, fields, api

class player(models.Model):
    _name = 'dungeons.player'
    _description = 'players'

    name = fields.Char()
    avatar = fields.Image(max_width = 200, max_height = 200)
    login = fields.Char()
    password = fields.Char()
    dungeons_player = fields.One2many()

class dungeon (models.Model):
    _name = 'dungeons.dungeon'
    _description = 'dungeons'
    
    name = fields.Char()
    
