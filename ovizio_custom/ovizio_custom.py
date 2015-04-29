#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from osv import osv, fields
from datetime import datetime
from datetime import timedelta

class crm_lead(osv.osv):
        
    _name = 'crm.lead'
    _inherit = 'crm.lead'
    _columns = {
        'need_demo': fields.boolean('Needed for Demo'),
        'demo_date': fields.date('Demo Date'),
        'demo_desc': fields.text('Demo Description'),
        'demo_state': fields.selection([('pending','Pending'),('inprogress','In Progress'),
            ('succesful','Succesful'),('failed','Failed')], 'Demo Status'),
    }
    _defaults = {
        'demo_state': 'pending',
    }

crm_lead()

class mrp_bom(osv.osv):

    _inherit = 'mrp.bom'

    def _cost_product_get(self, cr, uid, ids, name, args={}, context=None):
        boms = self.browse(cr, uid, ids)
        res= {}
        for bom in boms:
            res[bom.id] = bom.product_id.standard_price * bom.product_qty
        return res 

    _columns = { 
        'product_cost': fields.function(_cost_product_get, method=True, type='float', string='Cost'),
        'product_delay': fields.related('product_id', 'produce_delay', type='float', string='Delay'),
        'product_supplier': fields.related('product_id', 'supplier_id', type='many2one', relation="res.partner", string='Supplier', store=True),
        'product_supplier_id': fields.related('product_id', 'main_supplier_id', type='many2one', relation="res.partner", string='Supplier', store=True),
    }   

mrp_bom()

class sale_order(osv.osv):

    _inherit = "sale.order"

    _columns = {
        'date_validity': fields.date('Validity Date'),
    }

class sale_order_line(osv.osv):

    _inherit = 'sale.order.line'

    def _line_nbr_get(self, cr ,uid, ids, field_name, args, context=None):
        """get the line nunber"""
        if not context:
            context = {}
        result = {}
        l = []
        for line in self.browse(cr, uid, ids):
           l.append(line.id)
           l = sorted(l)
        for i in l:
           result[i] = l.index(i) + 1
        return result

    def _delivery_date_get(self, cr ,uid, ids, field_name, args, context=None):
        """get the line delivery date"""
        if not context:
            context = {}
        result = {}
        for line in self.browse(cr, uid, ids):
           if line.product_id:
                   order_date = datetime.strptime(line.order_id.date_order,  '%Y-%m-%d')
                   delivery_date = order_date + timedelta(days=line.product_id.sale_delay)
                   result[line.id] = delivery_date.strftime('%Y-%m-%d')
        return result

    _columns = {
        'line_nbr': fields.function(_line_nbr_get, type="integer", string='Number', store=False, readonly=True),
        'date_delivery': fields.function(_delivery_date_get, type="date", string='Delivery Date', store=False, readonly=True),
    }

class product_product(osv.osv):

    _inherit = 'product.product'

    def _get_main_supplier(self, cr ,uid, ids, field_name, args, context=None):
        """get the main supplier"""
        if not context:
            context = {}
        result = {}
        for prod in self.browse(cr, uid, ids):
            if prod.seller_ids:
                print "SELLER IDS:",prod.seller_ids
                result[prod.id] = prod.seller_ids[0].name.id
        print "RESULT:",result
        return result

    _columns = {
        'supplier_id': fields.function(_get_main_supplier, type="many2one", relation="res.partner", string="Main Supplier", store=True, readonly=False),
        'main_supplier_id': fields.many2one('res.partner', 'Main Supplier'),
        'critical': fields.boolean('Critical'),
    }

class res_partner(osv.osv):

    _inherit = 'res.partner'

    _columns = {
        'critical': fields.boolean('Critical'),
    }

    


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
