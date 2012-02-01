InvoiceMixIn =
    mark_paid: ->
        @status = @.constructor.STATUS_PAID
        @save()

    print: ->
        if @status not in [@.constructor.STATUS_PAID, @.constructor.STATUS_TOBEPAID]
            @status = @.constructor.STATUS_TOBEPAID
            @save()
        inv = @
        tpl.load OFFICE_APP_NAME, 'print_dialog', =>
            $('<div />').html(tpl.render 'print_dialog', {}).dialog
                'title': 'Drukuj fakturę',
                'draggable': false,
                'modal': true,
                'resizable': false,
                'buttons':
                    'Zamknij': ->
                        $(@).dialog 'close'
                    'Drukuj': ->
                        types = $('#print_types_choice input[type=radio]:checked').val()
                        types = types.split(',').join('&types=')
                        lang = $('#print_lang_choice input[type=radio]:checked').val()
                        window.open "/invoice/render/.pdf?doc_codename=INVOICE&id=#{inv.id}&types=#{types}&lang=#{lang}", "_blank"
                        $(@).dialog 'close'

    download: ->
        window.open "/invoice/render/.zip?doc_codename=INVOICE&id=#{@id}"

window.mixin_include models.Invoice, InvoiceMixIn
window.mixin_include models.VatInvoice, InvoiceMixIn
window.mixin_include models.ProformaInvoice, InvoiceMixIn

window.mixin_include models.ProformaInvoice,
    into_vat: (cb) ->
        $.get "/invoice/profintovat/#{@id}", (data) =>
            cb(data)

class InvoiceItem extends models.InvoiceItem
    construct: ->
        super
        @gross_price = @compute_gross()

    compute_gross: =>
        @net_price * (100 + @tax) / 100
    
models.InvoiceItem = InvoiceItem
