from rest_framework.renderers import JSONRenderer
from rest_framework.views import exception_handler


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {"errors": [], "data": {}, "status": "success"}
        if isinstance(data, dict):
            if errors := data.get('errors'):
                response_data['errors'] = errors if isinstance(errors, list) else [errors]
                response_data['status'] = 'failed'
            else:
                response_data['data'] = data
        elif isinstance(data, list):
            response_data['data'] = data

        response = super(CustomJSONRenderer, self).render(
            response_data, accepted_media_type, renderer_context
        )
        return response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data = {'errors': response.data}
    return response
