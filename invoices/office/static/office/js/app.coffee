OFFICE_APP_NAME = 'office'
window.OFFICE_APP_NAME = OFFICE_APP_NAME

class App extends Spine.Controller
    constructor: ->
        @routes
            "/users/:id": (params) ->
                console.log("/users/", params.id)
            "/users": ->
                console.log("users")
        ind = new controllers.Index el: $('#content')

        
$ ->
    Spine.Route.setup()
    a = new App()
    window.a = a
