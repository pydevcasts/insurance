# from django.shortcuts import HttpResponse, get_object_or_404
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# User = get_user_model()



# def send_notification(request):
#     channel_layer = get_channel_layer()
#     message = request.GET.get("message")
#     async_to_sync(channel_layer.group_send)(
#         "notification_broadcast",
#         {
#             'type': 'send_notification',
#              'notification':
#         {
      
#             'message': message
#         }
#         }
#     )
#     return HttpResponse("Done")