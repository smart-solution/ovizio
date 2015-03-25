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
ids = sock.execute(dbname, uid, pwd, 'product.product', 'search', []) 

a_datas = sock.execute(dbname, uid, pwd, 'product.product', 'read', ids, ['qty_available'])
print "A_DATAS:",a_datas

to_unactive = []
for a_data in a_datas:
    if a_data['qty_available'] == 0:
        to_unactive.append(a_data['id'])
        print a_data
sock.execute(dbname, uid, pwd, 'product.product', 'write', to_unactive, {'active':False})

