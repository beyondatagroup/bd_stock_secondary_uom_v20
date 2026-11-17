# -*- coding: utf-8 -*-
#############################################################################
#
#    BeyonData Solutions Private Limited
#
#    Copyright (C) BeyonData Solutions Pvt. Ltd.
#    Author: BeyonData Solutions Pvt. Ltd.
#    Website: https://www.beyondatagroup.com
#
#############################################################################

{
    "name": "Stock Secondary Unit of Measure",
    "version": '20.0.1.0.0',
    "category": "Inventory",
    "summary": "Use Secondary Unit of Measure in Inventory Operations.",
    "description": """
        Stock Secondary Unit of Measure
        ===============================

        This module extends the Product Secondary Unit of Measure module to
        support secondary units in Inventory Operations.

        Features
        --------
        * Display Secondary Unit of Measure on Stock Moves.
        * Display Secondary Quantity in Inventory Transfers.
        * Automatic conversion between Primary and Secondary UoM.
        * Support for Receipts, Delivery Orders, and Internal Transfers.
        * Support for Inventory Reports.
        * Compatible with Odoo 20.
    """,
    "author": "BeyonData Solutions Private Limited",
    "website": "https://www.beyondatagroup.com",
    "license": "OPL-1",
    "depends": [
        "base",
        "stock",
        "bd_product_secondary_uom",
    ],
    "data": [
        "security/groups.xml",
        "views/stock_picking_views.xml",
        "views/stock_picking_templates.xml",
        "views/stock_quant_views.xml",
        "views/stock_scrap.xml",
    ],
    "images": [
        "static/description/banner.gif",
    ],

    "price": "4.99",
    "currency": "EUR",

    "installable": True,
    "application": False,
    "auto_install": False,
}
