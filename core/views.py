import requests

from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator

from .models import Category, Video, Link, Episode
from users.utils import data_exist, verify_captcha
from users.decorators import admin_required, login_required


class HomeView(View):

    def get(self, request, *args, **kwargs):
        title = request.GET.get('title')
        if title:
            videos = Video.objects.filter(name__contains=title).order_by('-id')
        elif 'category_name' in kwargs:
            videos = Video.objects.filter(approved=True, categories__name=kwargs['category_name']).order_by('-id')
        else:
            videos = Video.objects.filter(approved=True).order_by('-id')

        category_dates = Category.objects.filter(type='date')
        category_languages = Category.objects.filter(type='language')
        category_categories = Category.objects.filter(type='category')

        paginator = Paginator(videos, 10)
        page_num = request.GET.get('page')
        page = paginator.get_page(page_num)

        context = {
            'videos': videos,
            'dates': category_dates,
            'languages': category_languages,
            'categories': category_categories,
            'page': page,
            'title': title  # for search
        }

        return render(request, 'core/index.html', context=context)


class AddVideoView(View):

    def get(self, request, *args, **kwargs):
        category_dates = Category.objects.filter(type='date')
        category_languages = Category.objects.filter(type='language')
        category_categories = Category.objects.filter(type='category')

        context = {
            'dates': category_dates,
            'languages': category_languages,
            'categories': category_categories
        }

        return render(request, 'core/add_video.html', context=context)

    def post(self, request, *args, **kwargs):
        captcha = request.POST.get("g-recaptcha-response")

        if not verify_captcha(captcha):
            messages.add_message(request, messages.ERROR, 'Captcha nie została uzupełniona poprawnie.')
            return redirect('/add_video')

        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.POST.get('image')
        type = request.POST.get('type')
        date = request.POST.get('date')
        categories = request.POST.getlist('categories')

        if not data_exist(name, description, image, type, date, categories):
            messages.add_message(request, messages.ERROR, 'Uzupełnij formularz.')
            return redirect('/add_video')

        date = Category.objects.get(name=date)
        categories_instances = []
        for i in categories:
            categories_instances.append(Category.objects.get(name=i))
        categories_instances.append(date)

        video = Video(
            name=name,
            description=description,
            image=image,
            type=type
        )
        video.save()
        video.categories.add(*categories_instances)

        messages.add_message(request, messages.SUCCESS, 'Materiał został dodany, oczekuje teraz na akceptacje.')
        return redirect('/add_video')


class VideoView(View):

    def get(self, request, video_id, *args, **kwargs):
        video = Video.objects.get(id=video_id)
        languages = Category.objects.filter(type='language')
        links = Link.objects.filter(video__id=video_id, approved=True)

        if video.type == 'Series':
            episodes = Episode.objects.filter(video=video)
            episode = []
            episode_view = False
            if request.GET:
                episode = Episode.objects.filter(video=video, season=request.GET.get('season'), episode=request.GET.get('episode'))[0]
                links = Link.objects.filter(video__id=video_id, approved=True, episode=episode)
                episode_view = True
        else:
            episodes = []
            episode = []
            episode_view = False

        seasons = video.seasons
        if not seasons:
            seasons = 0

        context = {
            'video': video,
            'languages': languages,
            'links': links,
            'seasons': range(1, seasons+1),
            'episodes': episodes,
            'episode': episode,
            'episode_view': episode_view
        }

        return render(request, 'core/video_page.html', context=context)


