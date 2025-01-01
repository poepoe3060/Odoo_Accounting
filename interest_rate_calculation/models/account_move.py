import calendar
from datetime import datetime
from odoo import fields, models, _
from datetime import date
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    use_interest = fields.Boolean(string="Use Interest?", compute='_compute_over_due_date')
    over_due_date = fields.Boolean(string='Over Due Date?', compute='_compute_over_due_date')
    done_interest = fields.Boolean(string='Done Interest')

    def _compute_over_due_date(self):
        today = date.today()
        for rec in self:
            interest_rate = self.env["ir.config_parameter"].sudo().get_param("account_internal.interest_rate")
            if rec.move_type == 'out_invoice' and float(interest_rate) > 0.00:
                rec.use_interest = True
            else:
                rec.use_interest = False
            if rec.use_interest == True and today > rec.invoice_date_due:
                self.over_due_date = True
            else:
                self.over_due_date = False

    def action_generate_interest(self):
        today = datetime.now().date()
        current_year = datetime.now().year
        current_month = datetime.now().month
        for rec in self:
            if rec.over_due_date:
                interest_product_id = self.env.ref('interest_rate_calculation.product_interest_service_product_template').id
                product_id = self.env['product.product'].search([('product_tmpl_id', '=', interest_product_id)]).id
                interest_rate = self.env["ir.config_parameter"].sudo().get_param("account_internal.interest_rate")
                days_in_month = calendar.monthrange(current_year, current_month)[1]
                interest_day = today - rec.invoice_date_due
                interest_day_count = interest_day.days
                interest_price_unit = ((rec.amount_total * (float(interest_rate)/100)) / days_in_month) * interest_day_count

                self.invoice_line_ids.create({
                    'move_id': self.id,
                    'name': 'Interest',
                    'product_id':product_id,
                    'quantity':1,
                    'tax_ids': [],
                    'price_unit': round(interest_price_unit,2),
                    'price_subtotal': round(interest_price_unit,2),
                })

                rec.done_interest = True
            else:
                rec.done_interest = False

    def action_register_payment(self):
        res = super(AccountMove, self).action_register_payment()
        for rec in self:
            if rec.done_interest == False:
                raise UserError(_('Please, Interest must be generated!'))
        return res




