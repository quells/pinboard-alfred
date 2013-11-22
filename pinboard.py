#!/usr/bin/python

from xml.etree import ElementTree as ET
import urllib, urllib2, json
import glob
import re
import time, calendar

def download(TOKEN, XML, BOOKMARKS, QUERY = ""):
	url = 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=' + TOKEN
	response = urllib2.urlopen(url)
	response_items = response.read()
	items = json.loads(response_items)
	for i in range(len(items)-1):
		item = items[i]
		BOOKMARKS += item[u'description'].encode('utf8') + '\t' + item[u'extended'].encode('utf8') + '\t' + item[u'href'].encode('utf8') + '\t' + item[u'tags'].encode('utf8') + '\n'
		if re.search(re.compile(QUERY, re.IGNORECASE), item[u'description']) or re.search(re.compile(QUERY, re.IGNORECASE), item[u'extended']) or re.search(re.compile(QUERY, re.IGNORECASE), item[u'tags']):
			subtitletext = item[u'extended'] + " | " + item[u'tags'] if not item[u'extended'] == "" else item[u'tags']
			XML.append ({
				'title': item[u'description'],
				'subtitle': subtitletext,
				'arg': item[u'href'],
				'icon': 'blue-' + `100-(10*i/len(items))*10` + '.png'
			})
	return [BOOKMARKS, XML]

def list(TOKEN, CACHETIME, QUERY = ""):
	xml = []
	t = 0
	b = ''
	currentTime = calendar.timegm(time.gmtime())
	if not CACHETIME == 0:
		# CHECK FOR RECENCY
		try:
			with open('bookmarks.txt') as f:
				t = int(f.readline())
			f.close()
		except IOError:
			t = currentTime
	# PARSE ITEMS
	if not QUERY == "":
		xml.append ({
					'title': 'Search for ' + `QUERY`,
					'arg': 'https://pinboard.in/search/u:' + TOKEN.split(':')[0] + '?query=' + QUERY.replace(' ', '+') + '&fulltext=on',
					'icon': 'icon.png'
				})
	if currentTime - t > CACHETIME or abs(currentTime - t) < 5 or CACHETIME == 0:
		# GET JSON DATA
		b = `t` + '\n'
		(b, xml) = download(TOKEN, xml, b, QUERY)
		if not CACHETIME == 0:
			f = open('bookmarks.txt', 'w')
			f.write(b)
			f.close
	else:
		# READ BOOKMARKS FROM DISK
		items = []
		try:
			f = open('bookmarks.txt', 'r')
			b = f.read()
			f.close()
			items = b.split('\n')
			del items[0]
		except IOError:
			# GET JSON DATA
			b = `t` + '\n'
			(b, xml) = download(TOKEN, xml, b, QUERY)
			if not CACHETIME == 0:
				f = open('bookmarks.txt', 'w')
				f.write(b)
				f.close
			items = b.split('\n')
		for i in range(len(items)-1):
			item = items[i].split('\t')
			if re.search(re.compile(QUERY, re.IGNORECASE), item[0]) or re.search(re.compile(QUERY, re.IGNORECASE), item[1]) or re.search(re.compile(QUERY, re.IGNORECASE), item[3]):
				try:
					subtitletext = item[1] + " | " + item[3] if not item[1] == "" else item[3]
				except IndexError:
					subtitletext = item[1]
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