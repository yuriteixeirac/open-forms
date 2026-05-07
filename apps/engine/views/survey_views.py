from django.shortcuts import render


def survey_creation(request):
    return render(request, 'engine/survey-creation.html')
