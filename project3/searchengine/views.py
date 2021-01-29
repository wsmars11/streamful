from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateProfileForm, UpdateUserForm, UpdateFavoriteGames, UpdateFavoriteStreamers
# from isodate import parse_duration
from django.conf import settings

import requests

# Create your views here.
@login_required
def index(request):
    #DEBUG VARIABLE TO SHOW OR HIDE SUGGESTIONS TO SAVE ON YOUTUBE SEARCH QUOTAS
    #TODO: USE ALONG SIDE USER PREFERENCE TO SHOW OR HIDE SUGGESTIONS AT THE START
    showSuggestions = True

    streamer0 = User.objects.get(username=request.user.username).profile.streamer0
    streamer1 = User.objects.get(username=request.user.username).profile.streamer1
    streamer2 = User.objects.get(username=request.user.username).profile.streamer2
    streamer3 = User.objects.get(username=request.user.username).profile.streamer3
    streamer4 = User.objects.get(username=request.user.username).profile.streamer4
    streamer5 = User.objects.get(username=request.user.username).profile.streamer5
    streamer6 = User.objects.get(username=request.user.username).profile.streamer6
    streamer7 = User.objects.get(username=request.user.username).profile.streamer7
    streamer8 = User.objects.get(username=request.user.username).profile.streamer8
    streamer9 = User.objects.get(username=request.user.username).profile.streamer9
    streamers = [streamer0,streamer1,streamer2,streamer3,streamer4,streamer5,streamer6,streamer7,streamer8,streamer9]

    game0 = User.objects.get(username=request.user.username).profile.game0
    game1 = User.objects.get(username=request.user.username).profile.game1
    game2 = User.objects.get(username=request.user.username).profile.game2
    game3 = User.objects.get(username=request.user.username).profile.game3
    game4 = User.objects.get(username=request.user.username).profile.game4
    game5 = User.objects.get(username=request.user.username).profile.game5
    game6 = User.objects.get(username=request.user.username).profile.game6
    game7 = User.objects.get(username=request.user.username).profile.game7
    game8 = User.objects.get(username=request.user.username).profile.game8
    game9 = User.objects.get(username=request.user.username).profile.game9
    games = [game0,game1,game2,game3,game4,game5,game6,game7,game8,game9]

    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    context = {
        'streamers': streamers,
        'games': games,
    }

    suggested_livestreams = []

    fav_streamer_list = []

    fav_game_list = []

    videos = []

    if request.method == 'POST':

       #filter check for source platform
        resultTypes = request.POST.getlist('Filter')

        #If both are unselected, display both instead of an empty page
        if (resultTypes == []):
            resultTypes = ['Youtube', 'Twitch']

        #YOUTUBE RESULTS
        if 'Youtube' in resultTypes:
            search_params = {
                'part': 'snippet',
                'q': request.POST['search'],
                'key': 'AIzaSyALkwmDhtc2FsklXbo9rxVg6BPdpPBnQuo',
                'maxResults': 9,
                'type': 'video'
            }

            r = requests.get(search_url, params=search_params)

            #TODO better error checking the results for quota limits
            results = r.json().get('items',[])

            video_ids = []
            for result in results:
                video_ids.append(result['id']['videoId'])

            video_params = {
                'key': 'AIzaSyALkwmDhtc2FsklXbo9rxVg6BPdpPBnQuo',
                'part': 'snippet,contentDetails',
                'id': ','.join(video_ids),
                'maxResults': 9
            }

            r = requests.get(video_url, params=video_params)

            #TODO better error checking the results for quota limits
            results = r.json().get('items',[])

            for result in results:
                video_data = {
                    'title': result['snippet']['title'] + ' - ' + result['snippet']['channelTitle'],
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={result["id"]}',
                    # 'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail': result['snippet']['thumbnails']['high']['url'],
                    'platform': "YouTube"
                }

                videos.append(video_data)


        # TWITCH RESULTS
        if 'Twitch' in resultTypes:
            MAX_TWITCH_RESULTS = 9
            twitch_url = 'https://api.twitch.tv/kraken/search/streams'
            # twitch_url = 'https://api.twitch.tv/kraken/search/games'
            twitch_headers = {
                'Accept': 'application/vnd.twitchtv.v5+json',
                'Client-ID': 'w145ct9mbr7i76f8yoc2qrq95tjbne',
            }

            twitch_params = {
                'query': request.POST['search'],
                'limit': MAX_TWITCH_RESULTS
            }

            twitch_r = requests.get(twitch_url, headers=twitch_headers, params=twitch_params)

            twitch_streams = twitch_r.json()['streams']

            for stream in twitch_streams:
                video_data = {
                    'title': stream['channel']['status'] + ' - ' + stream['channel']['display_name'],
                    'id': stream['_id'],
                    'url': stream['channel']['url'],
                    'thumbnail': stream['preview']['large'],
                    'currentViews': stream['viewers'],
                    #use template and replace {width} and {height} for custom size
                    # 'template': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_waxxinator-{width}x{height}.jpg'
                    # 'thumbnail': stream['preview']['template']
                    'platform': "Twitch"
                }
                videos.append(video_data)


        context['videos'] = videos
    elif request.method == "GET":
        live_search_params = {
            'part': 'snippet',
            'key': 'AIzaSyALkwmDhtc2FsklXbo9rxVg6BPdpPBnQuo',
            'maxResults': 4,
            'type': 'video',
            'eventType': 'live',
            'order': 'viewCount',
            'topicId': '/m/0bzvm2', # Gaming Category of YT
        }
        if(showSuggestions):
            l = requests.get(search_url, params=live_search_params)

            #TODO better error checking the results for quota limits
            sug_results = l.json().get('items',[])
            for result in sug_results:
                sug_video_data = {
                    'title': result['snippet']['title'] + ' - ' + result['snippet']['channelTitle'],
                    'id': result['id']['videoId'],
                    'url': f'https://www.youtube.com/watch?v={result["id"]["videoId"]}',
                    'thumbnail': result['snippet']['thumbnails']['high']['url'],
                    'platform': 'YouTube',
                    'viewCount': requests.get(video_url,
                        params={'part': 'liveStreamingDetails', 'id': result['id']['videoId'], 'key': 'AIzaSyALkwmDhtc2FsklXbo9rxVg6BPdpPBnQuo'}
                    ).json()['items'][0]['liveStreamingDetails']['concurrentViewers']
                }
                suggested_livestreams.append(sug_video_data)

            context['sug_livestreams'] = suggested_livestreams

        #LIST FAVORITE STREAMERS
        for curStreamer in streamers:
            headers = {
                'Accept' : 'application/vnd.twitchtv.v5+json',
                'Client-ID' : 'w145ct9mbr7i76f8yoc2qrq95tjbne',
            }
            params = {
                'query' : curStreamer,
                'limit' : 1
            }

            response = requests.get('https://api.twitch.tv/kraken/search/channels', headers=headers, params=params)

            thumbnailURL = ''
            try:
                thumbnailURL = response.json()['channels'][0]['logo']
            except IndexError:
                #substitute image if channel logo not found
                thumbnailURL = 'https://sites.google.com/site/authorstudyedgarallanpoe/_/rsrc/1463974077373/works/short-stories/the-pit-and-the-pendulum/the-spanish-inquisition/spanish%20inquisition.jpg?height=250&width=320'
            except KeyError:
                thumbnailURL = 'https://sites.google.com/site/authorstudyedgarallanpoe/_/rsrc/1463974077373/works/short-stories/the-pit-and-the-pendulum/the-spanish-inquisition/spanish%20inquisition.jpg?height=250&width=320'
            streamer_data = {
                'name' : curStreamer,
                'thumbnail' : thumbnailURL
            }
            fav_streamer_list.append(streamer_data)

        context['streamers_list'] = fav_streamer_list

        #LIST FAVORITE GAMES
        for curGame in games:
            headers = {
                'Accept' : 'application/vnd.twitchtv.v5+json',
                'Client-ID' : 'w145ct9mbr7i76f8yoc2qrq95tjbne',
            }
            params = {
                'query' : curGame,
                'limit' : 1,
            }

            response = requests.get('https://api.twitch.tv/kraken/search/games', headers=headers, params=params)
            try:
                thumbnail = response.json()['games'][0]['box']['medium']
            except KeyError:
                thumbnail = 'https://sites.google.com/site/authorstudyedgarallanpoe/_/rsrc/1463974077373/works/short-stories/the-pit-and-the-pendulum/the-spanish-inquisition/spanish%20inquisition.jpg?height=250&width=320'

            game_data = {
                'title' : curGame,
                'thumbnail' : thumbnail
            }
            fav_game_list.append(game_data)

        context['games_list'] = fav_game_list



        #AUDIO ACCESSIBITLIY
        if request.GET.get('read_livestreams'):
            src = 'Your Suggested Live Streams are '
            for ls in suggested_livestreams:
                src += ls['title'] + ','

            audio = {
                'key': 'da314389a1ef4cc4835553360f4f7b92',
                'src': src,
            }
            context['audio_ls'] = audio
        elif request.GET.get('read_streamers'):
            src = 'Your Favorite Streamers are '
            for ls in streamers:
                src += ls + ', '

            audio = {
                'key': 'da314389a1ef4cc4835553360f4f7b92',
                'src': src,
            }
            context['audio_fs'] = audio
        elif request.GET.get('read_games'):
            src = 'Your Favorite Games are '
            for ls in games:
                src += ls + ', '

            audio = {
                'key': 'da314389a1ef4cc4835553360f4f7b92',
                'src': src,
            }
            context['audio_g'] = audio

    return render(request, 'index.html', context)

