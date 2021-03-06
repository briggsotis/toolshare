from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from messaging.models import Message
from django.contrib.auth.models import User
from django.contrib import messages
from messaging.forms import MessageForm

def messages_view(request):
	if not request.user.is_authenticated():
		return redirect('login')
	if request.method == 'POST':
		form = MessageForm(data=request.POST)
		if form.is_valid():
			subject = form.cleaned_data['subject']
			to = form.cleaned_data['to']
			body = form.cleaned_data['body']
			send_to = User.objects.filter(username=to)
			if send_to.count() != 0:
				msg = Message()
				msg.msg_from = request.user
				msg.msg_to = send_to[0]
				msg.body = body
				msg.subject = subject
				msg.save()
				messages.add_message(request, messages.SUCCESS, 'Message sent Successfully', extra_tags='alert-success')
			else:
				messages.add_message(request, messages.WARNING, 'User Does Not Exist.', extra_tags='alert-danger')
		else:
			messages.add_message(request, messages.WARNING, 'One or More Invalid Field(s).', extra_tags='alert-danger')
		return redirect('messaging:messages')
	template = loader.get_template('base_messages_inbox.html')
	message_q = Message.objects.filter(msg_to=request.user)[:50]
	if message_q.count() != 0:
		message_list = list(message_q)
		message_list.reverse()
		args = {'user_messages': message_list}
	else:
		args = {}
	context = RequestContext(request, args)
	return HttpResponse(template.render(context))

def message_delete_view(request, message_id):
	if not request.user.is_authenticated():
		return redirect('login')
	msg = Message.objects.get(id=message_id)
	if msg.msg_to == request.user:
		msg.delete()
	return redirect('messaging:messages')

def set_message_read(request, message_id):
	if not request.user.is_authenticated():
		return redirect('sharetools:login')
	msg = Message.objects.get(id=message_id)
	if msg.msg_to != request.user:
		return redirect('messaging:messages')

	if request.method == "POST":
		if request.POST.get("delete", "-1") != "-1":
			msg.delete()
		return redirect('messaging:messages')
	msg.markRead()
	template = loader.get_template('base_read_message.html')
	context = RequestContext(request, {'message': msg})
	return HttpResponse(template.render(context))
