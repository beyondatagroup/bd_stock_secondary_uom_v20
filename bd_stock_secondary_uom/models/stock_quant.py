# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    secondary_uom_id = fields.Many2one(
        related="product_id.secondary_uom_id",
        string="Secondary UoM",
        readonly=True,
    )

    secondary_qty = fields.Float(
        string="On Hand (Secondary)",
        compute="_compute_secondary_qty",
        readonly=True,
    )

    @api.depends("quantity", "product_id", "secondary_uom_id")
    def _compute_secondary_qty(self):
        for quant in self:
            quant.secondary_qty = 0.0

            if quant.product_id and quant.secondary_uom_id and quant.uom_id:
                try:
                    quant.secondary_qty = quant.uom_id._compute_quantity(
                        quant.quantity,
                        quant.secondary_uom_id,
                        raise_if_failure=False,
                    )
                except Exception:
                    quant.secondary_qty = 0.0
