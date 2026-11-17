# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    secondary_uom_id = fields.Many2one(
        "uom.uom",
        string="Secondary UoM",
        compute="_compute_secondary_uom",
        store=True,
        readonly=False,
        precompute=True,
    )

    secondary_qty = fields.Float(
        string="Secondary Qty",
        compute="_compute_secondary_qty",
        store=True,
        readonly=False,
    )

    secondary_done_qty = fields.Float(
        string="Secondary Done Qty",
        compute="_compute_secondary_done_qty",
        store=True,
        readonly=False,
    )

    allowed_secondary_uom_id = fields.Many2one(
        "uom.uom",
        compute="_compute_allowed_secondary_uom",
        store=False,
    )

    @api.depends("product_id", "product_id.product_tmpl_id.secondary_uom_id")
    def _compute_allowed_secondary_uom(self):
        for line in self:
            line.allowed_secondary_uom_id = (
                line.product_id.product_tmpl_id.secondary_uom_id
                if line.product_id
                else False
            )

    # ==========================================================
    # Secondary UoM
    # ==========================================================

    @api.depends("product_id")
    def _compute_secondary_uom(self):
        """
        Automatically fetch Secondary UoM from Product.
        Works for:
            • Direct Receipt
            • Delivery Order
            • Internal Transfer
            • Scrap
            • Purchase Order
            • Sale Order
            • Manufacturing
        """
        for move in self:
            if move.product_id:
                template = move.product_id.product_tmpl_id
                if template.is_secondary_unit and template.secondary_uom_id:
                    move.secondary_uom_id = template.secondary_uom_id
                else:
                    move.secondary_uom_id = False
            else:
                move.secondary_uom_id = False

    # Secondary Demand Qty
    @api.depends(
        "product_uom_qty",
        "quantity",
        "is_scrap",
        "uom_id",
        "secondary_uom_id",
    )
    def _compute_secondary_qty(self):
        for move in self:
            qty = move.quantity if (move.is_scrap and not move.product_uom_qty) else move.product_uom_qty
            if (
                move.uom_id
                and move.secondary_uom_id
                and qty
            ):
                move.secondary_qty = move.uom_id._compute_quantity(
                    qty,
                    move.secondary_uom_id,
                    raise_if_failure=False,
                )
            else:
                move.secondary_qty = 0.0

    # Secondary Done Qty
    @api.depends(
        "quantity",
        "uom_id",
        "secondary_uom_id",
    )
    def _compute_secondary_done_qty(self):
        for move in self:
            if (
                move.uom_id
                and move.secondary_uom_id
                and move.quantity
            ):
                move.secondary_done_qty = move.uom_id._compute_quantity(
                    move.quantity,
                    move.secondary_uom_id,
                    raise_if_failure=False,
                )
            else:
                move.secondary_done_qty = 0.0

    # Onchange
    @api.onchange("product_id")
    def _onchange_product_id_secondary_uom(self):
        """
        Immediate update while selecting product
        in Receipt/Delivery form and Scrap form.
        """
        for move in self:
            if move.product_id:
                template = move.product_id.product_tmpl_id
                if template.is_secondary_unit and template.secondary_uom_id:
                    move.secondary_uom_id = template.secondary_uom_id
                else:
                    move.secondary_uom_id = False
            else:
                move.secondary_uom_id = False

    @api.onchange("quantity", "secondary_uom_id", "uom_id")
    def _onchange_quantity_secondary_uom(self):
        """Immediate update of secondary done quantity on scrap or transfer."""
        for move in self:
            if move.uom_id and move.secondary_uom_id and move.quantity:
                move.secondary_done_qty = move.uom_id._compute_quantity(
                    move.quantity,
                    move.secondary_uom_id,
                    raise_if_failure=False,
                )

    # Create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("product_id") and not vals.get("secondary_uom_id"):
                product = self.env["product.product"].browse(vals["product_id"])
                template = product.product_tmpl_id

                if template.is_secondary_unit and template.secondary_uom_id:
                    vals["secondary_uom_id"] = template.secondary_uom_id.id

        moves = super().create(vals_list)

        # Recompute secondary quantity
        for move in moves:
            if move.uom_id and move.secondary_uom_id:
                qty = move.quantity if (move.is_scrap and not move.product_uom_qty) else move.product_uom_qty
                move.secondary_qty = move.uom_id._compute_quantity(
                    qty,
                    move.secondary_uom_id,
                    raise_if_failure=False,
                )

                move.secondary_done_qty = move.uom_id._compute_quantity(
                    move.quantity,
                    move.secondary_uom_id,
                    raise_if_failure=False,
                )

        return moves

    def write(self, vals):
        res = super().write(vals)

        if "product_uom_qty" in vals or "quantity" in vals or "uom_id" in vals or "secondary_uom_id" in vals:
            for move in self:
                if move.uom_id and move.secondary_uom_id:
                    qty = move.quantity if (move.is_scrap and not move.product_uom_qty) else move.product_uom_qty
                    move.secondary_qty = move.uom_id._compute_quantity(
                        qty,
                        move.secondary_uom_id,
                        raise_if_failure=False,
                    )

                    move.secondary_done_qty = move.uom_id._compute_quantity(
                        move.quantity,
                        move.secondary_uom_id,
                        raise_if_failure=False,
                    )

        return res


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    secondary_qty = fields.Float(
        related="move_id.secondary_qty",
        string="Secondary Qty",
        store=True,
        readonly=True,
    )

    secondary_done_qty = fields.Float(
        related="move_id.secondary_done_qty",
        string="Secondary Done Qty",
        store=True,
        readonly=True,
    )

    secondary_uom_id = fields.Many2one(
        "uom.uom",
        related="move_id.secondary_uom_id",
        string="Secondary UoM",
        store=True,
        readonly=True,
    )

    def _get_aggregated_product_quantities(self, **kwargs):
        result = super()._get_aggregated_product_quantities(**kwargs)

        for key, values in result.items():
            move = values.get("move")
            if not move:
                move = self.filtered(
                    lambda ml:
                        ml.product_id == values.get("product") and
                        ml.uom_id == values.get("uom_id")
                )[:1].move_id

            if move:
                values["secondary_qty"] = move.secondary_done_qty or move.secondary_qty
                values["secondary_uom"] = move.secondary_uom_id

        return result
