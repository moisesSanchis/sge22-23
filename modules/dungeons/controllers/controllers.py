# -*- coding: utf-8 -*-
# from odoo import http


# class Dungeons(http.Controller):
#     @http.route('/dungeons/dungeons', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dungeons/dungeons/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dungeons.listing', {
#             'root': '/dungeons/dungeons',
#             'objects': http.request.env['dungeons.dungeons'].search([]),
#         })

#     @http.route('/dungeons/dungeons/objects/<model("dungeons.dungeons"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dungeons.object', {
#             'object': obj
#         })
