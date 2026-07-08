# -*- coding: utf-8 -*-
# Part of Odoo, SuperFoodsOnline and Aktiv Software.
# See LICENSE file for full copyright & licensing details.

{
    "name": "Actual Landed Cost",
    "summary": "Track actual landed cost and true COGS on sale order lines.",
    "version": "14.0.1.0.0",
    "category": "Purchase",
    "depends": ["sale_stock_margin","sale_margin",'stock_landed_costs'],
    "author": "Aktiv Software",
    'license': 'OPL-1',
    "website": "https://www.aktivsoftware.com",
    "data": [
        'views/sale_order_line_views.xml'
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
