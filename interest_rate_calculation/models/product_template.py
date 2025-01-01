from odoo import api, fields, models, _
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Cause we can't create necessary Interest (service product) if sale_line_warn and purchase_line_warn are required.

    sale_line_warn = fields.Selection(WARNING_MESSAGE, 'Sales Order Line', help=WARNING_HELP, required=False,
                                      default="no-message")
    purchase_line_warn = fields.Selection(WARNING_MESSAGE, 'Purchase Order Line Warning', help=WARNING_HELP,
                                          required=False, default="no-message")