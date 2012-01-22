class Invoice extends Spine.Controller
    constructor: ->
        super

    render: (item) =>
        if (item)
            @item = item
        tpl.load OFFICE_APP_NAME, 'inv_t', =>
            console.log @item
            @html tpl.render('inv_t', @item)
        @

class Invoices extends Spine.Controller
    constructor: ->
        super
        tpl.load OFFICE_APP_NAME, 'invoices', =>
            @replace tpl.render 'invoices', {}
        models.Invoice.fetch data: "status=#{@inv_status}"
        console.log "GWIAZDA"
        models.Invoice.bind("refresh",  @add_invoice)

    add_invoice: (items) =>
        (@append (new Invoice(item: item)).render() for item in items when item.status == @inv_status)

    render: (item) =>
        if (item)
            @item = item
        @replace render_tpl OFFICE_APP_NAME, 'invoices'
        @


class Index extends Spine.Controller
    constructor: ->
        @log "BAJKA"
        super
        tpl.load OFFICE_APP_NAME, 'index', =>
            @log "DUPA"
            @replace tpl.render 'index', {}
            @c1 = new Invoices inv_status: models.Invoice.STATUS_DRAFT, el: $ "#drafts"



window.controllers = {}
window.controllers.Index = Index
