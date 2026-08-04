# -*- coding: utf-8 -*-
{
    'name': 'Website Customization',
    'version': '18.0.1.4.0',
    'summary': "Custom Theme Prime tweaks: editable USP preheader, custom CSS.",
    'description': "House module for custom Theme Prime / website tweaks that must "
                   "live outside the third-party theme_prime module: a natively "
                   "editable USP preheader (Custom Preheader - USP) plus a place "
                   "for custom SCSS.",
    'category': 'Website',
    'author': 'Aktiv Software',
    'website': 'https://www.aktivsoftware.com',
    'license': 'LGPL-3',
    'depends': ['theme_prime', 'website', 'website_sale_stock'],
    'data': [
        'views/preheader_templates.xml',
        'views/hide_variants_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_customization/static/src/scss/preheader.scss',
            'website_customization/static/src/scss/customizations.scss',
            'website_customization/static/src/js/website_sale_variant_filter.js',
            'website_customization/static/src/js/product_configurator_hide_variants.js',
        ],
    },
    'installable': True,
    'application': False,
}
