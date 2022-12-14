from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Tickets, Status, Stations, shuttle, destination, current_loc, imhere, answers, questions, hdf, reserve, participants, shuttle_service, shuttle_service_list, shuttle_driver, shuttle_ride
from login.models import Roles, Author,Sex
from django.utils import timezone as tz
from django.db.models import Q
import datetime
import calendar
import json
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from .utils import Calendar
from datetime import timedelta
from django.views.decorators.clickjacking import xframe_options_exempt
from .resources import PersonResource
from django.contrib import messages
from tablib import Dataset

def simple_upload(request):
	if request.method == 'POST':
		person_resource = PersonResource()
		dataset = Dataset()
		new_person = request.FILES['myfile']

		if not new_person.name.endswith('xlsx'):
			messages.info(request, 'wrong file format')
			return render (request, 'ticket/upload.html')

		imported_data = dataset.load(new_person.read(),format = 'xlsx')
		for data in imported_data:
			db = User()
			db.username = data[1]
			pw = data[2]
			db.set_password(pw)
			db.email = data[3]
			db.first_name = data[4]
			db.last_name = data[5]
			db.is_staff = data[6]
			db.save()
	return render(request, 'ticket/upload.html')	

class CalendarView(generic.ListView):
    model = Tickets
    template_name = 'ticket/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('day', None))
        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.datetime.today()


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

@xframe_options_exempt
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
		'dr': shuttle_driver.objects.all(),
	}

	if request.method == "POST":
		db = Tickets.objects.get(ticket_id = tag)
		db.driver_id = request.POST.get('d') or None
		db.ticket_status_id = 2
		db.save()

		return HttpResponseRedirect('/ticket/fts_ticket')

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

def iscan(request, sn = 0):
	query = {
		'sn': sn,
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

def iscancon(request, con = '', sn = 0):
	query = {
		'con': con,
		'sn': sn,
		'exec': shuttle_ride.objects.create(shuttle_ride_log = con, shuttle_service_id = sn)
	}

	return render(request, 'ticket/iscancon.html', query)

def datav(request):
	query = {
		'ss': shuttle_service.objects.all(),
	}
	now = tz.now()
	query['now'] = now
	today = datetime.date.today()

	query['month'] = str(today.month)
	query['day'] = str(today.day)
	query['ride123'] = shuttle_ride.objects.all()
	query['ride1'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day__lte = str(7))).count()
	query['ride2'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&(Q(shuttle_ride_date__day__gte = str(8))&Q(shuttle_ride_date__day__lte = str(14)))).count()
	query['ride3'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&(Q(shuttle_ride_date__day__gte = str(15))&Q(shuttle_ride_date__day__lte = str(21)))).count()
	query['ride4'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&(Q(shuttle_ride_date__day__gte = str(22))&Q(shuttle_ride_date__day__lte = str(31)))).count()
	
	query['h1'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(1))).count()
	query['h2'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(2))).count()
	query['h3'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(3))).count()
	query['h4'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(4))).count()
	query['h5'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(5))).count()
	query['h6'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(6))).count()
	query['h7'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(7))).count()
	query['h8'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(8))).count()
	query['h9'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(9))).count()
	query['h10'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(10))).count()
	query['h11'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(11))).count()
	query['h12'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__hour = str(12))).count()
	query['m'] = Author.objects.filter(sex_id = 1).count()
	query['f'] =Author.objects.filter(sex_id = 2).count()

	query['w1'] = json.dumps(query['ride1'])
	query['w2'] = json.dumps(query['ride2'])
	query['w3'] = json.dumps(query['ride3'])
	query['w4'] = json.dumps(query['ride4'])

	query['t1'] = json.dumps(query['h1'])
	query['t2'] = json.dumps(query['h2'])
	query['t3'] = json.dumps(query['h3'])
	query['t4'] = json.dumps(query['h4'])
	query['t5'] = json.dumps(query['h5'])
	query['t6'] = json.dumps(query['h6'])
	query['t7'] = json.dumps(query['h7'])
	query['t8'] = json.dumps(query['h8'])
	query['t9'] = json.dumps(query['h9'])
	query['t10'] = json.dumps(query['h10'])
	query['t11'] = json.dumps(query['h11'])
	query['t12'] = json.dumps(query['h12'])

	query['male'] = json.dumps(query['m'])
	query['female'] = json.dumps(query['f'])

	return render(request, 'ticket/datav.html', query)

