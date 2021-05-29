from django.contrib import admin
from .models import Category, Color, Present, Question, Answer, TempUrl


admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Present)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(TempUrl)
