# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'FBB Professional Report',
    'version': '1.0',
    'summary': '定制报告 报表模版',
    'category': 'Tools',
    'description': """
		定制报告,定制pdf报告,报告定制模板,自定义销售订单报告,
		定制采购订单报告,发票定制报告,定制交付订单报告,会计报告,简单的报告,灵活的报告,报告模板.
		
    """,
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    'depends': ['base', 'account', 'sale', 'purchase', 'stock', 'sale_stock', 'base_vat'],
    'data': [
		"res_company.xml",
		"invoice_report/fency_report_account.xml",
		"invoice_report/fency_report_invoice.xml",
		"invoice_report/report_invoice_classic.xml",
		"invoice_report/report_invoice_modern.xml",
"invoice_report/report_invoice_odoo_standard.xml",

"delivery_report/stock_report_classic.xml",
"delivery_report/fency_report_deliveryslip.xml",
"delivery_report/modern_report_deliveryslip.xml",
"delivery_report/odoo_standard_report_deliveryslip.xml",
"delivery_report/report_deliveryslip_classic.xml",

"purchase_report/classic_purchase_report.xml",
"purchase_report/classic_report_purchaseorder.xml",
"purchase_report/classic_report_purchasequotation.xml",
"purchase_report/fency_report_purchaseorder.xml",
"purchase_report/fency_report_purchasequotation.xml",
"purchase_report/modern_report_purchaseorder.xml",
"purchase_report/modern_report_purchasequotation.xml",
"purchase_report/odoo_standard_report_purchaseorder.xml",
"purchase_report/odoo_standard_report_purchasequotation.xml",

"sale_report/classic_sale_report.xml",
"sale_report/classic_report_saleorder.xml",
"sale_report/fency_report_saleorder.xml",
"sale_report/modern_report_saleorder.xml",
"sale_report/odoo_standard_report_saleorder.xml",
             ],
	'qweb': [
		],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    "images":['static/description/Banner.png'],
}
