# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    state = fields.Selection([
        ('draf', 'Draft'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draf')
    approver_id = fields.Many2one('res.users', readonly=True)

    def action_approve(self):
        for rec in self:
            rec.approver_id = self.env.user.id #env.uid
            rec.state = 'approved'

    def action_cancelled(self):
        for rec in self:
            rec.state = 'cancelled'

    def action_reset(self):
        for rec in self:
            rec.state = 'draf'