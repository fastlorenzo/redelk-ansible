require 'net/http'
require 'uri'
require 'json'

def filter(event)
  url = 'http://api.greynoise.io:8888/v1/query/ip'
  uri = URI.parse(url)
  response = Net::HTTP.post_form(uri, {'ip' => event.get('src_ip')})
  # response = Net::HTTP.post_form(uri, {'ip' => '211.35.227.240'})
  http = Net::HTTP.new(uri.host, uri.port)
  res = JSON.parse(response.body)

  if res['status'] == 'ok'
    fr = {}
    event.tag('greynoise_found')
    tags = Array.new
    $i = 0
    tor = false
    asn = ''
    org = ''
    os = ''
    intention = []
    confidence = []
    category = []

    res['records'] = res['records'].sort_by {|obj| obj['last_updated']}
    fr['last_updated'] = res['records'][res['returned_count']-1]['last_updated']

    res['records'] = res['records'].sort_by {|obj| obj['first_seen']}
    fr['first_seen'] = res['records'][0]['first_seen']

    while $i < res['returned_count']
      r = res['records'][$i]
      tags.push(r['name'])
      intention.push(r['intention'])
      confidence.push(r['confidence'])
      category.push(r['category'])

      tor = r['metadata']['tor'] if tor == false
      asn = r['metadata']['asn'] if asn == ''
      org = r['metadata']['org'] if org == ''
      os = r['metadata']['os'] if os == ''

      $i += 1
    end
    fr['tor'] = tor
    fr['asn'] = asn
    fr['org'] = org
    fr['os'] = os
    fr['intention'] = intention
    fr['confidence'] = confidence
    fr['category'] = category

    event.set('greynoise_tags', tags)
    event.set('iplist', 'greynoise_found')
    event.set('greynoise', fr)
  elsif res['status'] == 'unknown'
    event.tag('greynoise_unknown')
    event.set('iplist','greynoise_unknown')
  end
  return [event]
end
#
# test_evt = {}
# filter(test_evt)
