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
    constructor: ->
        super
        tpl.load OFFICE_APP_NAME, 'index', =>
            @replace tpl.render 'index', {}
            controller_names = [
                [models.Invoice.STATUS_DRAFT, 'drafts'],
                [models.Invoice.STATUS_TOBEPAID, 'tobepaid'],
                [models.Invoice.STATUS_PAID, 'paid'],
                [models.Invoice.STATUS_OVERDUE, 'overdue']
            ]
            @controlles = ((new Invoices inv_status: record[0], el: $("##{record[1]} table tbody")) for record in controller_names)
            console.log controlles



window.controllers = {}
window.controllers.Index = Index
