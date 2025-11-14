import math
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.db.models import Count
from app.models import Question, Tag, Answer, User

class PaginatedView:
    QUESTIONS_PER_PAGE = 5

    def paginate_questions(self, questions, page):
        count_questions = questions.count()
        max_page = math.ceil(count_questions / self.QUESTIONS_PER_PAGE)

        if page == 1:
            paginated_questions = questions[0:self.QUESTIONS_PER_PAGE]
        else:
            start_idx = (page - 1) * self.QUESTIONS_PER_PAGE
            end_idx = start_idx + self.QUESTIONS_PER_PAGE
            paginated_questions = questions[start_idx:end_idx]

        return {
            'questions': paginated_questions,
            'count_questions': count_questions,
            'max_page': max_page,
            'pages': range(1, int(max_page) + 1),
        }

class BaseView(TemplateView):
    def get_base_context(self):
        popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
        best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

        return {
            'popular_tags': popular_tags,
            'best_members': best_members,
        }

class IndexView(BaseView, PaginatedView):
    template_name = 'index.html'
    http_method_names = ['get',]

    def get_questions(self):
        return Question.objects.new_questions()\
            .select_related('author')\
            .prefetch_related('tags')\
            .annotate(answers_count=Count('answers'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        questions = self.get_questions()
        pagination_data = self.paginate_questions(questions, page)

        context.update(pagination_data)
        context.update(self.get_base_context())
        context['page_title'] = 'New Questions'
        context['page'] = page

        return context

class HotQuestionsView(BaseView, PaginatedView):
    template_name = 'index.html'

    def get_questions(self):
        return Question.objects.hot_questions()\
            .select_related('author')\
            .prefetch_related('tags')\
            .annotate(answers_count=Count('answers'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = int(self.request.GET.get('page', 1))

        questions = self.get_questions()
        pagination_data = self.paginate_questions(questions, page)

        context.update(pagination_data)
        context.update(self.get_base_context())
        context['page_title'] = 'Hot Questions'
        context['page'] = page

        return context

class TagQuestionsView(BaseView, PaginatedView):
    template_name = 'tag.html'

    def get_questions(self, tag_name):
        return Question.objects.with_tag(tag_name)\
            .select_related('author')\
            .prefetch_related('tags')\
            .annotate(answers_count=Count('answers'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = kwargs.get('tag_name')
        page = int(self.request.GET.get('page', 1))

        tag = get_object_or_404(Tag, name=tag_name)

        questions = self.get_questions(tag_name)
        pagination_data = self.paginate_questions(questions, page)

        context.update(pagination_data)
        context.update(self.get_base_context())
        context['tag_name'] = tag_name
        context['page_title'] = f'Tag: {tag_name}'
        context['page'] = page

        return context

class QuestionDetailView(BaseView, PaginatedView):
    template_name = 'question.html'
    ANSWERS_PER_PAGE = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_id = kwargs.get('question_id')
        page = int(self.request.GET.get('page', 1))

        question = get_object_or_404(
            Question.objects\
                .select_related('author')\
                .prefetch_related('tags'),
            id=question_id
        )

        answers = Answer.objects.filter(
            question=question,
            is_active=True
        ).select_related('author').order_by('-is_correct', '-created_at')

        count_answers = answers.count()
        max_page = math.ceil(count_answers / self.ANSWERS_PER_PAGE)

        if page == 1:
            paginated_answers = answers[0:self.ANSWERS_PER_PAGE]
        else:
            start_idx = (page - 1) * self.ANSWERS_PER_PAGE
            end_idx = start_idx + self.ANSWERS_PER_PAGE
            paginated_answers = answers[start_idx:end_idx]

        context.update(self.get_base_context())
        context['question'] = question
        context['answers'] = paginated_answers
        context['answers_count'] = count_answers
        context['answers_max_page'] = max_page
        context['answers_pages'] = range(1, int(max_page) + 1)
        context['page'] = page

        return context

def login_view(request):
    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
    best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'login.html', context)

def signup_view(request):
    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
    best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'signup.html', context)

def ask_question(request):
    if request.method == 'POST':
        return redirect('app:index')

    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
    best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }
    return render(request, 'ask.html', context)
