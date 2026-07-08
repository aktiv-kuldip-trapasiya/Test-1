from odoo import models, fields, api, _
from collections import defaultdict
from odoo.tools.misc import formatLang
from odoo.exceptions import UserError


class AccountMove(models.Model):

    _inherit = 'account.move'

    retention_perc = fields.Boolean(string='% Retención Garantía')

    warranty_retention = fields.Monetary(string='Retención por garantía', compute='_compute_warranty_retention')
    subtotal_obra = fields.Monetary(string='Base Imponible', compute='_compute_warranty_retention')

    amount_by_group_obra = fields.Binary(string="Tax amount by group",
        compute='_compute_invoice_taxes_by_group_obra')

    amount_total_obra = fields.Monetary(string='Total', compute='_compute_amount_obra')

    @api.depends("amount_untaxed", "retention_perc")
    def _compute_warranty_retention(self):
        for rec in self:
            perc = 5 if rec.retention_perc else 0
            warranty_retention = 0
            subtotal_obra = 0
            amount_total = 0
            if rec.amount_untaxed:
                warranty_retention = rec.amount_untaxed * (perc / 100)
                subtotal_obra = rec.amount_untaxed
                amount_total = (
                    rec.amount_untaxed + rec.amount_tax - warranty_retention
                )
                rec.amount_total = amount_total
            rec.warranty_retention = warranty_retention
            rec.subtotal_obra = subtotal_obra

    @api.constrains("retention_perc")
    def _update_retention(self):
        for rec in self:
            tax_id = self.env.ref("vg_custom.1_account_tax_template_ret_garantia").id
            for line in rec.invoice_line_ids:
                if line.product_id:
                    if rec.retention_perc:
                        line.tax_ids = [(4, tax_id)]
                    elif tax_id in line.tax_ids.ids:
                        line.tax_ids = [(3, tax_id)]
            rec._recompute_dynamic_lines(recompute_all_taxes=True, recompute_tax_base_amount=True)


    @api.depends(
        "line_ids.price_subtotal",
        "line_ids.tax_base_amount",
        "line_ids.tax_line_id",
        "partner_id",
        "currency_id",
    )
    def _compute_invoice_taxes_by_group_obra(self):
        for move in self:

            # Not working on something else than invoices.
            if not move.is_invoice(include_receipts=True):
                move.amount_by_group = []
                continue

            balance_multiplicator = -1 if move.is_inbound() else 1

            tax_lines = move.line_ids.filtered('tax_line_id')
            base_lines = move.line_ids.filtered('tax_ids')

            tax_group_mapping = defaultdict(lambda: {
                'base_lines': set(),
                'base_amount': 0.0,
                'tax_amount': 0.0,
            })

            # Compute base amounts.
            tax_group_vals = None
            for base_line in base_lines:
                base_amount = balance_multiplicator * (base_line.amount_currency if base_line.currency_id else base_line.balance)

                for tax in base_line.tax_ids.flatten_taxes_hierarchy():

                    if base_line.tax_line_id.tax_group_id == tax.tax_group_id:
                        continue

                    tax_group_vals = tax_group_mapping[tax.tax_group_id]
                    if base_line not in tax_group_vals['base_lines']:
                        tax_group_vals['base_amount'] += base_amount
                        tax_group_vals['base_lines'].add(base_line)

            # Compute tax amounts.
            # if tax_group_vals:
            #     tax_group_vals['base_amount'] -= move.warranty_retention
            tax_ret = self.env.ref("vg_custom.1_account_tax_template_ret_garantia")
            for tax_line in tax_lines:
                if tax_line.tax_line_id != tax_ret:
                    tax_amount = tax_group_vals['base_amount'] * (tax_line.tax_line_id.amount/100)
                    tax_group_vals = tax_group_mapping[tax_line.tax_line_id.tax_group_id]
                    tax_group_vals['tax_amount'] += tax_amount
            tax_groups = sorted(tax_group_mapping.keys(), key=lambda x: x.sequence)
            amount_by_group = []
            for tax_group in tax_groups:
                if tax_group != self.env.ref("vg_custom.tax_group_retencion_garantia"):
                    tax_group_vals = tax_group_mapping[tax_group]
                    amount_by_group.append((
                        tax_group.name,
                        tax_group_vals['tax_amount'],
                        tax_group_vals['base_amount'],
                        formatLang(self.env, tax_group_vals['tax_amount'], currency_obj=move.currency_id),
                        formatLang(self.env, tax_group_vals['base_amount'], currency_obj=move.currency_id),
                        len(tax_group_mapping),
                        tax_group.id
                    ))
            move.amount_by_group_obra = amount_by_group

    @api.depends('line_ids')
    def _compute_amount_obra(self):
        for rec in self:
            taxes = 0
            for tax in rec.amount_by_group_obra:
                taxes += tax[1]
            rec.amount_total_obra = rec.subtotal_obra + taxes - rec.warranty_retention

# class AccountMoveLine(models.Model):

#    _inherit = 'account.move.line'

#    def _check_reconciliation(self):
 #       if not self._context.get("no_validation"):
  #          for line in self:
   #             if line.matched_debit_ids or line.matched_credit_ids:
    #                raise UserError(_("You cannot do this modification on a reconciled journal entry. "
     #                               "You can just change some non legal fields or you must unreconcile first.\n"
      #                              "Journal Entry (id): %s (%s)") % (line.move_id.name, line.move_id.id)) -->
