class Invoice extends Spine.Controller
    tag: 'tr'

    constructor: ->
        super

    render: (item) =>
        if (item)
            @item = item
        tpl.load OFFICE_APP_NAME, 'inv_t', =>
            @html tpl.render('inv_t', @item)
        @

class Invoices extends Spine.Controller
    constructor: ->
        super
        models.Invoice.fetch data: "status=#{@inv_status}"
        models.Invoice.bind("refresh",  @add_invoice)

    add_invoice: (items) =>
        filterted_items = ((new Invoice(item: item)).render() for item in items when item.status == @inv_status)
        if filterted_items.length
            @html ''
            (@append a for a in filterted_items)


class Index extends Spine.Controller
    #elements:
    
    events:
        "click div": "click"

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
                console.log "KLAMSTWO", text, invoice_status
                if invoice_status == models.Invoice.STATUS_PAID
                    ''
                else
                    text
            @replace tpl.render 'index', {blocks: ({type: c[0], id: c[1], name: c[2], 'paid_action': (text) -> paid_action(c[0], text)} for c in controller_names)}
            @controllers = ((new Invoices inv_status: record[0], el: $("##{record[1]} table tbody")) for record in controller_names)



window.controllers = {}
window.controllers.Index = Index
