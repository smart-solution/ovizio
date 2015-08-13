# -*- coding: utf-8 -*-
##############################################################################
#
#    Smart Solution bvba
#    Copyright (C) 2010-Today Smart Solution BVBA (<http://www.smartsolution.be>).
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

from openerp.osv import orm, fields
from openerp.tools.translate import _

class stock_production_lot(orm.Model):

    _inherit = "stock.production.lot"

    def _location_get(self, cr, uid, ids, field_name, args, context=None):
        """Get the last assigned destination address for that producion lot"""
        result = {}

        lots = self.browse(cr, uid, ids)
        for lot in lots:
            lot_quants = self.pool.get('stock.quant').search(cr, uid, [('lot_id','in',[lot.id])])
            lot_moves = self.pool.get('stock.move').search(cr, uid, [('quant_ids','in',lot_quants)])

            if lot_moves:
                result[lot.id] = self.pool.get('stock.move').browse(cr, uid, max(lot_moves)).location_dest_id.id
            else:
                result[lot.id] = False
        return result

    _columns = { 
            'last_location_id': fields.function(_location_get, method=True, type='many2one', relation='stock.location', readonly=True, string="Location"),
    }   

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
