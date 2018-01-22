import odoo.tests
from odoo.api import Environment


@odoo.tests.common.at_install(True)
@odoo.tests.common.post_install(True)
class TestUi(odoo.tests.HttpCase):

    def test_01_pos_is_loaded(self):
        # see more https://odoo-development.readthedocs.io/en/latest/dev/tests/js.html#phantom-js-python-tests
        env = Environment(self.registry.test_cr, self.uid, {})

        # get exist product
        box_product = env.ref('pos_product_lot.box')

        # Update Inventory
        inventory_wizard = env['stock.change.product.qty'].create({
            'product_id': box_product.id,
            'new_quantity': 5,
        })
        inventory_wizard.change_product_qty()

        self.phantom_js(
            '/web',

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".run('pos_product_lot_tour')",

            "odoo.__DEBUG__.services['web_tour.tour']"
            ".tours.pos_product_lot_tour.ready",

            login="admin",
            timeout=240,
        )
