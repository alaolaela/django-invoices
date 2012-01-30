class GrossComputation
    compute_gross: =>
        @net_price * (1 + @tax  / 100)
    
mixin_include models.VatInvoice, GrossComputation
mixin_include models.ProformaInvoice, GrossComputation
