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
        models.VatInvoice.bind("change", (item) => @invoice_changed(item, models.VatInvoice))
        models.ProformaInvoice.bind("change", (item) => @invoice_changed(item, models.ProformaInvoice))

    add_invoice: (items, model_cls) =>
        filterted_items = ((new Invoice(item: item)).render() for item in items when item.status == @inv_status)
        if not filterted_items.length
            return
        items_ids = (item.id for item in items  when item.status == @inv_status)
        $.get conf.INVOICE_ADD_INFO_ADDR + items_ids.join(','), (data) =>
                for inv_id, add_info of data
                    gross_price = add_info.gross_price
                    inv = model_cls.find(inv_id)
                    inv.gross_price = gross_price.toFixed 2
                    inv.trigger('change-local', inv)
            ,'json'
        for a in filterted_items
            if @el.find("#invoice-#{a.item.constructor.TYPE}-#{a.item.id}").length
                continue
            @append a
    
    invoice_changed: (item, model_cls) =>
        if item.status != @inv_status
            @el.find("#invoice-#{item.constructor.TYPE}-#{item.id}").parent().remove()
        else
            @add_invoice([item], model_cls)
    
    delete: =>
        for check in @el.find("input:checked")
            $(check).parent().item().destroy()

    print: =>
        checks = @el.find("input:checked")
        for check in checks
            item = $(check).parent().item().item
            item.status = models.Invoice.STATUS_TOBEPAID
            item.save()
            window.open "/invoice/render/.pdf?doc_codename=INVOICE&id=#{item.id}", "_blank"

    download: =>
        ids = ""
        checks = @el.find("input:checked")
        for check in checks
            id = $(check).parent().item().item.id
            ids = "#{ids}&id=#{id}"
        window.open "/invoice/render/.zip?doc_codename=INVOICE#{ids}"

class Index extends Spine.Controller
    events:
        "click input.delete": "delete_invoice"
        "click input.print": "print_invoice"
        "click input.download": "download_invoice"

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

    download_invoice: (e) =>
        @controllers[$(e.target).data('ref')].download()
    

class InvoicePreview extends Spine.Controller
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
        models.InvoiceItem.bind "refresh", =>
            $.get conf.INVOICE_ADD_INFO_ADDR + @item.id, (data) =>
                for key, val of data[@item.id]
                    @item[key] = val
                @render()

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


window.controllers = {}
window.controllers.Index = Index
window.controllers.InvoicePreview = InvoicePreview
window.ComputeValue = ComputeValue
