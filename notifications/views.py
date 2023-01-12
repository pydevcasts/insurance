# from django.shortcuts import HttpResponse, get_object_or_404
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from django.contrib.auth import get_user_model
# User = get_user_model()



# def send_notification(request, user_id):
#     user = get_object_or_404(User, pk = user_id)
#     title = request.GET.get('title')
#     content = request.GET.get('content')

#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(f'user_{user.id}_notification',
#     {
#         'type':'user.notify',
#         'notification':{
#             'title':title,
#             'content':content
#         }
#     })
#     return HttpResponse(f'notification send to {user.email}')