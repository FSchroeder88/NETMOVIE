from django.shortcuts import render
from .models import Video
from .forms import VideoForm




def video(request):
    movies = Video.objects.all()
    return render(request, 'video.html', context={'movies': movies}) 
# Create your views here.


def showvideo(request):

    allvideos= Video.objects.all()

    video_file= allvideos.videofile


    form= VideoForm(request.POST)
    if form.is_valid():
        form.save()

    
    context= {'video_file': video_file,
              'form': form
              }
    
      
    return render(request, 'video.html', context)


