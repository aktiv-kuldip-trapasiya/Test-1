# Copyright <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Versatil Green Custom",
    "summary": "",
    "version": "14.0.0.0.0",
    "category": "Base",
    "website": "https://www.qubiq.es",
    "author": "QubiQ",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ['account','sale_margin'],
    "data": [
        "reports/account_invoice_obra.xml",
        "data/report.xml",
        # "data/account_tax.xml",
        "reports/account_invoice.xml",
        "reports/report_saleorder_custom.xml",
        "reports/external_layout_background.xml",
        "views/sale_order_view.xml",
        # "views/account_move.xml",
             ],
}
