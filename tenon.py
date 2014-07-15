import urllib

def get_results(tenon_url, params):
  params = urllib.urlencode(params)
  connection = urllib.urlopen(tenon_url, params)
  return connection.read()
