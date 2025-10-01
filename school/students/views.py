
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Students
from education.models import Section, Classes, Options


def students_list(request):
	"""
	Vue pour afficher la liste paginée des élèves, avec filtres par section, classe et option.

	Args:
		request (HttpRequest): La requête HTTP reçue.

	Returns:
		HttpResponse: La page HTML affichant la liste filtrée et paginée des élèves.
	"""
	# Récupération des paramètres de filtre depuis la requête GET
	section_id = request.GET.get('section')
	classe_id = request.GET.get('classe')
	option_id = request.GET.get('option')

	# Filtrage de la queryset des élèves selon les filtres sélectionnés
	students = Students.objects.all()
	if section_id:
		students = students.filter(section_id=section_id)
	if classe_id:
		students = students.filter(classe_id=classe_id)
	if option_id:
		students = students.filter(option_id=option_id)

	# Récupération de toutes les sections, classes et options pour les filtres du template
	sections = Section.objects.all()
	classes = Classes.objects.all()
	options = Options.objects.all()

	# Pagination de la liste des élèves (1 élève par page ici, à ajuster si besoin)
	paginator = Paginator(students, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	context = {
		'sections': sections,
		'classes': classes,
		'options': options,
		'page_obj': page_obj,
	}
	return render(request, 'students/students_list.html', context)

