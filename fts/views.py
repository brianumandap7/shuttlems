from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from ticket.models import Tickets, Status, Stations, shuttle, destination, current_loc, imhere
from login.models import Author, Roles


def fts(request):
	query = {
		'list': Tickets.objects.all(),
	}
	return render(request, 'fts/fts.html', query)

def fts1(request):
	query = {
		'list': Tickets.objects.all(),
	}
	return render(request, 'fts/fts1.html', query)

def head(request):
	query = {
		'list': Tickets.objects.all(),
	}
	return render(request, 'fts/head.html', query)

def driver(request):
	query = {
		'shuttle': shuttle.objects.filter(driver = request.user),
		'curr': current_loc.objects.all(),
		'stat': Stations.objects.filter(a_driver = request.user),
		'cnt': imhere.objects.all().count(),

	}

	if request.method == "POST":
		upd = Stations.objects.get(a_driver = request.user)
		upd.current_loc_id = request.POST.get('cl')
		upd.lat = request.POST.get('lat')
		upd.lon = request.POST.get('lon')
		upd.save()

	return render(request, 'fts/driver.html', query)


def exec(request):
	query = {
		'list': Tickets.objects.all(),
	}
	return render(request, 'fts/exec.html', query)

def execu(request, tag = 0):
	query = {
		'tag': tag,
		'upd':Tickets.objects.filter(ticket_id = tag).update(status_id = 4),
	}
	return render(request, 'fts/execu.html', query)

def headu(request, tag = 0):
	query = {
		'tag':tag,
		'upd':Tickets.objects.filter(ticket_id = tag).update(status_id = 2),
	}
	return render(request, 'fts/headu.html', query)


def ftsu(request, tag = 0):
	query = {
		'tag':tag,
		'driv': Author.objects.filter(role_id = 6)
	}
	
	if request.method == "POST":
		upd = Tickets.objects.get(ticket_id = tag)
		upd.status_id = 3
		upd.save()

		return HttpResponseRedirect('/fts/')
	return render(request, 'fts/ftsu.html', query)

def add_driver(request):
	query = {
	}
	return render(request, 'fts/add_driver.html', query)




