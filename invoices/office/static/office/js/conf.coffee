conf = {}

conf.INVOICE_TYPE_VAT = 1
conf.INVOICE_TYPE_PROFORMA = 2

conf.INVOICE_TYPES =
    vat: conf.INVOICE_TYPE_VAT
    proforma: conf.INVOICE_TYPE_PROFORMA

conf.INVOICE_MODELS = {}
conf.INVOICE_MODELS[conf.INVOICE_TYPE_VAT] = 'VatInvoice'
conf.INVOICE_MODELS[conf.INVOICE_TYPE_PROFORMA] = 'ProformaInvoice'

conf.INVOICE_ADD_INFO_ADDR = '/invoice/additionalinfo/'

window.conf = conf
