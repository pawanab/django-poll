from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

# Create your views here.


class IndexView(generic.ListView):
    # default template <app name>/<model name>_list.html
    template_name = 'pollsapp/index.html'
    # default context object name <model_name>_list ie question_list
    context_object_name = 'latest_questions'

    # template = loader.get_template('pollsapp/index.html')
    # return HttpResponse(template.render(context, request))
    def get_queryset(self):
        return Question.objects.order_by('-publish_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    # default <app name>/<model name>_detail.html
    template_name = 'pollsapp/detail.html'


class ResultView(generic.DetailView):
    model = Question
    template_name = 'pollsapp/result.html'


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
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
