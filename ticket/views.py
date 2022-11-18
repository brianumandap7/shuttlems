from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Tickets, Status, Stations, shuttle, destination, current_loc, imhere, answers, questions, hdf, reserve, participants, shuttle_service, shuttle_service_list, shuttle_driver, shuttle_ride
from login.models import Roles, Author,Sex
from django.utils import timezone as tz
from django.db.models import Q
import datetime
import calendar



def ticket(request):
	query = {
		'role': Author.objects.filter(user = request.user),
		'tik': Tickets.objects.filter(user = request.user)
	}
	return render(request, 'ticket/dash.html', query)

def admindash(request):
	query = {
		'uc': Author.objects.all().count(),
		'tc': Tickets.objects.all().count(),
		'sc': shuttle_service.objects.all().count(),
		'cc': hdf.objects.all().count(),
	}
	return render(request, 'ticket/admindash.html', query)

def student_page(request):
	query = {
		'gp': shuttle_service.objects.all(),
	}
	now = tz.now()
	query['now'] = now
	query['today'] = str(tz.localtime(now).date())
	query['part'] = participants.objects.filter(participant_user = request.user)
	query['mtx'] = Tickets.objects.filter(start_date = str(tz.localtime(now).date()))
	query['aut'] = Author.objects.filter(user = request.user)
	return render(request, 'ticket/student_page.html', query)

def employee_page(request):
	query = {
		'gp': shuttle_service.objects.all(),
	}
	now = tz.now()
	query['now'] = now
	query['today'] = str(tz.localtime(now).date())
	query['part'] = participants.objects.filter(participant_user = request.user)
	query['mtx'] = Tickets.objects.filter(start_date = str(tz.localtime(now).date()))
	query['aut'] = Author.objects.filter(user = request.user)
	return render(request, 'ticket/employee_page.html', query)

def fts_page(request):
	query = {
		'gp': shuttle_service.objects.all(),
	}
	now = tz.now()
	query['now'] = now
	today = datetime.date.today()
	query['month'] = str(today.month)
	query['day'] = str(today.day)

	query['mtx'] = Tickets.objects.filter(start_date = str(tz.localtime(now).date())).exclude(Q(ticket_status_id = 3)|Q(ticket_status_id = 4)|Q(ticket_status_id = 1))
	query['allmtx'] = Tickets.objects.filter(start_date__month = str(today.month)).exclude(Q(ticket_status_id = 3)|Q(ticket_status_id = 4)|Q(ticket_status_id = 1))
	
	return render(request, 'ticket/fts_page.html', query)

def file(request):
	query = {
		
	}
	now = tz.now()
	query['now'] = now
	query['today'] = tz.localtime(now).date()

	if request.method == "POST" and 'sb' in request.POST:
		db = Tickets()
		db.description = request.POST.get('pur')
		db.destination = request.POST.get('des')
		db.start_date = request.POST.get('dt')
		db.start_time = request.POST.get('tt')
		db.arrival_time = request.POST.get('ta')

		db.ticket_status_id = 1
		
		db.user = request.user
		db.save()

		return HttpResponseRedirect('/ticket/cw')
	return render(request, 'ticket/file.html', query)

def record(request):
	query = {
		'list': Tickets.objects.filter(user = request.user).order_by('-ticket_id')
	}
	
	return render(request, 'ticket/record.html', query)

def view_ticket(request, tag = 0):
	query = {
		'tag': tag,
		'ticket': Tickets.objects.filter(ticket_id = tag),
		'participants': User.objects.all(),
		'participants2': participants.objects.filter(ticket_id = tag),
		'r': Author.objects.filter(user = request.user),
	}

	if request.method == "POST":
		db = participants()
		db.participant_user_id = request.POST.get('part') or None
		db.ticket_id = tag
		db.save()

	
	return render(request, 'ticket/view_ticket.html', query)

def fts_ticket(request):
	query = {
		'ticket': Tickets.objects.all().order_by('-ticket_id'),
	}
	
	return render(request, 'ticket/fts_ticket.html', query)

def a(request, tag = 0):
	query = {
		'tag': tag,
		'exec': Tickets.objects.filter(ticket_id = tag).update(ticket_status_id = 2),
	}

	return render(request, 'ticket/a.html', query)
def d(request, tag = 0):
	query = {
		'tag': tag,
		'exec': Tickets.objects.filter(ticket_id = tag).update(ticket_status_id = 3),
	}

	return render(request, 'ticket/d.html', query)

def track(request):
	query = {

	}
	return render(request, 'ticket/track.html', query)


def dashtrack(request):
	query = {
	'sh': Stations.objects.all(),
	}
	return render(request, 'ticket/dashtrack.html', query)

def shuttle_track(request, tag=0):
	query = {
		'tag':tag,
		'curr': current_loc.objects.all(),
		'stat': Stations.objects.filter(station_id = tag),
		'res': reserve.objects.filter(user = request.user),
	}

	if request.method == "POST":
			db = reserve()
			db.user = request.user
			db.save()
	return render(request, 'ticket/shuttle_track.html', query)

