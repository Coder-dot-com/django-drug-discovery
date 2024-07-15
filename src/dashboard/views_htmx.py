from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import UserFeedback
# Create your views here.

@login_required
def add_feedback_htmx(request):
    user = request.user

    feedback = request.POST['feedback']
    UserFeedback.objects.create(user=user, feedback=feedback)

    return HttpResponse("Feedback submitted. Thank you! Refresh the page to submit again")

