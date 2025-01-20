# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'product.template'

    is_rent = fields.Boolean(string="Can be Ranted")
    count_rent = fields.Integer()

    @api.depends('is_rent')
    def action_open_sale_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'views': [
                (self.env.ref('sale.view_order_tree').id, 'tree'),
                (self.env.ref('sale.view_order_form').id, 'form'),
            ],
        }
