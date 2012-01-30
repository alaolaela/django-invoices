OFFICE_APP_NAME = 'office'
window.OFFICE_APP_NAME = OFFICE_APP_NAME

class App extends Spine.Controller
    constructor: ->
        @current_controller = false
        rc = =>
            if @current_controller
                current_controller.release()
        @routes
            "/add-invoice/:inv_type": (params) ->
                if not params.inv_type
                    return
                rc()
                current_controller = new controllers.InvoiceAddition inv_type: params.inv_type, el: $('#content')
            "/edit-invoice/:inv_type/:inv_id": (params) ->
                if not params.inv_type
                    return
                rc()
                current_controller = new controllers.InvoiceAddition inv_id: params.inv_id, inv_type: params.inv_type, el: $('#content')
            "/show-invoice/:inv_type/:inv_id": (params) ->
                if not (params.inv_type and params.inv_id)
                    return
                rc()
                current_controller = new controllers.InvoicePreview
                    inv_type: params.inv_type
                    inv_id: params.inv_id
                    el: $('#content')
            "/": ->
                rc()
                current_controller = new controllers.Index el: $('#content')
        Spine.Route.setup()

        
$ ->
    a = new App()
