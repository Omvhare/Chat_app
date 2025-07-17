# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from .models import Message
# from django.db.models import Q
# from datetime import datetime
#
#
# @login_required
# def chat_room(request, room_name):
#     search_query = request.GET.get('search', '')
#     users = User.objects.exclude(id=request.user.id)
#     chats = Message.objects.filter(
#         (Q(sender=request.user) & Q(receiver__username=room_name)) |
#         (Q(receiver=request.user) & Q(sender__username=room_name))
#     )
#
#     if search_query:
#         chats = chats.filter(Q(content__icontains=search_query))
#
#     chats = chats.order_by('timestamp')
#     user_last_messages = []
#
#     for user in users:
#         last_message = Message.objects.filter(
#             (Q(sender=request.user) & Q(receiver=user)) |
#             (Q(receiver=request.user) & Q(sender=user))
#         ).order_by('-timestamp').first()
#
#         user_last_messages.append({
#             'user': user,
#             'last_message': last_message
#         })
#
#     from django.utils import timezone
#     from datetime import datetime
#
#     user_last_messages.sort(
#         key=lambda x: x['last_message'].timestamp if x['last_message'] and x[
#             'last_message'].timestamp else timezone.make_aware(datetime.min),
#         reverse=True
#     )
#
#     # chat/views.py
#
#     def user_list(request):
#         # user list logic
#         return render(request, 'user_list.html')
#
#     return render(request, 'chat.html', {
#         'room_name': room_name,
#         'chats': chats,
#         'users': users,
#         'user_last_messages': user_last_messages,
#         'search_query': search_query
#     })

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from django.db.models import Q
from datetime import datetime
from django.utils import timezone

@login_required
def chat_room(request, room_name):
    search_query = request.GET.get('search', '')
    users = User.objects.exclude(id=request.user.id)
    chats = Message.objects.filter(
        (Q(sender=request.user) & Q(receiver__username=room_name)) |
        (Q(receiver=request.user) & Q(sender__username=room_name))
    )

    if search_query:
        chats = chats.filter(Q(content__icontains=search_query))

    chats = chats.order_by('timestamp')
    user_last_messages = []

    for user in users:
        last_message = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver=user)) |
            (Q(receiver=request.user) & Q(sender=user))
        ).order_by('-timestamp').first()

        user_last_messages.append({
            'user': user,
            'last_message': last_message
        })

    user_last_messages.sort(
        key=lambda x: x['last_message'].timestamp if x['last_message'] and x['last_message'].timestamp else timezone.make_aware(datetime.min),
        reverse=True
    )

    return render(request, 'chat.html', {
        'room_name': room_name,
        'chats': chats,
        'users': users,
        'user_last_messages': user_last_messages,
        'search_query': search_query
    })


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'user_list.html', {'users': users})

