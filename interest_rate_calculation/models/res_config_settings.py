from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    is_interest = fields.Boolean( string="Is Interest", readonly=False, config_parameter='account_internal.is_interest')
    interest_rate = fields.Float(string="Interest Rate", readonly=False, config_parameter='account_internal.interest_rate')



