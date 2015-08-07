#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##############################################################################
#
#
##############################################################################
{
    "name" : "ovizio_custom",
    "version" : "1.0",
    "author" : "SmartSolution",
    "category" : "Generic Modules/Base",
    "description": """
    Ovizio Customization module
""",
    "depends" : ["account","purchase","crm_claim","mrp","stock"],
    "init_xml" : [
        ],
    "update_xml" : [
        'ovizio_custom_view.xml',
        'wizard/mrp_stock_move_view.xml',
        'ovizio_custom_report.xml',
#        'report_inventory_analysis_view.xml',
        'ovizio_custom_data.xml',
#        'security/ir.model.access.csv'
        ],
    "active": False,
    "installable": True
}
