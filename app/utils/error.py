# Example error handler
class ErrorHandler:
    def handle_exception(self, exception: Exception) -> str:
        # log error or do something with it
        return str(exception)  # or generate a unique error ID
