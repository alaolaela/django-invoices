class ComputeValue
    constructor: (@el, @invoice_items) ->

    input_val: (row, a) ->
        pf = parseFloat
        inp_val = row.find(".#{a} input, .#{a} select").val()
        if inp_val
            pf(inp_val)
        else
            span_el = row.find(".#{a} span")
            if span_el.length
                pf span_el.text()
            else
                0

    compute_values: (e) =>
        el = $(e.target)
        if not (el.val() or el.text())
            return
        p = el.parent()
        row = el.parents('tr').eq(0)
        f = (a) => @input_val(row, a)
        quantity = f 'quantity'
        net_price = f 'net_price'
        net_value = f 'net_value'
        tax = f 'tax'
        if p.hasClass 'net_value'
            if quantity
                net_price = (net_value / quantity)
        sf = (a, b) ->
            if row.find(".#{a} input").length
                row.find(".#{a} input").val b
            else
                row.find(".#{a} span").text b
        net_value = quantity * net_price
        sf 'net_value', net_value.toFixed 2
        sf 'net_price', net_price.toFixed 2
        sf 'quantity', quantity.toFixed 2
        sf 'taxval', (tax / 100 * net_value).toFixed 2
        sf 'gross', ((1 + tax / 100) * net_value).toFixed 2
        @compute_summary()

    compute_summary: (e) =>
        net_sum = 0
        tax_sum = 0
        gross_sum = 0
        tax_sum_tpl =
            net_sum: 0
            tax_sum: 0
            gross_sum: 0
        tax_sum_classes = {}

        f = @input_val
        for row in @invoice_items.find('tr:visible')
            row = $ row
            net_sum += f row, 'net_value'
            tax_sum += f row, 'taxval'
            gross_sum += f row, 'gross'
            tax = f row, 'tax'
            
            if not tax_sum_classes.hasOwnProperty tax
                tax_sum_classes[tax] = _.clone(tax_sum_tpl)
            tax_sum_classes[tax].net_sum += f row, 'net_value'
            tax_sum_classes[tax].tax_sum += f row, 'taxval'
            tax_sum_classes[tax].gross_sum += f row, 'gross'
        tf = (a) -> a.toFixed 2
        @el.find('.whole_sum .net_sum').text(tf net_sum)
        @el.find('.whole_sum .tax_sum').text(tf tax_sum)
        @el.find('.whole_sum .gross_sum').text(tf gross_sum)
        @el.find('tr.tax_class_sum').remove()
        for own tax, sum of tax_sum_classes
            new_tr = $ '<tr />',
                class: 'tax_class_sum'
            new_tr.html $('.tax_class_sum_tpl').html()
            new_tr.find('.tax_class').text(tax)
            new_tr.find('.net_sum').text(tf sum.net_sum)
            new_tr.find('.tax_sum').text(tf sum.tax_sum)
            new_tr.find('.gross_sum').text(tf sum.gross_sum)
            $('.total_cost').before new_tr
        @el.find('.tax_class_sum').eq(0).find('.label').css 'visibility', 'visible'
        $('.total_cost p span').text(tf gross_sum)

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
        tpl.load OFFICE_APP_NAME, @inv_tpl, =>
            @html tpl.render @inv_tpl,
                item: @item
                type: @item.constructor.TYPE
                verbose_name: @item.constructor.VERBOSE_NAME
            @item.constructor.trigger('item-rendered')
        @

    remove: =>
        @item.unbind("destroy", @remove)
        @item.unbind("change", @change)
        @item.unbind("change-local", @change)
        @el.remove()

    change: (inv) =>
        @render(inv)

