from loguru import logger

from log_request_id.middleware import RequestIDMiddleware


class LogRequestIdMiddleware(RequestIDMiddleware):
    def process_view(self, request, view_func, view_args, view_kwargs):
        with logger.contextualize(request_id=request.id):
            logger.debug(f"Start handling request.")
            response = view_func(request, *view_args, **view_kwargs)
            logger.debug(f"Request handled with response <{response}>.")

            return response