@login_required
def profile(request):
    # TODO parse favorite streamers and games objects
    streamer0 = User.objects.get(username=request.user.username).profile.streamer0
    streamer1 = User.objects.get(username=request.user.username).profile.streamer1
    streamer2 = User.objects.get(username=request.user.username).profile.streamer2
    streamer3 = User.objects.get(username=request.user.username).profile.streamer3
    streamer4 = User.objects.get(username=request.user.username).profile.streamer4
    streamer5 = User.objects.get(username=request.user.username).profile.streamer5
    streamer6 = User.objects.get(username=request.user.username).profile.streamer6
    streamer7 = User.objects.get(username=request.user.username).profile.streamer7
    streamer8 = User.objects.get(username=request.user.username).profile.streamer8
    streamer9 = User.objects.get(username=request.user.username).profile.streamer9
    streamers = [streamer0,streamer1,streamer2,streamer3,streamer4,streamer5,streamer6,streamer7,streamer8,streamer9]

    game0 = User.objects.get(username=request.user.username).profile.game0
    game1 = User.objects.get(username=request.user.username).profile.game1
    game2 = User.objects.get(username=request.user.username).profile.game2
    game3 = User.objects.get(username=request.user.username).profile.game3
    game4 = User.objects.get(username=request.user.username).profile.game4
    game5 = User.objects.get(username=request.user.username).profile.game5
    game6 = User.objects.get(username=request.user.username).profile.game6
    game7 = User.objects.get(username=request.user.username).profile.game7
    game8 = User.objects.get(username=request.user.username).profile.game8
    game9 = User.objects.get(username=request.user.username).profile.game9
    games = [game0,game1,game2,game3,game4,game5,game6,game7,game8,game9]

    context = {
        'firstname': User.objects.get(username=request.user.username).first_name,
        'lastname': User.objects.get(username=request.user.username).last_name,
        'profile_img': User.objects.get(username=request.user.username).profile.image,
        'bio': User.objects.get(username=request.user.username).profile.bio,
        'username': request.user.username,
        'email' : request.user.email,
        'streamers': streamers,
        'games': games,
    }

    key = 'da314389a1ef4cc4835553360f4f7b92'
    if request.GET.get('read_personal'):
        src = f'Personal Information. Your name is {context["firstname"]} {context["lastname"]}. Your username is {context["username"]}. Your email is {context["email"]}. Your biography reads: {context["bio"]}.'

        audio = {
            'key': key,
            'src': src,
        }
        context['audio_personal'] = audio
    elif request.GET.get('read_pic'):
        src = 'This is your profile picture.'
        # src += 'It seems to be or contain the following: ' # Stretch Goal: image analysis api maybe

        audio = {
            'key': key,
            'src': src,
        }
        context['audio_pic'] = audio
    elif request.GET.get('read_accounts'):
        src = 'These are your connected streaming accounts.'

        audio = {
            'key': key,
            'src': src,
        }
        context['audio_accounts'] = audio

    return render(request, 'profile.html', context)

