InvoiceMixIn = {

    mark_paid: ->
        @status = @STATUS_PAID
        @save()

    print: ->
        @status = @STATUS_TOBEPAID
        @save()
        window.open "/invoice/render/.pdf?doc_codename=INVOICE&id=#{@id}", "_blank"

    download: ->
        window.open "/invoice/render/.zip?doc_codename=INVOICEid=#{@id}"

}

window.mixin_include models.Invoice, InvoiceMixIn
window.mixin_include models.VatInvoice, InvoiceMixIn
window.mixin_include models.ProformaInvoice, InvoiceMixIn


class InvoiceItem extends models.InvoiceItem
    construct: ->
        super
        @gross_price = @compute_gross()

    compute_gross: =>
        @net_price * (100 + @tax) / 100
    
models.InvoiceItem = InvoiceItem
