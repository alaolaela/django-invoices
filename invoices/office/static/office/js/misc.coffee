window.STATUS_OK = 'ok'
window.STATUS_ERROR = 'error'
window.STATUS_KEY = 'status'

window.quick_msg = (title, msg) ->
    $.gritter.add
        title: title
        text: msg
