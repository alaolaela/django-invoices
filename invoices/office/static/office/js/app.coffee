OFFICE_APP_NAME = 'office'
window.OFFICE_APP_NAME = OFFICE_APP_NAME

class App extends Spine.Controller
    constructor: ->
        @routes
            "/add-invoice": (params) ->
                new controllers.InvoiceAddition el: $('#content')
            "/users": ->
                console.log("users")
            "/": ->
                ind = new controllers.Index el: $('#content')
        Spine.Route.setup()

        
$ ->
    a = new App()
