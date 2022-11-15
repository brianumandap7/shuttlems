from django.contrib import admin

from .models import Status, Tickets, Stations, shuttle, destination, current_loc, imhere, tracing, answers, questions, hdf, reserve, Ticket_status, participants, shuttle_service, shuttle_driver, shuttle_service_list, shuttle_ride
# Register your models here.
admin.site.register(Tickets)
admin.site.register(shuttle)
admin.site.register(destination)
admin.site.register(current_loc)
admin.site.register(tracing)
admin.site.register(answers)
admin.site.register(questions)
admin.site.register(hdf)
admin.site.register(Ticket_status)
admin.site.register(participants)
admin.site.register(shuttle_service)
admin.site.register(shuttle_service_list)
admin.site.register(shuttle_driver)
admin.site.register(shuttle_ride)