def df(request, tag = 0):
	query = {
		'tag': tag,
		'hd': hdf.objects.all()[:1],
	}

	if request.method == "POST":
		db = hdf()
		db2 = participants.objects.get(Q(ticket_id = tag)&Q(participant_user = request.user))
		db.q1_id = 1
		db.q2_id = 2
		db.q3_id = 3
		db.ticket_id = tag

		db.a1 = request.POST.get('a1') or None

		if db.a2 != "None of the above":
			db.a2 = "Not cleared"
		else:
			db.a2 = "Cleared"

		if db.a3 != "None of the above":
			db.a3 = "Not cleared"
		else:
			db.a3 = "Cleared"
		
		db.user = request.user
		db2.hdf = 1
		db.save()
		db2.save()

		return HttpResponseRedirect('/ticket/cw')

	return render(request, 'ticket/hdf.html', query)

def conf(request):
	query = {
		'lat': hdf.objects.all().order_by('-id')[:1]
	}

	return render(request, 'ticket/conf.html', query)

def df0(request, tag):
	query = {
		'tag': tag,
		'hd': hdf.objects.all()[:1],
		'ans': answers.objects.all(),
	}

	return render(request, 'ticket/hdf0.html', query)

def cw(request):
	query = {
	
	}

	return render(request, 'ticket/cw.html', query)

def iscan(request):
	query = {
	
	}

	return render(request, 'ticket/iscan.html', query)

def hdf_list(request):
	query = {
		'dec': hdf.objects.all().exclude(user = None),

	}

	return render(request, 'ticket/hdf_list.html', query)

def view_ticket1(request, tag = 0):
	query = {
		'tag': tag,
		'ticket': Tickets.objects.filter(ticket_id = tag),
		'participants': User.objects.all(),
		'participants2': participants.objects.filter(ticket_id = tag),
		'r': Author.objects.filter(user = request.user),
	}
	
	return render(request, 'ticket/view_ticket1.html', query)

def route(request, tag = 0):
	query = {
		'tag': tag,
		'ss': shuttle_service.objects.filter(shuttle_service_id = tag),
	}

	return render(request, 'ticket/route.html', query)

def add_shuttle(request):
	query = {
		'ss': shuttle_service.objects.all(),
		'slist': shuttle_service_list.objects.all(),
	}

	if request.method == "POST":
		db = shuttle_service()
		db.shuttle_name_id = request.POST.get('sname') or None
		db.gps_link = request.POST.get('glink') or None

		db.save()

	return render(request, 'ticket/add_shuttle.html', query)

def delete_shuttle(request, tag):
	query = {
		'tag': tag,
		'ss': shuttle_service.objects.filter(shuttle_service_id = tag).delete()
	}

	return render(request, 'ticket/delete_shuttle.html', query)

def edit_shuttle(request, tag):
	query = {
		'tag': tag,
		'ss': shuttle_service.objects.filter(shuttle_service_id = tag)
	}
	if request.method == "POST":
		db = shuttle_service.objects.get(shuttle_service_id = tag)
		db.gps_link = request.POST.get('glink') or None

		db.save()

		return HttpResponseRedirect('/ticket/add_shuttle')

	return render(request, 'ticket/edit_shuttle.html', query)

def shuttle_options(request):
	query = {
		'ss': shuttle_service.objects.all()
	}

	return render(request, 'ticket/shuttle_options.html', query)

def cancel_ticket(request, tag = 0):
	query = {
		'tag': tag,
		'exec': Tickets.objects.filter(ticket_id = tag).update(ticket_status_id = 4),
	}

	return render(request, 'ticket/cancel_ticket.html', query)

def profile(request):
	query = {
		'dp': Author.objects.filter(user = request.user),
	}

	return render(request, 'ticket/profile.html', query)

def add_shuttle_list(request):
	query = {
		'dri': shuttle_driver.objects.all(),
		'slist': shuttle_service_list.objects.all(),
	}

	if request.method == "POST":
		db = shuttle_service_list()
		db.shuttle_name = request.POST.get('sname') or None
		db.plate_number = request.POST.get('pnumber') or None
		db.driver_name_id = request.POST.get('dname') or None

		db.save()

	return render(request, 'ticket/add_shuttle_list.html', query)

def add_driver(request):
	query = {
		'dri': shuttle_driver.objects.all(),
	}

	if request.method == "POST":
		db = shuttle_driver()
		db.driver_name = request.POST.get('dname') or None

		db.save()

	return render(request, 'ticket/add_driver.html', query)

def iscancon(request, con = ''):
	query = {
		'con': con,
		'exec': shuttle_ride.objects.create(shuttle_ride_log = con)
	}

	return render(request, 'ticket/iscancon.html', query)

def datav(request):
	query = {

	}

	return render(request, 'ticket/datav.html', query)

