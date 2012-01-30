class Invoice extends Spine.Controller
    tag: 'tr'

    constructor: ->
        super
        @item.bind("destroy", @remove)
        @item.bind("change", @change)
        @item.bind("change-local", @change)
    
    render: (item) =>
        if (item)
            @item = item
        tpl.load OFFICE_APP_NAME, 'inv_t', =>
            @html tpl.render 'inv_t', 
                item: @item
                type: @item.constructor.TYPE
                verbose_name: @item.constructor.VERBOSE_NAME
        @

    remove: =>
        @el.remove()

    change: (inv) =>
        @render(inv)

class Invoices extends Spine.Controller
    constructor: ->
        super
        models.VatInvoice.fetch data: "status=#{@inv_status}"
        models.ProformaInvoice.fetch data: "status=#{@inv_status}"
        models.VatInvoice.bind("refresh", (items) => @add_invoice(items, models.VatInvoice))
        models.ProformaInvoice.bind("refresh", (items) => @add_invoice(items, models.ProformaInvoice))

    add_invoice: (items, model_cls) =>
        filterted_items = ((new Invoice(item: item)).render() for item in items when item.status == @inv_status)
        if not filterted_items.length
            return
        items_ids = (item.id for item in items  when item.status == @inv_status)
        $.get conf.INVOICE_ADD_INFO_ADDR + items_ids.join(','), (data) =>
                for inv_id, gross_price of data
                    inv = model_cls.find(inv_id)
                    inv.gross_price = gross_price.toFixed 2
                    inv.trigger('change-local', inv)
            ,'json'
        for a in filterted_items
            if @el.find("#invoice-#{a.item.constructor.TYPE}-#{a.item.id}").length
                continue
            @append a

    delete: =>
        for check in @el.find("input:checked")
            $(check).parent().item().destroy()

    print: =>
        ids = ""
        checks = @el.find("input:checked")
        ext = if checks.length > 1 then 'zip' else 'pdf'
        for check in checks
            id = $(check).parent().item().item.id
            ids = "#{ids}&id=#{id}"
        # It is possible to open multiple tabs instead of zip, just call x times window.open with _blank
        window.open "/invoice/print/.#{ext}?doc_codename=INVOICE#{ids}", "_blank"


class Index extends Spine.Controller
    events:
        "click input.delete": "delete_invoice"
        "click input.print": "print_invoice"

    constructor: ->
        super
        tpl.load OFFICE_APP_NAME, 'index', =>
            controller_names = [
                [models.Invoice.STATUS_DRAFT, 'drafts', 'Szkice'],
                [models.Invoice.STATUS_TOBEPAID, 'tobepaid', 'Do zapłacenia'],
                [models.Invoice.STATUS_PAID, 'paid', 'Zapłacone'],
                [models.Invoice.STATUS_OVERDUE, 'overdue', 'Przeterminowane']
            ]
            paid_action = (invoice_status, text) ->
                if invoice_status == models.Invoice.STATUS_PAID
                    ''
                else
                    text
            @el.find('.left').html tpl.render 'index', {blocks: ({type: c[0], id: c[1], name: c[2], 'paid_action': (text) -> paid_action(c[0], text)} for c in controller_names)}
            @controllers = {}
            (@controllers[record[0]] = (new Invoices inv_status: record[0], el: $("##{record[1]} table tbody")) for record in controller_names)

        tpl.load OFFICE_APP_NAME, 'index_right', =>
            @el.find('.right').html tpl.render 'index_right', {}


    delete_invoice: (e) =>
        @controllers[$(e.target).data('ref')].delete()

    
    print_invoice: (e) =>
        @controllers[$(e.target).data('ref')].print()
    

class InvoicePreview extends Spine.Controller
    constructor: ->
        super
        tpl.load OFFICE_APP_NAME, 'preview', =>
            @el.find('.left').html tpl.render 'preview', {}
        tpl.load OFFICE_APP_NAME, 'preview_right', =>
            @el.find('.right').html tpl.render 'preview_right', {}


window.controllers = {}
window.controllers.Index = Index
window.controllers.InvoicePreview = InvoicePreview
