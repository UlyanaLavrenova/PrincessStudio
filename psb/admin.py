from django.contrib import admin
from .models import Procedure, Master, Record, VacantTimes, Message

admin.site.register(Procedure)
admin.site.register(Master)
admin.site.register(Record)
admin.site.register(Message)
admin.site.register(VacantTimes)
