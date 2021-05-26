from django.shortcuts import render
from catalogapp.models import Category, Good
from django.core.paginator import Paginator

def show_category(request, cpu_slug):

	category = Category.objects.filter(cpu_slug=cpu_slug).first()

	context = {}

	if request.method == 'GET':

		params = False

		if request.GET.get('data') or request.GET.get('sorting'):

			params = True

			str_active_params = '?'

			data = request.GET.get('data')

			context.update({'search_data': data})

			if data:
				goods = Good.objects.filter(is_active=True, title__contains=data.upper())
				str_active_params += 'data=' + data +'&'

			else:
				goods = Good.objects.filter(is_active=True, category=category)

			sorting = request.GET.get('sorting')

			if sorting:
				str_active_params += 'sorting=' + sorting +'&'
				if sorting == 'cheap':
					goods = Good.objects.filter(is_active=True, category=category).order_by('price')
					context.update({'sorting': 'Сначала дешевые'})
				elif 	sorting == 'expensive':
					goods = Good.objects.filter(is_active=True, category=category).order_by('-price')
					context.update({'sorting': 'Сначала дорогие'})
				elif 	sorting == 'new':
					goods = Good.objects.filter(is_active=True, category=category).order_by('-pk')
					context.update({'sorting': 'Новинки'})

			context.update({'str_active_params':str_active_params})

		else:	

			goods = Good.objects.filter(is_active=True, category=category)


		goods_count=9

		page_number = request.GET.get('page', 1)

		paginator = Paginator(goods, goods_count)	

		page = paginator.get_page(page_number)

		if params:
			last_url = '{1}page={0}'.format(paginator.num_pages, str_active_params)
		else:				
			last_url = '?page={}'.format(paginator.num_pages)

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
				next_url = '{1}page={0}'.format(page.previous_page_number(), str_active_params)
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
			'last_page' : paginator.num_pages,
			'last_url' : last_url,
			'categories': categories,
			'top_rated': top_rated,
			'category': category,
		})
		
		return render(request, 'categoryapp/category.html', context)