# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import tools
from osv import fields,osv
from decimal_precision import decimal_precision as dp


class ovizio_report_stock_inventory(osv.osv):
    _name = "ovizio.report.stock.inventory"
    _description = "Ovizio Stock Statistics"
    _auto = False
    _columns = {
        'date': fields.datetime('Date', readonly=True),
        'partner_id':fields.many2one('res.partner.address', 'Partner', readonly=True),
        'supplier_id':fields.many2one('res.partner', 'Supplier', readonly=True),
        'product_id':fields.many2one('product.product', 'Product', readonly=True),
        'product_categ_id':fields.many2one('product.category', 'Product Category', readonly=True),
        'location_id': fields.many2one('stock.location', 'Location', readonly=True),
        'prodlot_id': fields.many2one('stock.production.lot', 'Lot', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', readonly=True),
        'product_qty':fields.float('Quantity',  digits_compute=dp.get_precision('Product UoM'), readonly=True),
        'price_unit' : fields.float('Unit Price',  digits_compute=dp.get_precision('Account'), required=True),
        'value' : fields.float('Total Value',  digits_compute=dp.get_precision('Account'), required=True),
        'state': fields.selection([('draft', 'Draft'), ('waiting', 'Waiting'), ('confirmed', 'Confirmed'), ('assigned', 'Available'), ('done', 'Done'), ('cancel', 'Cancelled')], 'State', readonly=True, select=True,
              help='When the stock move is created it is in the \'Draft\' state.\n After that it is set to \'Confirmed\' state.\n If stock is available state is set to \'Avaiable\'.\n When the picking it done the state is \'Done\'.\
              \nThe state is \'Waiting\' if the move is waiting for another one.'),
        'location_type': fields.selection([('supplier', 'Supplier Location'), ('view', 'View'), ('internal', 'Internal Location'), ('customer', 'Customer Location'), ('inventory', 'Inventory'), ('procurement', 'Procurement'), ('production', 'Production'), ('transit', 'Transit Location for Inter-Companies Transfers')], 'Location Type', required=True),
    }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'ovizio_report_stock_inventory')
        cr.execute("""
CREATE OR REPLACE view ovizio_report_stock_inventory AS (
    (SELECT
        min(m.id) as id, m.date as date,
        m.address_id as partner_id, m.location_id as location_id,
        m.product_id as product_id, pt.categ_id as product_categ_id, l.usage as location_type,
        m.company_id, m.price_unit as price_unit, m.partner_id as supplier_id,
        m.state as state, m.prodlot_id as prodlot_id,
        coalesce(sum(-m.price_unit * m.product_qty)::decimal, 0.0) as value,
        CASE when pt.uom_id = m.product_uom
        THEN
        coalesce(sum(-m.product_qty)::decimal, 0.0)
        ELSE
        coalesce(sum(-m.product_qty * pu.factor)::decimal, 0.0) END as product_qty
    FROM
        stock_move m
            LEFT JOIN stock_picking p ON (m.picking_id=p.id)
            LEFT JOIN product_product pp ON (m.product_id=pp.id)
                LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                LEFT JOIN product_uom pu ON (pt.uom_id=pu.id)
            LEFT JOIN product_uom u ON (m.product_uom=u.id)
            LEFT JOIN stock_location l ON (m.location_id=l.id)
    GROUP BY
        m.id, m.product_id, m.product_uom, m.price_unit, pt.categ_id, m.partner_id, m.address_id, m.location_id,  m.location_dest_id,
        m.prodlot_id, m.date, m.state, l.usage, m.company_id,pt.uom_id
) UNION ALL (
    SELECT
        -m.id as id, m.date as date,
        m.address_id as partner_id, m.location_dest_id as location_id,
        m.product_id as product_id, pt.categ_id as product_categ_id, l.usage as location_type,
        m.company_id, m.price_unit as price_unit, m.partner_id as supplier_id,
        m.state as state, m.prodlot_id as prodlot_id,
        coalesce(sum(m.price_unit * m.product_qty )::decimal, 0.0) as value,
        CASE when pt.uom_id = m.product_uom
        THEN
        coalesce(sum(m.product_qty)::decimal, 0.0)
        ELSE
        coalesce(sum(m.product_qty * pu.factor)::decimal, 0.0) END as product_qty
    FROM
        stock_move m
            LEFT JOIN stock_picking p ON (m.picking_id=p.id)
            LEFT JOIN product_product pp ON (m.product_id=pp.id)
                LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                LEFT JOIN product_uom pu ON (pt.uom_id=pu.id)
            LEFT JOIN product_uom u ON (m.product_uom=u.id)
            LEFT JOIN stock_location l ON (m.location_dest_id=l.id)
    GROUP BY
        m.id, m.product_id, m.product_uom, m.price_unit,  pt.categ_id, m.partner_id, m.address_id, m.location_id, m.location_dest_id,
        m.prodlot_id, m.date, m.state, l.usage, m.company_id,pt.uom_id
    )
);
        """)
ovizio_report_stock_inventory()


