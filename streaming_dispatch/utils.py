import requests
import random
import string

from .models import StreamingServer

key_length = 20

def push_stream_to_server(stream):
  server = random.SystemRandom().choice(StreamingServer.objects.all())
  key = ''.join(random.SystemRandom().choice(string.letters + string.digits)
      for _ in range(key_length))
  r = requests.post('http://' + server.url + ':8081/add',
      data = {'name': str(stream.id), 'key': key})
  if r.status_code != 200:
    return False
  stream.server = server
  stream.key = key
  stream.save()
  return True
