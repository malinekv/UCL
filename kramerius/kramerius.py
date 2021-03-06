#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# kramerius5.nkp.cz
# digitalniknihovna.cz/mzk
# kramerius.lib.cas.cz
#
# Kramerius grab & link
#

from __future__ import print_function

import requests,json,time

# 0009-0468 Česká literatura
# Ceska literatura uuid:f9f595d7-4116-11e1-99e8-005056a60003
#
# [ {
#     'volume_year' : volume_year,
#     'volume_number' : volume_number,
#     'volume_pid' : volume_pid,
#     'issue' : [
#                  {
#                    'issue_date' : issue_date
#                    'issue_pid' : issue_pid
#	             'page' : {
#                                page_name : page_pid
#                                ......
#                             }
#                  }
#                  ......
#               ]
#   }
#   ......
# ]
#

CESLIT='uuid:f9f595d7-4116-11e1-99e8-005056a60003'

DATA=[]
VOLUME_INDEX=0
ISSUE_INDEX=0

session = requests.Session()

req = session.get('https://kramerius.lib.cas.cz/search/api/v5.0/item/' + CESLIT + '/children')
if req.status_code == 200:
	# VOLUUME
	for volume in json.loads(req.text, strict=False):
		volume_year = volume['details']['year']
		volume_number = volume['details']['volumeNumber']
		volume_pid = volume['pid']
		DATA.append({
				'volume_year':volume_year,
				'volume_number':volume_number,
				'volume_pid':volume_pid,
				'issue':[]
		})
		print('volume: ' + volume_pid)
		req = session.get('https://kramerius.lib.cas.cz/search/api/v5.0/item/' + volume_pid + '/children')
		if req.status_code == 200:
			# ISSUE
			for issue in json.loads(req.text, strict=False):
				if issue['model'] != 'periodicalitem': continue# skip index listing page
				issue_date = issue['details']['date']
				issue_pid = issue['pid']
				DATA[VOLUME_INDEX]['issue'].append({
					'issue_date':issue_date,
					'issue_pid':issue_pid,
					'page':{}
				})
				print('   issue: ' + issue_pid)
				req = session.get('https://kramerius.lib.cas.cz/search/api/v5.0/item/' + issue_pid + '/children')
				if req.status_code == 200:
					# PAGE
					for page in json.loads(req.text, strict=False):
						page_name = page['title']
						page_pid = page['pid']
						DATA[VOLUME_INDEX]['issue'][ISSUE_INDEX]['page'][page_name] = page_pid
				# update indexes
				ISSUE_INDEX+=1
		# update /reset indexes
		VOLUME_INDEX+=1
		ISSUE_INDEX=0
		time.sleep(1)

with open('ceslit.json', 'w') as ceslit:
	ceslit.write(json.dumps(DATA))

