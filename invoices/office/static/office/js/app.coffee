OFFICE_APP_NAME = 'office'
window.OFFICE_APP_NAME = OFFICE_APP_NAME

class App extends Spine.Controller
    constructor: ->
        @routes
            "/add-invoice/:inv_type": (params) ->
                if not params.inv_type
                    return
                new controllers.InvoiceAddition inv_type: params.inv_type, el: $('#content')
            "/show-invoice/:inv_type/:inv_id": (params) ->
                if not (params.inv_type and params.inv_id)
                    return
                new controllers.InvoicePreview
                    inv_type: params.inv_type
                    inv_id: params.inv_id
                    el: $('#content')
            "/": ->
                ind = new controllers.Index el: $('#content')
        Spine.Route.setup()

        
$ ->
    a = new App()
