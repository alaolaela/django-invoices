InvoiceMixIn =
    mark_paid: =>
        @status = @.constructor.STATUS_PAID
        @save()

    print: =>
        @status = @.constructor.STATUS_TOBEPAID
        @save()
        window.open "/invoice/render/.pdf?doc_codename=INVOICE&id=#{@id}", "_blank"

    download: =>
        window.open "/invoice/render/.zip?doc_codename=INVOICE&id=#{@id}"

window.mixin_include models.Invoice, InvoiceMixIn
window.mixin_include models.VatInvoice, InvoiceMixIn
window.mixin_include models.ProformaInvoice, InvoiceMixIn

window.mixin_include models.ProformaInvoice,
    into_vat: =>
        console.log('a')
        @status = @STATUS_TOBEPAID
        @key = null
        @save()


class InvoiceItem extends models.InvoiceItem
    construct: ->
        super
        @gross_price = @compute_gross()

    compute_gross: =>
        @net_price * (100 + @tax) / 100
    
models.InvoiceItem = InvoiceItem
