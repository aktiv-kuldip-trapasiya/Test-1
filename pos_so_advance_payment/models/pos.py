# -*- coding: utf-8 -*-
import time
from datetime import datetime
from odoo import fields, models, api, _
from functools import partial


class sale_order(models.Model):
    _inherit = 'sale.order'

    def _order_line_fields(self, line):
        if line and 'tax_ids' not in line[2]:
            product = self.env['product.product'].browse(line[2]['product_id'])
            line[2]['tax_ids'] = [(6, 0, [x.id for x in product.taxes_id])]
        line[2]['product_uom_qty'] = line[2]['qty']
        return line

    @api.model
    def _order_fields(self, ui_order):
        partner = self.env['res.partner']
        process_line = partial(self._order_line_fields)
        shipping_id = False
        if ui_order.get('partner_shiping_id'):
            shipping_id = ui_order.get('partner_shiping_id')
            partner.browse([shipping_id]).write(
                {'street': ui_order.get('street'),
                 'street2': ui_order.get('street2'),
                 'city': ui_order.get('city'),
                 'phone': ui_order.get('phone'),
                 'mobile': ui_order.get('mobile')})
        else:
            shipping_id = partner.create({
                'name': ui_order.get('c_name'),
                'street': ui_order.get('street'),
                'street2': ui_order.get('street2'),
                'city': ui_order.get('city'),
                'parent_id': ui_order.get('parent_id'),
                'phone': ui_order.get('phone'),
                'mobile': ui_order.get('mobile'),
                'type': 'delivery',
            }).id
        return {
            'user_id': ui_order['user_id'],
            'order_line': [process_line(l) for l in ui_order['lines']] if
            ui_order['lines'] else False,
            'partner_id': ui_order['partner_id'] or False,
            'fiscal_position_id': ui_order['fiscal_position_id'],
            'note': ui_order['so_notes'],
            'partner_shipping_id': shipping_id
        }

    def register_down_payment_inv(self, register_down_payment_inv_rec,
                                  journal_id):
        account_payment = self.env['account.payment']
        fields = ['amount', 'journal_id', 'payment_date', 'partner_type',
                  'partner_id', 'payment_type', 'invoice_ids',
                  'payment_method_id']
        payment_dict = account_payment.with_context(default_invoice_ids=[
            (4, register_down_payment_inv_rec.id, None)]).default_get(fields)
        payment_id = account_payment.create({
            'amount': payment_dict.get('amount') or False,
            'journal_id': journal_id,
            'payment_date': payment_dict.get('payment_date') or False,
            'partner_type': payment_dict.get('partner_type') or False,
            'partner_id': payment_dict.get('partner_id') or False,
            'payment_type': payment_dict.get('payment_type') or False,
            'invoice_ids': payment_dict.get('invoice_ids') or False,
            'payment_method_id': self.env.ref(
                'account.account_payment_method_manual_in').id,
        })
        payment_id.post()

    @api.model
    def create_new_quotation(self, quotation):
        quotation_obj = self.create(self._order_fields(quotation))
        session_id = self.env['pos.session'].browse(
            quotation['pos_session_id'])
        adv_payment_product = False
        if session_id.config_id.pos_sale_order_state == 'sale_order':
            quotation_obj.action_confirm()
            # create down payment invoice of sale order.
            if quotation.get('advance_pay') and \
                    float(quotation.get('advance_pay')) > 0:
                adv_payment = self.env['sale.advance.payment.inv']
                sale_line_obj = self.env['sale.order.line']
                amount = float(quotation.get('advance_pay'))
                adv_payment_rec = adv_payment.create(
                    {'advance_payment_method': 'fixed',
                     'amount': amount})
                if not adv_payment_rec.product_id:
                    vals = adv_payment_rec._prepare_deposit_product()
                    adv_payment_rec.product_id = self.env[
                        'product.product'].create(vals)
                    self.env['ir.config_parameter'].sudo().set_param(
                        'sale.default_deposit_product_id',
                        adv_payment_rec.product_id.id)
                taxes = adv_payment_rec.product_id.taxes_id.filtered(
                    lambda r: not quotation_obj.company_id or
                              r.company_id == quotation_obj.company_id)
                if quotation_obj.fiscal_position_id and taxes:
                    tax_ids = quotation_obj.fiscal_position_id.map_tax(
                        taxes).ids
                else:
                    tax_ids = taxes.ids
                so_line = sale_line_obj.create({
                    'name': _('Advance: %s') % (time.strftime('%m %Y'),),
                    'price_unit': amount,
                    'product_uom_qty': 0.0,
                    'order_id': quotation_obj.id,
                    'discount': 0.0,
                    'product_uom': adv_payment_rec.product_id.uom_id.id,
                    'product_id': adv_payment_rec.product_id.id,
                    'tax_id': [(6, 0, tax_ids)],
                    'is_downpayment': True,
                })
                down_payment_inv_rec = adv_payment_rec._create_invoice(
                    quotation_obj, so_line, amount)
                adv_payment_product = adv_payment_rec.product_id
                down_payment_inv_rec.action_date_assign()
                # Create account move of invoice
                down_payment_inv_rec.action_move_create()
                # Change state of invoice draft to open.
                down_payment_inv_rec.invoice_validate()

                # Register payment of down_payment invoice
                self.register_down_payment_inv(
                    down_payment_inv_rec,
                    quotation.get('payment_journal'))

            # If any product contains ordered invoice policy then sale order's
            # invoice will be created with open state.
            order_lines = quotation_obj.order_line.filtered(
                lambda line: line.product_id.invoice_policy == 'order' and
                             line.product_id != adv_payment_product)
            if order_lines:
                quotation_obj.action_invoice_create(final=True)
                # Set due date of invoice
                quotation_obj.invoice_ids.action_date_assign()
                # Create account move of invoice
                quotation_obj.invoice_ids.action_move_create()
                # Change state of invoice draft to open.
                quotation_obj.invoice_ids.invoice_validate()
        return {'result': quotation_obj.name}


class pos_config(models.Model):
    _inherit = 'pos.config'

    allow_create_sale_order = fields.Boolean("Enable Creating SO from POS")
    pos_sale_order_state = fields.Selection([('draft', 'Quotation'),
                                             ('sale_order', 'Confirm')], default='draft',string='Default SO State')
    allow_advance_payment = fields.Boolean("Advance Payment")

    @api.onchange('pos_sale_order_state', 'allow_create_sale_order')
    def _onchange_so_state(self):
        if not self.allow_create_sale_order:
            self.allow_advance_payment = False
        if self.pos_sale_order_state == 'draft':
            self.allow_advance_payment = False