class Invoices extends Spine.Controller
    constructor: ->
        super
        if @inv_query
            inv_filter = "#{@inv_query}=#{@inv_param}"
            models.VatInvoice.fetch data: inv_filter
            models.ProformaInvoice.fetch data: inv_filter
        else
            models.VatInvoice.fetch()
            models.ProformaInvoice.fetch()

        models.VatInvoice.bind("refresh", @vat_callback)
        models.ProformaInvoice.bind("refresh", @prof_callback)
        models.VatInvoice.bind("change", @vat_callback_c)
        models.ProformaInvoice.bind("change", @prof_callback_c)
        models.VatInvoice.bind("item-rendered", @compute_total)
        models.ProformaInvoice.bind("item-rendered", @compute_total)
        @invoiceids = []

    prof_callback: (items) =>
        @add_invoice(items, models.ProformaInvoice)

    vat_callback: (items) =>
        @add_invoice(items, models.VatInvoice)

    prof_callback_c: (items) =>
        @invoice_changed(items, models.ProformaInvoice)

    vat_callback_c: (items) =>
        @invoice_changed(items, models.VatInvoice)

    add_invoice: (items, model_cls) =>
        if not items.length
            return
        filterted_items = ((new Invoice(item: item, inv_tpl: @inv_tpl)).render() for item in items when @filter_function(item, @inv_param) and not item.destroyed)
        if not filterted_items.length
            return
        items_ids = (item.id for item in items  when  @filter_function(item, @inv_param))
        $.get conf.INVOICE_ADD_INFO_ADDR + items_ids.join(','), (data) =>
                for inv_id, add_info of data
                    gross_price = add_info.gross_price
                    inv = model_cls.find(inv_id)
                    inv.gross_price = gross_price.toFixed 2
                    inv.get_status_display = add_info.get_status_display
                    inv.customer_name = add_info.customer_name
                    inv.trigger('change-local', inv)
            ,'json'
        for a in filterted_items
            if a.item.id in @invoiceids
                continue
            @invoiceids.push a.item.id
            if @el.find("#invoice-#{a.item.constructor.TYPE}-#{a.item.id}").length
                continue
            @append a
    
    invoice_changed: (item, model_cls) =>
        @invoiceids = []
        if not @filter_function(item, @inv_param)
            @el.find("#invoice-#{item.constructor.TYPE}-#{item.id}").parent().remove()
        else
            @add_invoice([item], model_cls)
    
    release: (fun) =>
        super
        models.VatInvoice.unbind("refresh", @vat_callback)
        models.ProformaInvoice.unbind("refresh", @prof_callback)
        models.VatInvoice.unbind("change", @vat_callback_c)
        models.ProformaInvoice.unbind("change", @prof_callback_c)
        models.VatInvoice.unbind "item-rendered", @compute_total
        models.ProformaInvoice.unbind "item-rendered", @compute_total

    compute_total: =>
        sum = 0
        for row in @el.find('tr')
            val = $(row).find('.gross_value-column span').text()
            if not val
                continue
            sum += parseFloat val
        @el.parents('.overview').next().find('.total_gross_value').text sum.toFixed 2
            

    delete: =>
        @iterate_checked (item) =>
            item.item.constructor.find(item.item.id).destroy()

    print: =>
        @iterate_checked (item) =>
            item.item.print()

    download: =>
        ids = []
        @iterate_checked (item) =>
            ids.push item.item.id
        window.open "/invoices/render/.zip?doc_codename=INVOICE&id=#{ids.join('&id=')}"

    mark_as_paid: =>
        @iterate_checked (item) =>
            item.item.mark_paid()

    iterate_checked: (func) =>
        checks = @el.find('input:checked')
        for check in checks
            func $(check).parent().item()

class Index extends Spine.Controller
    events:
        "click input.delete": "delete_invoice"
        "click input.print": "print_invoice"
        "click input.mark_as_paid": "mark_invoice_as_paid"
        "click input.download": "download_invoice"

    init_controller: =>
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
            filter_items = (item, param) -> item.status == param
            for record in controller_names
                inv_con = new Invoices
                    filter_function: filter_items
                    inv_param: record[0]
                    el: $("##{record[1]} table tbody")
                    inv_query: 'status'
                    inv_tpl: 'inv_t'
                @controllers[record[0]] = inv_con


        tpl.load OFFICE_APP_NAME, 'index_right', =>
            @el.find('.right').html tpl.render 'index_right', {}

    release: (fun) =>
        super
        for id, controller of @controllers
            controller.release()

    delete_invoice: (e) =>
        @controllers[$(e.target).data('ref')].delete()

    print_invoice: (e) =>
        @controllers[$(e.target).data('ref')].print()

    download_invoice: (e) =>
        @controllers[$(e.target).data('ref')].download()

    mark_invoice_as_paid: (e) =>
        @controllers[$(e.target).data('ref')].mark_as_paid()
    
