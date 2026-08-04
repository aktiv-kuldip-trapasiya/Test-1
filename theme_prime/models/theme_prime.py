# -*- coding: utf-8 -*-
# Copyright (c) 2019-Present Droggol Infotech Private Limited. (<https://www.droggol.com/>)

from odoo import api, models


class ThemePrime(models.AbstractModel):
    _inherit = 'theme.utils'

    @api.model
    def _reset_default_config(self):
        header_styles = list(range(1, 9))
        for style in header_styles:
            self.disable_view('theme_prime.template_header_style_%s' % style)

        footer_styles = list(range(1, 11))
        for style in footer_styles:
            self.disable_view('theme_prime.template_footer_style_%s' % style)

        super()._reset_default_config()
from odoo import http
from odoo.http import request

class WebsiteStockController(http.Controller):

    @http.route('/shop/get_allow_oos', type='json', auth='public')
    def get_allow_oos(self, product_id):
        product = request.env['product.product'].sudo().browse(product_id)
        return product.allow_out_of_stock_order
