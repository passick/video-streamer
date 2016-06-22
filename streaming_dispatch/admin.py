from django.contrib import admin

from .models import Stream, StreamingServer

admin.site.register(Stream)
admin.site.register(StreamingServer)

class StreamingServerAdmin(admin.ModelAdmin):
  def has_delete_permission(self, request, obj=None):
    return False

  def get_actions(self, request):
    actions = super(StreamingServerAdmin, self).get_actions(request)
    if 'delete_selected' in actions:
      del actions['delete_selected']
    return actions
