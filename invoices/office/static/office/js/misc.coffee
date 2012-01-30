window.STATUS_OK = 'ok'
window.STATUS_ERROR = 'error'
window.STATUS_KEY = 'status'

window.quick_msg = (title, msg) ->
    $.gritter.add
        title: title
        text: msg

mixin_extend = (obj, mixin) ->
    for name, method of mixin
        obj[name] = method

window.mixin_include = (klass, mixin) ->
    mixin_extend klass.prototype, mixin

#example
#class Button
#  onClick: -> # do stuff

#include Button, Options
#include Button, Events
