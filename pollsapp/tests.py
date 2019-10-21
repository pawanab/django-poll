import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question, Choice
# Create your tests here.


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(publish_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(publish_date=time)

        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now()
        recent_question = Question(publish_date=time)

        self.assertIs(recent_question.was_published_recently(), True)


def createQuestion(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
   """
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text,
                                   publish_date=time)


class QuestoinIndexViewTest(TestCase):

    def test_no_question(self):
        """
           If no questions exist, an appropriate message is displayed.
       """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_questions'], '')

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        createQuestion(question_text='Past Question.', days=-30)
        resposne = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(resposne.context['latest_questions'], [
                                 '<Question: Past Question.>'])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        createQuestion(question_text='Future Question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_questions'], [])
        self.assertContains(response, 'No polls are available.')

    def test_past_and_future_question(self):
        """
       Even if both past and future questions exist, only past questions
       are displayed.
       """
        createQuestion(question_text='Past Question.', days=-30)
        createQuestion(question_text='Future Question.', days=30)

        resposne = self.client.get(reverse('polls:index'))

        self.assertEqual(resposne.status_code, 200)
        self.assertQuerysetEqual(resposne.context['latest_questions'], [
                                 '<Question: Past Question.>'])
        self.assertEqual(len(resposne.context['latest_questions']), 1)

    def test_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        createQuestion(question_text='first past question', days=-10)
        createQuestion(question_text='second past question', days=-15)

        response = self.client.get(reverse('polls:index'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions'],
                                 ['<Question: first past question>',
                                  '<Question: second past question>']
                                 )
        self.assertEqual(len(response.context['latest_questions']), 2)


class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_ques = createQuestion(question_text='Future Question.', days=5)

        url = reverse('polls:detail', args=(future_ques.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
       The detail view of a question with a pub_date in the past
       displays the question's text.
       """
        past_ques = createQuestion(question_text='Past Questoin.', days=-5)

        url = reverse('polls:detail', args=(past_ques.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_ques.question_text)


class QuestionResultViewTests(TestCase):

    def test_question_with_no_choice(self):
        """
        The result view of a question with a no choice
        in the requested questoin
        returns a 404 not found.
        """
        ques = createQuestion(
            question_text='Valid question with no choice', days=-1)
        url = reverse('polls:result', args=(ques.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_question_with_choice(self):
        """
        The result view of a question with atleast one choice
        in the requested questoin
        display question_text
        """
        ques = createQuestion(
            question_text="Question with one choice", days=-1)
        choice = Choice.objects.create(
            question=ques, choice_text='i am a choice.')

        response = self.client.get(reverse('polls:result', args=(ques.id,)))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Question with one choice')
