# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_rental_order = fields.Boolean()
    rental_start_date = fields.Datetime(string="Start Date")
    rental_return_date = fields.Datetime(string="End Date")
    duration_days = fields.Integer(string="Durations (days)", compute="_compute_duration_days", store=True)
    rental_status = fields.Selection([
        ('draft', 'Draft'),
        ('reserved', 'Reserved'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], default='draft')

    @api.depends('rental_start_date', 'rental_return_date')
    def _compute_duration_days(self):
        for record in self:
            if record.rental_start_date and record.rental_return_date:
                # Calculate the difference in days
                delta = fields.Date.from_string(record.rental_return_date) - fields.Date.from_string(record.rental_start_date)
                record.duration_days = max(delta.days, 0)
            else:
                record.duration_days = 0

    def action_confirm(self):
        res = super(SaleOrder, self).action_confim()
        for order in self:
            if order.is_rental_order:
                now = fields.Datetime.now()
                if order.rental_start_date <= now <= order.rental_return_date:
                    order.rental_status = 'reserved'
        return res

    def action_reserve(self):
        for order in self:
            order.rental_status = 'reserved'

    def action_turn_in(self):
        for order in self:
            order.rental_status = 'returned'

    @api.onchange('rental_return_date')
    def _onchange_rental_return_date(self):
        is_prior  = self.rental_return_date >= self.rental_start_date
        if not is_prior:
            self.rental_return_date = False
            return  {"warning": {"title": "Warning", "message": "Return date must higher than start date"}}
