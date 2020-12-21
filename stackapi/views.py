import json
import requests
import datetime

from django.shortcuts import render
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from stackapi.utils import get_client_ip
from stackapi.models import StackAPI


class SearchView(APIView):

	def get(self, request, *args, **kwargs):
		ip = get_client_ip(request)
		now = timezone.now()
		q = request.GET.get('q')
		limit = request.GET.get('limit', 5)
		offset = request.GET.get('offset', 0)
		obj = StackAPI.objects.filter(ip=ip).first()
		time = obj.date + timezone.timedelta(minutes=1)
		if cache.get(obj.id) and cache.get(obj.id) > 5:
			return Response(data={'message': 'your limit exceeded, please try after some time'},
				status=status.HTTP_400_BAD_REQUEST)
		cache_count = cache.get(obj.id) if cache.get(obj.id) else 0
		cache.set(obj.id, cache_count + 1, 60)
		if StackAPI.objects.filter(ip=ip).exists():
			obj = StackAPI.objects.filter(ip=ip).first()
			if obj.count > 100 and obj.date.date() == now.date():
				return Response(data={'message': 'your daily limit exceeded'},
					status=status.HTTP_400_BAD_REQUEST)
			else:
				obj.count += 1
				obj.save()
		else:
			StackAPI.objects.create(ip=ip, count=1, date=now)
		print(cache.get(ip+ '_query'))
		if cache.get(ip+ '_query') and cache.get(ip+ '_query') == q:
			req = cache.get(ip)
			print('iiiiiiiiiiiiiiii')
		else:
			print('llllllllllllllllllllll')
			url = 'https://api.stackexchange.com/2.2/search/advanced?key={}&site=stackoverflow&order=desc&sort=activity&body={}&filter=default'.format(settings.STACK_APP_KEY, q)
			req = requests.get(url)
			cache.set(ip, req)
			cache.set(ip+ '_query', q)
		result = req.json().get('items')
		print(result)
		total = len(result)
		print(limit, offset, total, type(result))
		return Response(data={
			'total_count': total,
			'next_url': '?limit=' + str(limit) + '?offset=' + str(min(total, offset + limit)),
			'prev_url': '?limit=' + str(limit) + '?offset=' + str(min(0, offset - limit)),
			'result': result[offset:limit+1]
			},
			status=status.HTTP_200_OK)



# https://devcenter.heroku.com/articles/django-memcache
	# https://api.stackexchange.com/docs/questions#order=desc&sort=activity&filter=default&site=stackoverflow
	# http://api.stackexchange.com/docs/questions#order=desc&sort=activity&tagged=ipv4&filter=!BHMIbze0EPheMk572h0ktETsgnphhU&site=stackoverflow&run=true
	# https://api.stackexchange.com/2.2/questions?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&order=desc&sort=activity&filter=default

		# https://api.stackexchange.com/2.2/search/advanced?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&order=desc&sort=activity&body=angular&title=angular&filter=default


		# https://api.stackexchange.com/2.2/search/advanced?key=U4DMV*8nvpm3EOpvf69Rxw((&site=stackoverflow&order=desc&sort=activity&body=python%20list&title=python%20list&filter=default