import json

class JsonResource(object):

    def render_object(self, obj, request):
        s = json.dumps(obj)
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')
        request.setHeader('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE')
        request.setHeader('Access-Control-Allow-Headers', ' X-Requested-With')
        request.setHeader('Content-Length', len(s))
        return s