class AllInvoices extends Spine.Controller
    constructor: ->
        super

class TypeInvoices extends Index
    constructor: ->
        super
        tpl.load OFFICE_APP_NAME, 'index', =>
            controller_names = [
                [conf.INVOICE_TYPE_VAT, 'vat', 'Faktury VAT'],
                [conf.INVOICE_TYPE_PROFORMA, 'proforma', 'Faktury proforma'],
            ]
            paid_action = (invoice_status, text) ->
                if invoice_status == models.Invoice.STATUS_PAID
                    ''
                else
                    text
            @el.find('.left').html tpl.render 'index', {blocks: ({type: c[0], id: c[1], name: c[2], 'paid_action': (text) -> paid_action(c[0], text)} for c in controller_names)}
            @controllers = {}
            filter_items = (item, param) -> item.constructor.TYPE == param
            for record in controller_names
                inv_con = new Invoices
                    filter_function: filter_items
                    inv_param: record[0]
                    el: $("##{record[1]} table tbody")
                    inv_tpl: 'inv_t_t'
                @controllers[record[0]] = inv_con


        tpl.load OFFICE_APP_NAME, 'index_right', =>
            @el.find('.right').html tpl.render 'index_right', {}

class InvoicePreview extends Spine.Controller
    events:
        "click .button.delete": "delete"
        "click .button.print": "print"
        "click .button.mark_as_paid": "mark_as_paid"
        "click .button.download": "download"
        "click .button.edit": "edit"
        "click .button.intovat": "into_vat"

    constructor: ->
        super
        @model_cls = models[conf.INVOICE_MODELS[parseInt @inv_type]]
        try
            @get_item()
        catch error
            @model_cls.bind 'refresh', @get_item
            @model_cls.fetch data: "id=#{@inv_id}"

    get_item: =>
        @item = @model_cls.find @inv_id
        models.InvoiceItem.fetch data: "invoice_id=#{@item.id}"
        models.InvoiceItem.bind "refresh", @get_item_ai

    get_item_ai: =>
        $.get conf.INVOICE_ADD_INFO_ADDR + @item.id, (data) =>
            for key, val of data[@item.id]
                @item[key] = val
            @render()

    release: (fun) =>
        super
        models.InvoiceItem.unbind "refresh", @get_item_ai
        if @model_cls
            @model_cls.unbind 'refresh', @get_item


    render: =>
        inv_items = models.InvoiceItem.select (inv_item) => inv_item.invoice == @item.id
        ctx =
            item: @item
            type: @item.constructor.TYPE
            verbose_name: @item.constructor.VERBOSE_NAME
            inv_items: inv_items

        tpl.load OFFICE_APP_NAME, 'preview', =>
            @el.find('.left').html tpl.render 'preview', ctx
            for item_row in @el.find('.goods table tbody tr')
                (new ComputeValue(@el, @el.find('.goods table tbody'))).compute_values(target: $(item_row).find('td.net_price span'))
        tpl.load OFFICE_APP_NAME, 'preview_right', =>
            @el.find('.right').html tpl.render 'preview_right', {}
            if parseInt(@inv_type) is conf.INVOICE_TYPE_VAT
                @el.find('.right .intovat').hide()
            else
                @el.find('.right .intovat').show()

    print: (e) =>
        @item.print()
        
    download: (e) =>
        @item.download()

    mark_as_paid: (e) =>
        @item.mark_paid()

    delete: (e) =>
        document.location.hash = "/"
        window.quick_msg "#{@item.key}", "Faktura o numerze #{@item.key} usunięta."
        @item.destroy()

    edit: (e) =>
        document.location.hash = "/edit-invoice/#{conf.INVOICE_TYPES_REV[@item.constructor.TYPE]}/#{@item.id}"

    into_vat: (e) =>
        @item.into_vat (data) =>
            document.location.hash = "/"
            window.quick_msg "#{@item.key}", "Faktura VAT o numerze #{data.key} utworzna."


window.controllers = {}
window.controllers.Index = Index
window.controllers.InvoicePreview = InvoicePreview
window.controllers.TypeInvoices = TypeInvoices
window.ComputeValue = ComputeValue