class AddLinkView(View):

    def post(self, request, *args, **kwargs):
        captcha = request.POST.get("g-recaptcha-response")

        if not verify_captcha(captcha):
            messages.add_message(request, messages.ERROR, 'Captcha nie została uzupełniona poprawnie.')
            return redirect('/')

        service = request.POST.get('service')
        link = request.POST.get('link')
        language = request.POST.get('language')
        quality = request.POST.get('quality')
        video_id = request.POST.get('video_id')

        if not data_exist(service, link, language, quality, video_id):
            messages.add_message(request, messages.ERROR, 'Uzupełnij formularz.')
            return redirect('/')

        language = Category.objects.filter(name=language)[0]
        video = Video.objects.filter(id=video_id)[0]

        if request.POST.get('episode_id'):
            episode = Episode.objects.filter(id=request.POST.get('episode_id'))[0]
        else:
            episode = None

        link = Link(
            service=service,
            url=link,
            language=language,
            quality=quality,
            video=video,
            episode=episode,
            approved=False
        )
        link.save()

        messages.add_message(request, messages.SUCCESS, 'Link został dodany, oczekuje teraz na akceptacje.')
        return redirect('/')


class PanelView(View):

    @method_decorator(login_required())
    @method_decorator(admin_required())
    def get(self, request, *args, **kwargs):
        videos = Video.objects.filter(approved=False)
        links = Link.objects.filter(approved=False)

        context = {
            'videos': videos,
            'links': links
        }

        return render(request, 'core/panel.html', context=context)


class VideoAction(View):

    @method_decorator(login_required())
    @method_decorator(admin_required())
    def post(self, request, *args, **kwargs):
        video_id = request.POST.get('video_id')
        name = request.POST.get('video_name')
        description = request.POST.get('video_description')
        image = request.POST.get('video_image')
        type = request.POST.get('video_type')

        if not data_exist(video_id, name, description, image, type):
            messages.add_message(request, messages.ERROR, 'Uzupełnij formularz.')
            return redirect('/panel')

        if request.POST.get('action') == 'Odrzuć':
            Video.objects.filter(id=video_id).delete()
            messages.add_message(request, messages.INFO, 'Odrzucono.')
            return redirect('/panel')

        video = Video.objects.filter(id=video_id).update(
            name=name,
            description=description,
            image=image,
            type=type,
            approved=True
        )

        messages.add_message(request, messages.SUCCESS, 'Zaakceptowano.')
        return redirect('/panel')


class LinkAction(View):

    @method_decorator(login_required())
    @method_decorator(admin_required())
    def post(self, request, *args, **kwargs):
        link_id = request.POST.get('link_id')
        service = request.POST.get('link_service')
        link_link = request.POST.get('link_link')

        if not data_exist(link_id, service, link_link):
            messages.add_message(request, messages.ERROR, 'Uzupełnij formularz.')
            return redirect('/panel')

        if request.POST.get('action') == 'Odrzuć':
            Link.objects.filter(id=link_id).delete()
            messages.add_message(request, messages.INFO, 'Odrzucono.')
            return redirect('/panel')

        link = Link.objects.filter(id=link_id).update(
            service=service,
            url=link_link,
            approved=True
        )

        messages.add_message(request, messages.SUCCESS, 'Zaakceptowano.')
        return redirect('/panel')


class ActualizeSeriesDataView(View):

    @method_decorator(login_required())
    @method_decorator(admin_required())
    def post(self, request, *args, **kwargs):
        episodate_link = request.POST.get('episodate_link')
        video_id = request.POST.get('video_id')

        if not episodate_link or not video_id:
            messages.add_message(request, messages.ERROR, 'Uzupełnij formularz.')
            return redirect('/')

        video = Video.objects.filter(id=video_id, type='Series')[0]
        if not video:
            messages.add_message(request, messages.ERROR, 'Brak takiego wideo.')
            return redirect('/')

        try:
            r = requests.get(episodate_link).json()
            episodes = r['tvShow']['episodes']
        except:
            messages.add_message(request, messages.ERROR, 'Wystąpił błąd, prawdopodobnie niepoprawny URL.')
            return redirect('/')

        seasons = []
        for episode in episodes:
            Episode.objects.update_or_create(
                video=video,
                season=episode['season'],
                episode=episode['episode'],
                defaults={
                    "title": episode['name']
                }
            )
            seasons.append(int(episode['season']))

        seasons_max = max(seasons)
        Video.objects.filter(id=video_id, type='Series').update(
            seasons=seasons_max
        )

        messages.add_message(request, messages.SUCCESS, 'Zaaktualizowano.')
        return redirect('/')


