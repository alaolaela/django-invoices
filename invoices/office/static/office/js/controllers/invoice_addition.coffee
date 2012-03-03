
class InvoiceAddition extends Spine.Controller
    INVOICES_TPL_ADDR: '/invoice/formtpl/'
    CHOICES_ADDR: '/invoice/choices/'
    CUSTOMER_DATA_ADDR: '/invoice/customerdata/'
    CUSTOMER_INVOICE_DATA_ADDR: '/invoice/customerinvoicedata/'
    PRODUCTS_SEARCH_ADDR: '/invoice/products/'
    INVOICES_SAVE_ADDR: '/invoice/formsave/'

    events:
        "change #id_customer_content_type": "customer_type_chosen"
        "change #id_customer_object_id": "customer_chosen"
        "click .add_new_product": "new_invoice_item"
        "click a.delete_commodity": "delete_invoice_item"
        "change .quantity input": "compute_values"
        "change .net_price input": "compute_values"
        "change .net_value input": "compute_values"
        "change .tax select": "compute_values"
        "change #id_date_created": "recalculate_dates"
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
            @refreshElements()
            @load_tpl()
        tpl.load OFFICE_APP_NAME, 'add_right', =>
            @el.find('.right').html tpl.render 'add_right', {}
        @product_id = (parseInt(pid) for pid in @product_id.split(','))

    load_tpl: =>
        base_addr = "#{@INVOICES_TPL_ADDR}#{conf.INVOICE_TYPES[@inv_type]}/"
        if not @inv_id
            tpl_addr = base_addr
        else
            tpl_addr = "#{base_addr}#{@inv_id}/"
        tpl_addr = tpl_addr
        $.get tpl_addr, (data) =>
            @el.find('form.facture').html data
            @refreshElements()
            $("#id_date_sale, #id_date_created, #id_date_payment").datepicker
                showOn: "button"
                buttonImage: "#{STATIC_URL}office/css/images/calendar.png"
                buttonImageOnly: true

            $('.commodity textarea').each (i, e) =>
                txta = @set_autocomplete $(e)
		
            for item in @invoice_items.find 'tr'
                @compute_values target: $(item).find('.net_price input')
            if not @inv_id
                $('#id_customer_content_type').change()
            else
                $('#id_customer_object_id').change()
            
            if @customer_type
                $("#id_customer_content_type option[value=#{@customer_type}]").attr 'selected', true
                $('#id_customer_content_type').change()

            if @product_type and @product_id
                for pid in @product_id
                    $.get "#{@PRODUCTS_SEARCH_ADDR}?p_ct=#{@product_type}&p_id=#{pid}&#{@additional_params}", (data) =>
                        @add_product data
                    

            
    customer_type_chosen: (e) =>
        sel_el = $(e.target)
        ct_id = sel_el.val()
        if not ct_id
            return
        $.get "#{@CHOICES_ADDR}#{ct_id}/", (data) =>
            sel_customer = $ '#id_customer_object_id'
            sel_customer.html ''
            for rec in data
                new_opt = $('<option />',
                    value: rec[0]
                    text: rec[1]
                )
                if @customer_id and parseInt(@customer_id) == rec[0]
                    new_opt.attr 'selected', true

                sel_customer.append new_opt
            sel_customer.change()
        , 'json'

    customer_chosen: (e) =>
        customer_id = $(e.target).val()
        ct_id = $('#id_customer_content_type').val()
        $.get "#{@CUSTOMER_INVOICE_DATA_ADDR}#{ct_id}/#{customer_id}/", (data) =>
            cd = data.customer_data
            p = [cd.name, cd.address, "#{cd.postal_code} #{cd.city}"]
            if cd.daily_rate
                p.push "<br />Stawka dzienna: #{cd.daily_rate} Euro"
            if cd.rate
                p.push "<br />Stawka miesięczna: #{cd.rate} Euro"
            if cd.broker_tocket_price
                p.push "<br />Pośrednik - koszt biletu: #{cd.broker_tocket_price} Euro"
            $('#customer-data').html p.join('<br />')
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
    
    recalculate_dates: (e) =>
        date = new Date($(e.target).val())
        format_date_str = (date) -> "#{date.getFullYear()}-#{date.getMonth()+1}-#{date.getDate()}"
        $('#id_date_sale').val format_date_str(date)
        date.setDate date.getDate() + 21
        $('#id_date_payment').val format_date_str(date)

    compute_values: (e) =>
        (new ComputeValue(@el, @invoice_items)).compute_values(e)

    compute_summary: (e) =>
        (new ComputeValue(@el, @invoice_items)).compute_summary(e)

    save_invoice: (e) =>
        e.preventDefault()
        data = $('form').serialize()
        base_addr = save_addr = "#{@INVOICES_SAVE_ADDR}#{conf.INVOICE_TYPES[@inv_type]}/"
        if not @inv_id
            save_addr = base_addr
        else
            save_addr = "#{base_addr}#{@inv_id}/"
        $.post save_addr, data, (resp_data) =>
            for old_error_el in $ 'input.error, select.error, textarea.error'
                $(old_error_el).qtip "destroy"
                $(old_error_el).removeClass 'error'
            if resp_data[STATUS_KEY] == STATUS_OK
                quick_msg 'Zapis', 'Faktura zapisana poprawnie'
                document.location.hash = "/show-invoice/#{conf.INVOICE_TYPES[@inv_type]}/#{resp_data['id']}"
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
                        input_el = @el.find("#id_items-#{form_index}-#{input_name}").addClass 'error'
                        input_el.qtip
                            content: error_msg[0]
                    form_index += 1
    
    input_tip: (input_name, msg, cls) ->
        input_el = @el.find("#id_#{input_name}").addClass cls
        input_el.qtip
            content: msg[0]
        
    set_autocomplete: (el) ->
        el.autocomplete 'source': @PRODUCTS_SEARCH_ADDR, 'select': (e, ui) =>
            @set_product el, ui.item.obj_id, ui.item.ct_id, ui.item.label, ui.item.desc, ui.item.rate

    add_product: (data) =>
        el = $(".invoice-items tbody tr:last .commodity textarea")
        if not el.length or el.val()
            $('.add_new_product').click()
            el = $(".invoice-items tbody tr:last .commodity textarea")
        @set_product el, data['obj_id'], data['ct_id'], data['label'], data['desc'], data['rate']

    set_product: (el, p_id, ct_id, label, desc, rate) ->
        el.parent().find('a.clear').remove()
        clear_button = $('<a href="#" class="clear"></a>').css {'display': 'block'}
        ct_input = el.siblings('.ct').children 'input'
        oid_input = el.siblings('.oid').children 'input'
        el.val label
        el.parents('tr:first').find('.quantity input').val('1').change()
        el.parents('tr:first').find('.net_price input').val(rate).change()
        if p_id and ct_id
            clear_button.text "X - " + desc
            ct_input.val ct_id
            oid_input.val p_id
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
