# -*- coding: utf-8 -*-
import time
import base64
import xmlrpclib

server='localhost'
dbname='ovizio'
uid=1
pwd='ovizio?123'
model = 'product.product'


#replace localhost with the address of the server
sock = xmlrpclib.ServerProxy('http://%s:8069/xmlrpc/object'%(server))
ids = sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'search', []) 

a_datas = sock.execute(dbname, uid, pwd, 'product.supplierinfo', 'read', ids, ['name','product_id'])
print "A_DATAS:",a_datas

for a_data in a_datas:
    sock.execute(dbname, uid, pwd, 'product.product', 'write', [a_data['product_id'][0]], {'main_supplier_id':a_data['name'][0]})

