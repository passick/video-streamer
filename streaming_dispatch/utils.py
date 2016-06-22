import requests
import random
import string

server_ips = ['188.166.151.75']
key_length = 20

def push_stream_to_server(stream):
  server_ip = random.SystemRandom().choice(server_ips)
  key = ''.join(random.SystemRandom().choice(string.letters + string.digits)
      for _ in range(key_length))
  r = requests.post('http://' + server_ip + ':8081/add',
      data = {'name': str(stream.id), 'key': key})
  if r.status_code != 200:
    return False
  stream.server = server_ip
  stream.key = key
  stream.save()
  return True

def get_stream_viewer_url(stream):
  return "rtmp://" + stream.server + "/mytv/" + str(stream.id)

def get_dash_stream_url(stream):
  return "http://" + stream.server + ":8080/dash/" + str(stream.id) + ".mpd"

def get_stream_publisher_url(stream):
  return "rtmp://" + stream.server + "/mytv/" + str(stream.id) + "?key=" + stream.key
