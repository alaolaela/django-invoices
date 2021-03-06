OFFICE_APP_NAME = 'office'
window.OFFICE_APP_NAME = OFFICE_APP_NAME

class App extends Spine.Controller
    constructor: ->
        super
        @current_controller = false
        rc = =>
            $('#footer').before tpl.render('base', {})
            if @current_controller
                @current_controller.release()

        $("#content").remove()
        @routes
            "/add-invoice/:inv_type/:customer_type/:customer_id/:product_type/:product_id/*:additional": (params) ->
                if not params.inv_type
                    return
                if params.additional?
                    params.additional = params.additional[1..]
                rc()
                @current_controller = new controllers.InvoiceAddition 
                    inv_type: params.inv_type
                    customer_type: params.customer_type
                    customer_id: params.customer_id
                    product_type: params.product_type
                    product_id: params.product_id
                    additional_params: (if params.additional? then params.additional else '')
                    , el: $('#content')
            "/add-invoice/:inv_type": (params) ->
                if not params.inv_type
                    return
                rc()
                @current_controller = new controllers.InvoiceAddition inv_type: params.inv_type, el: $('#content')
            "/edit-invoice/:inv_type/:inv_id": (params) ->
                if not params.inv_type
                    return
                rc()
                @current_controller = new controllers.InvoiceAddition inv_id: params.inv_id, inv_type: params.inv_type, el: $('#content')
            "/show-invoice/:inv_type/:inv_id": (params) ->
                if not (params.inv_type and params.inv_id)
                    return
                rc()
                @current_controller = new controllers.InvoicePreview
                    inv_type: params.inv_type
                    inv_id: params.inv_id
                    el: $('#content')
            "/type/": ->
                rc()
                @current_controller = new controllers.TypeInvoices el: $('#content')
            "/": ->
                rc()
                @current_controller = new controllers.Index el: $('#content')
                @current_controller.init_controller()
        Spine.Route.setup()

        
$ ->
    tpl.load OFFICE_APP_NAME, 'base', =>
        a = new App()
