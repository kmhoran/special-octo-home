from rest_framework.exceptions import APIException



class ArgumentException(APIException):
    status_code = 400
    default_detail = 'Invalid argument passed'
    default_code = 'BAD_REQUEST'

class NotAllowedException(APIException):
    status_code = 405
    default_detail = 'Methond not allowed'
    default_code = 'NOT_ALLOWED'

class ApplicationException(APIException):
    status_code = 500
    default_detail = 'A server error occured'
    default_code = 'INTERNAL_ERROR'