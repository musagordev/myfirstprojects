from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Question, Choice
from django.http import Http404
from django.urls import reverse


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    tmp = loader.get_template('poll/index.html')
    ctx={
        'latest_question_list':latest_question_list,
        }
    return HttpResponse(tmp.render(ctx,request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render (request, 'poll/detail.html', {
            'question' : question,
            'error_message' : "You didn't select a choice",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('poll:results', args = (question.id,)))

def owner(request):
   return HttpResponse("Hello, world. 941d7fab is the polls index.")