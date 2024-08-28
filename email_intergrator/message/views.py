import time

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from message.models import EmailAccount, Message


# Function to send progress updates through WebSocket
def send_progress(stage, progress):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'progress_group',  # Ensure this matches the group name in your consumer
        {
            'type': 'progress_update',
            'stage': stage,
            'progress': progress,
        }
    )


# View to display the message list page with a progress bar
@login_required
def message_list(request):
    email_accounts = EmailAccount.objects.filter(user=request.user)
    messages = Message.objects.filter(user=request.user)
    return render(request, 'templates/message_list.html',
                  {'messages': messages, 'email_accounts': email_accounts})


# View to start the process of reading and fetching messages
@login_required
def fetch_messages(request):
    email_account = EmailAccount.objects.filter(user=request.user).first()  # Assume the user has added an email account

    if not email_account:
        return JsonResponse({'error': 'No linked email accounts'}, status=400)

    # Reading messages stage
    for i in range(50):
        send_progress('reading', i)  # Send progress through WebSocket
        time.sleep(0.1)  # Simulate delay in reading messages

    # Fetching messages stage
    for i in range(50, 100):
        send_progress('fetching', i)  # Send progress through WebSocket
        # Example of adding a message to the database (replace with actual logic for fetching messages)
        Message.objects.create(
            subject=f"Example message {i}",
            date_sent="2024-08-24 12:00:00",
            date_received="2024-08-24 12:00:00",
            email_body=f"Message text {i}",
            user=request.user,
            email_account=email_account
        )
        time.sleep(0.1)  # Simulate delay in fetching messages

    return JsonResponse({'success': 'Messages successfully loaded'})
