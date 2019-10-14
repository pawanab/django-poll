from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

# Create your views here.


def index(request):
    latest_question = Question.objects.order_by('-publish_date')[:5]

    # template = loader.get_template('pollsapp/index.html')
    context = {
        'latest_questions': latest_question
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'pollsapp/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exists.')
    return render(request, 'pollsapp/detail.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pollsapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })

    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('pollsapp:result', args=(question.id,)))


def result(request, question_id):
    return HttpResponse('You are looking at the result of question %s' % question_id)
