from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse

# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username':username,
        'room':room,
        'room_details':room_details
    })

def checkview(request):
    if request.method == 'POST':
        room_name = request.POST['room_name']
        username = request.POST['username']

        if Room.objects.filter(name=room_name).exists():
            return redirect('/{}/?username={}'.format(room_name,username))
        else:
            new_room = Room.objects.create(name=room_name)
            new_room.save()
            return redirect('/{}/?username={}'.format(room_name,username))
        
def send(request):
    if request.method == 'POST':
        message = request.POST['message']
        room_id = request.POST['room_id']
        username = request.POST['username']
    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})