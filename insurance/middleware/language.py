# from django.utils import translation



# class LanguageMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         print('set language to spanish...')
#         translation.activate("fa")
#         request.LANGUAGE_CODE = "fa"
#         response = self.get_response(request)
#         translation.deactivate()

#         return response