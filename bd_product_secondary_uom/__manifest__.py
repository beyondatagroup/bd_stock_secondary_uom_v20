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
    "name": "Product Secondary Unit of Measure",
    'version': '20.0.1.0.0',
    "category": "Inventory",
    "summary": "Manage secondary units of measure for products and transactions.",
    "description": """
        Product Secondary Unit of Measure
        =================================
        
        This module allows you to configure and use a Secondary Unit of Measure
        for products across Sales, Purchases, Inventory, and related operations.
        
        Features
        --------
        * Configure Secondary Unit of Measure on products.
        * Define conversion ratio between primary and secondary UoM.
        * Automatically calculate quantities in secondary UoM.
        * Support Sales Orders.
        * Support Purchase Orders.
        * Support Inventory Transfers.
        * Easy configuration and user-friendly interface.
        * Compatible with Odoo 20.
        
        """,
    "author": "BeyonData Solutions Private Limited",
    "website": "https://www.beyondatagroup.com",
    "license": "OPL-1",
    "depends": [
        "base",
        "stock",
    ],
    "data": [
        "security/groups.xml",

        # Views
        "views/product_template_views.xml",
    ],
    "images": [
        "static/description/banner.gif",
    ],

    "price": "9.99",
    "currency": "EUR",

    "installable": True,
    "application": False,
    "auto_install": False,
}
