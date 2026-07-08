from odoo import models, fields


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    refernce_report = fields.Char(string='Referencia')


class SaleOrderLine(models.Model):

    _inherit = "sale.order.line"

    product_uom_q = fields.Many2one('uom.uom', string='Unit of Measure')
