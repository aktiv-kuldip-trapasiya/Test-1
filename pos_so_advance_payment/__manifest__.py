{
    'name': 'Create Sale Order, Delivery Address, Advance Payment from POS',
    'version': '14.0.1.0.0',
    'website': 'http://www.aktivsoftware.com',
    'category': 'Point of Sale',
    'author': 'Aktiv Software',
    'summary': "Create Sale Order, Manage Delivery Address and Register Advance Payment from POS" ,
    'description': """Create Sale Order, Manage Delivery Address and Register Advance Payment from POS.""",
    'depends': ['point_of_sale', 'sale_management'],
    'price': 20.00,
    'license': 'AGPL-3',
    'currency': "EUR",
    'data': [
        'views/pos_views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/pos.xml',
    ],
    'images': [
        'static/description/banner.jpg'
    ],
    'installable': True,
    'auto_install': False,
    'currency': 'EUR',
}
