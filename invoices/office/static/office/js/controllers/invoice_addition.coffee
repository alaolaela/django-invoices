
class InvoiceAddition extends Spine.Controller
    INVOICES_TPL_ADDR: '/invoice/formtpl/'
    CHOICES_ADDR: '/invoice/choices/'
    PRODUCTS_SEARCH_ADDR: '/invoice/products/'
    INVOICES_SAVE_ADDR: '/invoice/formsave/'

    events:
        "change #id_customer_content_type": "customer_type_chosen"
        "click .add_new_product": "new_invoice_item"
        "click a.delete_commodity": "delete_invoice_item"
        "change .quantity input": "compute_values"
        "change .net_price input": "compute_values"
        "change .net_value input": "compute_values"
        "change .tax select": "compute_values"
        "click #save-invoice": "save_invoice"

    elements:
        '.add_new_product': 'new_prod_button'
        'table.empty tr': 'empty_row'
        '.goods table.invoice-items tbody': 'invoice_items'
        '#id_invoiceitem_set-TOTAL_FORMS': 'total_forms'

    constructor: ->
        super
        tpl.load OFFICE_APP_NAME, 'add', =>
            @el.find('.left').html tpl.render 'add', {}
            @load_tpl()
        tpl.load OFFICE_APP_NAME, 'add_right', =>
            @el.find('.right').html tpl.render 'add_right', {}
            @load_tpl()

    load_tpl: =>
        tpl_addr = "#{@INVOICES_TPL_ADDR}#{conf.INVOICE_TYPES[@inv_type]}/"
        $.get tpl_addr, (data) =>
            @el.find('form.facture').html data
            $("#id_date_sale, #id_date_created, #id_date_payment").datepicker
                showOn: "button"
                buttonImage: "#{STATIC_URL}office/css/images/calendar.png"
                buttonImageOnly: true

            $('.commodity textarea').each (i, e) =>
                txta = @set_autocomplete $(e)
		
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

    new_invoice_item: (e) =>
        e.preventDefault()
        new_record = $(@empty_row.parent().html().replace(/__prefix__/g, @total_forms.val()))
        @invoice_items.append new_record
        @set_autocomplete new_record.find('.commodity textarea')
        @total_forms.val(1 + parseInt(@total_forms.val()))

    delete_invoice_item: (e) =>
        e.preventDefault()
        el = $(e.target).parents('tr').eq(0)
        el.hide()
        el.find('.delete_commodity input').attr('checked', 'checked')
        @compute_summary()
    

    compute_values: (e) =>
        (new ComputeValue(@el, @invoice_items)).compute_values(e)

    compute_summary: (e) =>
        (new ComputeValue(@el, @invoice_items)).compute_summary(e)

    save_invoice: (e) =>
        e.preventDefault()
        data = $('form').serialize()
        save_addr = "#{@INVOICES_SAVE_ADDR}#{conf.INVOICE_TYPES[@inv_type]}/"
        $.post save_addr, data, (resp_data) =>
            for old_error_el in $ 'input.error, select.error, textarea.error'
                $(old_error_el).qtip "destroy"
                $(old_error_el).removeClass 'error'
            if resp_data[STATUS_KEY] == STATUS_OK
                quick_msg 'Zapis', 'Faktura zapisana poprawnie'
                return
            
            if resp_data['key']?
                $('#id_key').val resp_data['key']
            
            for own input_name, msg of resp_data['main_form_info']
                @input_tip input_name, msg, 'info'

            for own input_name, msg of resp_data['main_form_errors']
                @input_tip input_name, msg, 'error'

            if resp_data.hasOwnProperty 'items_form_errors'
                form_index = 0
                for item_form in resp_data['items_form_errors']
                    for own input_name, error_msg of item_form
                        input_el = @el.find("#id_invoiceitem_set-#{form_index}-#{input_name}").addClass 'error'
                        input_el.qtip
                            content: error_msg[0]
                    form_index += 1
    
    input_tip: (input_name, msg, cls) ->
        input_el = @el.find("#id_#{input_name}").addClass cls
        input_el.qtip
            content: msg[0]
        
    set_autocomplete: (el) ->
        el.autocomplete 'source': @PRODUCTS_SEARCH_ADDR, 'select': (e, ui) ->
            ct_input = el.siblings('.ct').children 'input'
            oid_input = el.siblings('.oid').children 'input'
            if ui.item
                clear_button = $('<a href="#"></a>').css({'display': 'block'}).text "X - " + ui.item.desc
                ct_input.val ui.item.ct_id
                oid_input.val ui.item.obj_id
                el.before clear_button
                clear_button.bind 'click', (e) ->
                    e.preventDefault()
                    ct_input.val ''
                    oid_input.val ''
                    $(@).remove()
            else
                    ct_input.val ''
                    oid_input.val ''

window.controllers.InvoiceAddition = InvoiceAddition
