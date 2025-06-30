import json


class SanitizeScimPatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/scim/") and request.method == "PATCH":
            try:
                data = json.loads(request.body)
                for op in data.get("Operations", []):
                    if op.get("path") == "active":
                        val = str(op.get("value", "")).strip().lower()
                        if val in ("true", "false"):
                            op["value"] = val == "true"
                            request._body = json.dumps(data).encode("utf-8")
                            break
            except Exception:
                pass

        return self.get_response(request)
