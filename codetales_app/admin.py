from django.contrib import admin
from .models import Feedback, AdminRegistration, CStory,Puzzle,PyStory, Profile

admin.site.register(Feedback)
admin.site.register(Profile)
admin.site.register(AdminRegistration)
admin.site.register(CStory)
admin.site.register(PyStory)
admin.site.register(Puzzle)