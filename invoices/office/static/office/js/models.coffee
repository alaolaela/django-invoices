class InvoiceItem extends models.InvoiceItem
    construct: ->
        super
        @gross_price = @compute_gross()

    compute_gross: =>
        @net_price * (100 + @tax) / 100
    
models.InvoiceItem = InvoiceItem
