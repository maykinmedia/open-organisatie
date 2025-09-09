from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from vng_api_common.views import ERROR_CONTENT_TYPE


class ProblemJSONRenderer(CamelCaseJSONRenderer):
    media_type = ERROR_CONTENT_TYPE