def dataview(request, tag = 0):
	query = {
		'tag': tag,
	}
	today = datetime.date.today()

	query['month'] = str(today.month)
	query['day'] = str(today.day)

	if request.method == "POST":
		start_date = request.POST.get('s')
		end_date = request.POST.get('e')

		se = shuttle_ride.objects.filter(Q(shuttle_ride_date__range=[start_date, end_date])&Q(shuttle_service_id = tag)).count()

		return HttpResponseRedirect('/ticket/dataview/'+str(tag)+'/'+str(se)+'/'+str(start_date)+'/'+str(end_date))



	query['d1'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(1))&Q(shuttle_service_id = tag)).count()
	query['d2'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(2))&Q(shuttle_service_id = tag)).count()
	query['d3'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(3))&Q(shuttle_service_id = tag)).count()
	query['d4'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(4))&Q(shuttle_service_id = tag)).count()
	query['d5'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(5))&Q(shuttle_service_id = tag)).count()
	query['d6'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(6))&Q(shuttle_service_id = tag)).count()
	query['d7'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(7))&Q(shuttle_service_id = tag)).count()
	query['d8'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(8))&Q(shuttle_service_id = tag)).count()
	query['d9'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(9))&Q(shuttle_service_id = tag)).count()
	query['d10'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(10))&Q(shuttle_service_id = tag)).count()
	query['d11'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(11))&Q(shuttle_service_id = tag)).count()
	query['d12'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(12))&Q(shuttle_service_id = tag)).count()
	query['d13'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(13))&Q(shuttle_service_id = tag)).count()
	query['d14'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(14))&Q(shuttle_service_id = tag)).count()
	query['d15'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(15))&Q(shuttle_service_id = tag)).count()
	query['d16'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(16))&Q(shuttle_service_id = tag)).count()
	query['d17'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(17))&Q(shuttle_service_id = tag)).count()
	query['d18'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(18))&Q(shuttle_service_id = tag)).count()
	query['d19'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(19))&Q(shuttle_service_id = tag)).count()
	query['d20'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(20))&Q(shuttle_service_id = tag)).count()
	query['d21'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(21))&Q(shuttle_service_id = tag)).count()
	query['d22'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(22))&Q(shuttle_service_id = tag)).count()
	query['d23'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(23))&Q(shuttle_service_id = tag)).count()
	query['d24'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(24))&Q(shuttle_service_id = tag)).count()
	query['d25'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(25))&Q(shuttle_service_id = tag)).count()
	query['d26'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(26))&Q(shuttle_service_id = tag)).count()
	query['d27'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(27))&Q(shuttle_service_id = tag)).count()
	query['d28'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(28))&Q(shuttle_service_id = tag)).count()
	query['d29'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(29))&Q(shuttle_service_id = tag)).count()
	query['d30'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(30))&Q(shuttle_service_id = tag)).count()
	query['d31'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_ride_date__day = str(31))&Q(shuttle_service_id = tag)).count()
	query['hm'] = shuttle_ride.objects.filter(Q(shuttle_ride_date__month = str(today.month))&Q(shuttle_service_id = tag)).count()

	return render(request, 'ticket/dataview.html', query)

def dataview1(request, tag = 0, se = 0, sd = "", ed = ""):
	query = {
		'tag': tag,
		'se': se,
		'sd': sd,
		'ed': ed,

		'sh': shuttle_service_list.objects.filter(shuttle_service_list_id = tag),
	}

	return render(request, 'ticket/dataview1.html', query)
