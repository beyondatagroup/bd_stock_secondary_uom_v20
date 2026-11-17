# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_secondary_unit = fields.Boolean(
        string="Use Secondary Unit",
        help="Enable a secondary unit of measure for this product."
    )

    secondary_uom_id = fields.Many2one(
        "uom.uom",
        string="Secondary Unit of Measure",
        help="Select the secondary unit of measure. It must belong to the same UoM category as the primary Unit of Measure."
    )

    @api.constrains("is_secondary_unit")
    def _check_secondary_uom_setting(self):
        for product in self:
            if product.is_secondary_unit and not self.env.user.has_group("uom.group_uom"):
                raise ValidationError(_(
                    "Please enable 'Units of Measure & Packagings' in Inventory Settings before using Secondary Unit of Measure."
                ))


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_secondary_unit = fields.Boolean(
        related="product_tmpl_id.is_secondary_unit",
        readonly=False,
    )

    secondary_uom_id = fields.Many2one(
        "uom.uom",
        related="product_tmpl_id.secondary_uom_id",
        readonly=False,
    )