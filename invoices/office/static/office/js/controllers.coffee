class Invoice extends Spine.Controller
    tag: 'tr'

    constructor: ->
        super
        @item.bind("destroy", @remove)
    
    render: (item) =>
        if (item)
            @item = item
        tpl.load OFFICE_APP_NAME, 'inv_t', =>
            @html tpl.render('inv_t', @item)
        @

    remove: =>
        @el.remove()

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

    delete: =>
        for check in @el.find("input:checked")
            $(check).parent().item().destroy()


class Index extends Spine.Controller
    #elements:
    
    events:
        "click input.delete": "delete_invoice"

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
        console.log e
        @controllers[$(e.target).data('ref')].delete()


class InvoiceAddition extends Spine.Controller
    INVOICES_TPL_ADDR: '/invoices/formtpl/'
    CHOICES_ADDR: '/invoices/choices/'
    PRODUCTS_SEARCH_ADDR: '/invoices/products/'

    events:
        "change #id_customer_content_type": "customer_type_chosen"

    constructor: ->
        super
        tpl.load OFFICE_APP_NAME, 'add', =>
            @el.find('.left').html tpl.render 'add', {}
            @load_tpl()

    load_tpl: =>
        $.get @INVOICES_TPL_ADDR, (data) =>
            @el.find('form.facture').html data
            $("#id_date_sale, #id_date_created, #id_date_payment").datepicker
                showOn: "button"
                buttonImage: "#{STATIC_URL}office/css/images/calendar.png"
                buttonImageOnly: true

            prod_addr = @PRODUCTS_SEARCH_ADDR
            $('.commodity textarea').each ->
                txta = $(@)
                txta.autocomplete 'source': prod_addr, 'select': (e, ui) ->
                    if ui.item
                        txta.data('ct_id', ui.item.ct_id).data('obj_id', ui.item.obj_id)
                    else
                        txta.data('ct_id', None).data('obj_id', None)
		
            @refreshElements()

    customer_type_chosen: (e) =>
        sel_el = $(e.target)
        ct_id = sel_el.val()
        $.get "#{@CHOICES_ADDR}#{ct_id}/", (data) =>
            console.log data
            sel_customer = $ '#id_customer_object_id'
            sel_customer.html ''
            for rec in data
                new_opt = $('<option />',
                    value: rec[1]
                    text: rec[0]
                )
                sel_customer.append new_opt

        , 'json'
            

window.controllers = {}
window.controllers.Index = Index
window.controllers.InvoiceAddition = InvoiceAddition