def add_users(request):
	query = {

	}
	if request.method == "POST":
		db = User()
		db.username = request.POST.get('uname') or None
		password = request.POST.get('pword')

		db.set_password(password)

		db.first_name = request.POST.get('fname')
		db.last_name = request.POST.get('lname')
		db.email = request.POST.get('eadd')

		db.save()

		return HttpResponseRedirect('/ticket/cw')
	return render(request, 'ticket/add_users.html', query)

def assign(request):
	query = {
		'all': User.objects.all(),
		'au': Author.objects.all(),
	}

	return render(request, 'ticket/assign.html', query)


def assign_role(request, us = 0):
	query = {
		'us': us,
		'u': User.objects.filter(id = us),
		'a': Author.objects.filter(user_id = us),
	}
	if request.method == "POST":
		db = Author.objects.get(user_id = us)
		db.role_id = request.POST.get('role')
		db.position	= request.POST.get('position')
		db.student_or_employee_number = request.POST.get('snum')
		db.year_level = request.POST.get('ylevel')
		db.course_or_department = request.POST.get('cd')
		db.sex_id = request.POST.get('sex')

		db.save()
		return HttpResponseRedirect('/ticket/assign')
	return render(request, 'ticket/assign_role.html', query)

def add_role(request, us = 0):
	query = {
		'us': us,
		'u': User.objects.filter(id = us),
		'a': Author.objects.filter(user_id = us),
	}
	if request.method == "POST":
		db = Author()
		db.user_id = us
		db.role_id = request.POST.get('role')
		db.position	= request.POST.get('position')
		db.student_or_employee_number = request.POST.get('snum')
		db.year_level = request.POST.get('ylevel')
		db.course_or_department = request.POST.get('cd')
		db.sex_id = request.POST.get('sex')

		db.save()
		return HttpResponseRedirect('/ticket/cw')
	return render(request, 'ticket/add_role.html', query)

def delete_role(request, tag = 0):
	query = {
		'tag': tag,
		'exec': User.objects.filter(id = tag).delete(),
	}

	return render(request, 'ticket/delete_user.html', query)

def show_users(request):
	query = {
		'us': User.objects.all()
	}

	return render(request, 'ticket/show_users.html', query)

def edit_user(request, tag = 0):
	query = {
		'tag': tag,
		'us': User.objects.filter(id = tag),
	}

	if request.method == "POST":
		db = User.objects.get(id = tag)
		db.username = request.POST.get('uname') or None

		db.first_name = request.POST.get('fname')
		db.last_name = request.POST.get('lname')
		db.email = request.POST.get('eadd')

		if request.POST.get('ac'):
			db.is_active = True
		else:
			db.is_active = False

		db.save()

		return HttpResponseRedirect('/ticket/show_users')

	return render(request, 'ticket/edit_user.html', query)

def edit_driver(request, tag = 0):
	query = {
		'tag': tag,
		'sd': shuttle_driver.objects.filter(shuttle_driver_id = tag),
	}

	if request.method == "POST":
		db = shuttle_driver.objects.get(shuttle_driver_id = tag)
		db.driver_name = request.POST.get('dname') or None
		db.save()

		return HttpResponseRedirect('/ticket/add_driver')

	return render(request, 'ticket/edit_driver.html', query)

def delete_driver(request, tag = 0):
	query = {
		'tag': tag,
		'sd': shuttle_driver.objects.filter(shuttle_driver_id = tag).delete(),
	}

	return render(request, 'ticket/delete_driver.html', query)

def remove_shuttle(request, tag = 0):
	query = {
		'tag': tag,
		'sd': shuttle_service_list.objects.filter(shuttle_service_list_id = tag).delete(),
	}

	return render(request, 'ticket/remove_shuttle.html', query)

def iscanmenu(request):
	query = {
		'ss': shuttle_service.objects.all(),
		'slist': shuttle_service_list.objects.all(),
	}

	return render(request, 'ticket/iscanmenu.html', query)





