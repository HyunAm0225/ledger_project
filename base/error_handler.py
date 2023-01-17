from rest_framework.views import exception_handler


def exception_format_handler(exc, context):
    response = exception_handler(exc, context)
    response_data = dict()
    error_code = ""
    details = []

    if response is not None and hasattr(response, "data"):
        if isinstance(response.data, dict) and "detail" in response.data.keys():
            return response

        if isinstance(response.data, list):
            for detail_info in response.data:
                error = detail_info
                error_code = error.code if hasattr(error, "code") else str(error)
                details.append(
                    {
                        "property": None,
                        "message": str(error),
                        "code": str(error_code),
                    }
                )
        else:
            for key, detail_info in response.data.items():
                try:
                    error = detail_info[0]
                except KeyError:
                    error = detail_info

                error_code = error.code if hasattr(error, "code") else str(error)
                details.append(
                    {
                        "property": key if key != "non_field_errors" else None,
                        "message": str(error),
                        "code": str(error_code),
                    }
                )

        response_data["statusCode"] = response.status_code if response else 400
        response_data["detail"] = details
        response_data["error"] = error_code
        response.data = response_data

    return response