@login_required
def settings(request):
    if request.method == 'POST':
        if 'pinfo' in request.POST:
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
            user_form = UpdateUserForm(request.POST, instance=request.user)

            if profile_form.is_valid() and user_form.is_valid():
                profile_form.save()
                user_form.save()
                # messages.success(request,'Your Profile has been updated!')
                # return redirect('profile')
        elif 'streamerinfo' in request.POST:
            streamer_form = UpdateFavoriteStreamers(request.POST, instance=request.user.profile)

            if streamer_form.is_valid():
                streamer_form.save()

        elif 'gameinfo' in request.POST:
            game_form = UpdateFavoriteGames(request.POST, instance=request.user.profile)
            if game_form.is_valid():
                game_form.save()

        elif 'cpass' in request.POST:
            cpass_form = PasswordChangeForm(request.user, request.POST)
            if cpass_form.is_valid():
                user = cpass_form.save()
                update_session_auth_hash(request, user)

    profile_form = UpdateProfileForm(instance=request.user.profile)
    user_form = UpdateUserForm(instance=request.user)
    changepass_form = PasswordChangeForm(request.user)

    streamer0 = User.objects.get(username=request.user.username).profile.streamer0
    streamer1 = User.objects.get(username=request.user.username).profile.streamer1
    streamer2 = User.objects.get(username=request.user.username).profile.streamer2
    streamer3 = User.objects.get(username=request.user.username).profile.streamer3
    streamer4 = User.objects.get(username=request.user.username).profile.streamer4
    streamer5 = User.objects.get(username=request.user.username).profile.streamer5
    streamer6 = User.objects.get(username=request.user.username).profile.streamer6
    streamer7 = User.objects.get(username=request.user.username).profile.streamer7
    streamer8 = User.objects.get(username=request.user.username).profile.streamer8
    streamer9 = User.objects.get(username=request.user.username).profile.streamer9
    streamers = [streamer0,streamer1,streamer2,streamer3,streamer4,streamer5,streamer6,streamer7,streamer8,streamer9]

    game0 = User.objects.get(username=request.user.username).profile.game0
    game1 = User.objects.get(username=request.user.username).profile.game1
    game2 = User.objects.get(username=request.user.username).profile.game2
    game3 = User.objects.get(username=request.user.username).profile.game3
    game4 = User.objects.get(username=request.user.username).profile.game4
    game5 = User.objects.get(username=request.user.username).profile.game5
    game6 = User.objects.get(username=request.user.username).profile.game6
    game7 = User.objects.get(username=request.user.username).profile.game7
    game8 = User.objects.get(username=request.user.username).profile.game8
    game9 = User.objects.get(username=request.user.username).profile.game9
    games = [game0,game1,game2,game3,game4,game5,game6,game7,game8,game9]

    streamer_form = UpdateFavoriteStreamers(instance=request.user.profile)
    game_form = UpdateFavoriteGames(instance=request.user.profile)

    context = {
        'streamers': streamers,
        'games': games,
        'profile_form': profile_form,
        'user_form': user_form,
        'streamer_form': streamer_form,
        'changepass_form': changepass_form
    }

    return render(request, 'settings.html', context)

