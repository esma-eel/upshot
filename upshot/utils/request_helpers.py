def is_ajax_header(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def is_ajax_meta(request):
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
