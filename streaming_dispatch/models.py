from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class StreamingServer(models.Model):
  url = models.CharField(max_length=100, null=False, unique=True)

  def __str__(self):
    return self.url

class Stream(models.Model):
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  server = models.ForeignKey(StreamingServer, null=True)
  name = models.CharField(max_length=100)
  start = models.DateTimeField()
  active = models.BooleanField(default=False)
  key = models.CharField(max_length=100, null=True)

  def __str__(self):
    return self.name + (', ' +  self.server.url if self.server else '') + ', ' + \
      ('active' if self.active else 'not active')

  def _get_stream_viewer_url(stream):
    return "rtmp://" + stream.server.url + "/mytv/" + str(stream.id)
  viewer_url = property(_get_stream_viewer_url)

  def _get_dash_stream_url(stream):
    return "http://" + stream.server.url + ":8080/dash/" + str(stream.id) + ".mpd"
  dash_url = property(_get_dash_stream_url)

  def _get_hls_stream_url(stream):
    return "http://" + stream.server.url + ":8080/hls/" + str(stream.id) + ".m3u8"
  hls_url = property(_get_hls_stream_url)

  def _get_stream_publisher_url(stream):
    return "rtmp://" + stream.server.url + "/mytv/" + str(stream.id) + "?key=" + stream.key
  publisher_url = property(_get_stream_publisher_url)

  def _get_screenshot_url(stream):
    return "http://" + stream.server.url + ":8080/images/" + str(stream.id) + ".jpg"
  screen_url = property(_get_screenshot_url)