def login(request):
    return render(request, 'login.html')

def register(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        user.profile.first_name = form.cleaned_data.get('first_name')
        user.profile.last_name = form.cleaned_data.get('last_name')
        user.profile.email = form.cleaned_data.get('email')
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('index')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'register.html', context)

def forgotpassword(request):
    return render(request, 'forgotpassword.html')


def youtube(request):
    videos = []

    if request.method == 'POST':
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_DATA_API_KEY,
            'maxResults': 9,
            'type': 'video'
        }

        r = requests.get(search_url, params=search_params)

        results = r.json()['items']

        video_ids = []
        for result in results:
            video_ids.append(result['id']['videoId'])

        if request.POST['submit'] == 'lucky':
            return redirect(f'https://www.youtube.com/watch?v={video_ids[0]}')

        video_params = {
            'key': settings.YOUTUBE_DATA_API_KEY,
            'part': 'snippet,contentDetails',
            'id': ','.join(video_ids),
            'maxResults': 9
        }

        r = requests.get(video_url, params=video_params)

        #TODO better error checking the results for quota limits
        results = r.json().get('items',[])

        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                # 'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                'thumbnail': result['snippet']['thumbnails']['high']['url']
            }

            videos.append(video_data)

    context = {
        'videos': videos
    }

    return render(request, 'youtube.html', context)