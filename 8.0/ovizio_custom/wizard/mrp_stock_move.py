#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
##############################################################################

from openerp.osv import osv, fields
from openerp.tools.translate import _

class wizard_mrp_stock_move(osv.TransientModel):

    _name = 'wizard.mrp.stock.move'

    def stock_move_get(self, cr, uid, ids, context=None):
        """Get products to consume stock moves for a manufacturing order"""

        mod_obj = self.pool.get('ir.model.data')
        mo = self.pool.get('mrp.production').browse(cr, uid, context['active_id'])
        stock_move_ids = [move.id for move in mo.move_lines]

        try:
            tree_view_id = mod_obj.get_object_reference(cr, uid, 'stock', 'view_move_tree')[1]
        except ValueError:
            tree_view_id = False
        try:
            form_view_id = mod_obj.get_object_reference(cr, uid, 'stock', 'view_move_form')[1]
        except ValueError:
            form_view_id = False

        return {'name': _('Products to Consume'),
                'context': context,
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'stock.move',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'type': 'ir.actions.act_window',
                'domain': [('id','in',stock_move_ids)]
        }



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
