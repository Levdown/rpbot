from django.contrib import admin
from .models import Video, Profile, Message
from .forms import VideoForm, ProfileForm
from bot.management.commands.tbot import bot_mailing

# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'discription', 'url_video', 'video')
    form = VideoForm

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", 'text', 'photo')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm
    actions = ['publish']

    def publish(self, request, queryset):
        bot_mailing(ids=Profile.objects.all(),
                    m_message=Message.objects.get(id=1).text, image=Message.objects.get(id=1).photo)

    print("что-то")
    publish.short_description = "Разослать"
    publish.allowed_permissions = ('change',)