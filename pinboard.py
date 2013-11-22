#!/usr/bin/python

from xml.etree import ElementTree as ET
import urllib, urllib2, json
import glob
import re
import time, calendar

def list(TOKEN, CACHETIME, QUERY = ""):
	# CHECK FOR RECENCY
	t = 0
	if not CACHETIME == 0:
		try:
			with open('timestamp.txt') as f:
				t = f.read()
			f.close()
			if int(t) < 1:
				f = open('timestamp.txt', 'w')
				f.write(`calendar.timegm(time.gmtime())`)
				f.close()
		except IOError:
			f = open('timestamp.txt', 'w')
			t = calendar.timegm(time.gmtime())
			f.write(`t`)
			f.close()
	# PARSE ITEMS
	xml = []
	if calendar.timegm(time.gmtime()) - int(t) > CACHETIME or abs(calendar.timegm(time.gmtime()) - int(t)) < 5 or CACHETIME == 0:
		# GET JSON DATA
		url = 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=' + TOKEN
		response = urllib2.urlopen(url)
		response_items = response.read()
		items = json.loads(response_items)
		for i in range(len(items)-1):
			item = items[i]
			if not CACHETIME == 0:
				try:
					with open('bookmarks/' + item[u'time'] + '.txt') as f:
						pass
					f.close()
				except IOError:
					f = open('bookmarks/' + item[u'time'] + '.txt', 'w')
					f.write(item[u'description'].encode('utf8') + '\t' + item[u'extended'].encode('utf8') + '\t' + item[u'href'].encode('utf8') + '\t' + item[u'tags'].encode('utf8'))
					f.close()
			if re.search(re.compile(QUERY, re.IGNORECASE), item[u'description']) or re.search(re.compile(QUERY, re.IGNORECASE), item[u'extended']) or re.search(re.compile(QUERY, re.IGNORECASE), item[u'tags']):
				subtitletext = item[u'extended'] + " | " + item[u'tags'] if not item[u'extended'] == "" else item[u'tags']
				xml.append ({
					'title': item[u'description'],
					'subtitle': subtitletext,
					'arg': item[u'href'],
					'icon': 'blue-' + `100-(10*i/len(items))*10` + '.png'
				})
	else:
		# READ BOOKMARKS FROM DISK
		items = []
		for h in glob.glob('bookmarks/*.txt'):
			with open(h) as f:
				t = f.read()
			f.close()
			t = t.split('\t')
			items.append(t)
		items = items[::-1]
		for i in range(len(items)-1):
			item = items[i]
			if re.search(re.compile(QUERY, re.IGNORECASE), item[0]) or re.search(re.compile(QUERY, re.IGNORECASE), item[1]) or re.search(re.compile(QUERY, re.IGNORECASE), item[3]):
				subtitletext = item[1] + " | " + item[3] if not item[1] == "" else item[3]
				xml.append({
					'title': item[0].decode('utf8'),
					'subtitle': subtitletext.decode('utf8'),
					'arg': item[2].decode('utf8'),
					'icon': 'blue-' + `100-(10*i/len(items))*10` + '.png'
				})
	# PLANT XML TREE
	xml_items = ET.Element('items')
	for item in xml:
		xml_item = ET.SubElement(xml_items, 'item')
		for key in item.keys():
			if key is 'uid' or key is 'arg':
				xml_item.set(key, item[key])
			else:
				child = ET.SubElement(xml_item, key)
				child.text = item[key]
	return ET.tostring(xml_items)