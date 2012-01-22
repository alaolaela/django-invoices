
class Invoices extends Spine.Controller
    constructor: ->
        super

class Invoice extends Spine.Controller
    constructor: ->
        super
        load_template OFFICE_APP_NAME, 'inv_t', -> return

    render: (item) =>
        if (item)
            @item = item
        @replace render_tpl OFFICE_APP_NAME, 'inv_t'
        @
