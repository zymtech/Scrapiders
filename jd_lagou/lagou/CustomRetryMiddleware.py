from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware


class CustomRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if response.status in [301, 307, 302,403]:
            return response