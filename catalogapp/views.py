from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Good, Category

def show_catalog(request):

	context = {}

	if request.method == 'GET':

		params = False

		if request.GET.get('data') or request.GET.get('sorting'):

			params = True

			str_active_params = '?'

			if request.GET.get('data'):
				
				data = request.GET.get('data').strip()

				context.update({'search_data': data})

				if data:
					goods = Good.objects.filter(is_active=True, title__contains=data.upper())
					str_active_params += 'data=' + data +'&'

				else:
					goods = Good.objects.filter(is_active=True)

			sorting = request.GET.get('sorting')

			if sorting:
				str_active_params += 'sorting=' + sorting +'&'
				if sorting == 'cheap':
					goods = Good.objects.filter(is_active=True).order_by('price')
					context.update({'sorting': 'Сначала дешевые'})
				elif 	sorting == 'expensive':
					goods = Good.objects.filter(is_active=True).order_by('-price')
					context.update({'sorting': 'Сначала дорогие'})
				elif 	sorting == 'new':
					goods = Good.objects.filter(is_active=True).order_by('-pk')
					context.update({'sorting': 'Новинки'})

			context.update({'str_active_params':str_active_params})

		else:
			
			goods = Good.objects.filter(is_active=True)			

		goods_count=18

		page_number = request.GET.get('page', 1)

		paginator = Paginator(goods, goods_count)	

		page = paginator.get_page(page_number)

		if params:
			last_url = '{1}page={0}'.format(paginator.num_pages, str_active_params)
		else:
			last_url = '?page={}'.format(paginator.num_pages)

		if params:
			first_url = '{1}page={0}'.format(1, str_active_params)
		else:				
			first_url = '?page={}'.format(1)	

		is_paginated = page.has_other_pages()

		if page.has_previous():
			if params:
				prev_url = '{1}page={0}'.format(page.previous_page_number(), str_active_params)
			else:
				prev_url = '?page={}'.format(page.previous_page_number())
		else:
			prev_url = ''	

		if page.has_next():
			if params:
				next_url = '{1}page={0}'.format(page.next_page_number(), str_active_params)
			else:	
				next_url = '?page={}'.format(page.next_page_number())
		else:
			next_url = ''

		categories = Category.objects.all()

		top_rated = Good.objects.filter(is_active=True).order_by('?')[:5]


		context.update({
			'page_object': page,
			'prev_url': prev_url,
			'next_url': next_url,
			'is_paginated': is_paginated,
			'categories': categories,
			'top_rated': top_rated,
		})

		if (paginator.num_pages - page.number) > 2 :
			context.update({
				'last_page' : paginator.num_pages,
				'last_url' : last_url
				})

		if (page.number - 1) > 2 :
			context.update({
				'first_page' : 1,
				'first_url' : first_url
				})

		return  render(request, 'catalogapp/catalog.html', context)


def show_good(request, cpu_slug):

	good = Good.objects.filter(cpu_slug=cpu_slug).first()
	similar_products = Good.objects.filter(is_active=True).order_by('?')[:4]

	context = {
		'good': good,
		'similar_products': similar_products,
	}

	return render(request, 'catalogapp/good.html', context)
