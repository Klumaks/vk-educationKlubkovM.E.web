import math
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.db.models import Count
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Question, Tag, Answer, User
from app.forms import LoginForm, SignupForm, QuestionForm, AnswerForm, ProfileEditForm


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
            'user': self.request.user if hasattr(self.request, 'user') else None,
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

        answer_form = AnswerForm()

        context.update(self.get_base_context())
        context['question'] = question
        context['answers'] = paginated_answers
        context['answers_count'] = count_answers
        context['answers_max_page'] = max_page
        context['answers_pages'] = range(1, int(max_page) + 1)
        context['page'] = page
        context['answer_form'] = answer_form

        return context

    def post(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)

        if not request.user.is_authenticated:
            return redirect('app:login') + f'?next={request.path}'

        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            answers_count = Answer.objects.filter(question=question, is_active=True).count()
            answers_per_page = self.ANSWERS_PER_PAGE
            page_with_answer = (answers_count - 1) // answers_per_page + 1
            return redirect(f"/question/{question_id}/?page={page_with_answer}#answer-{answer.id}")

        context = self.get_context_data(**kwargs)
        context['answer_form'] = form
        return render(request, self.template_name, context)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Sorry, wrong password!')
    else:
        form = LoginForm()

    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
    best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data.get('nickname', '')
            )
            login(request, user)
            return redirect('app:index')
        else:
            messages.error(request, 'Sorry, this email address already registered!')
    else:
        form = SignupForm(initial={
            'username': 'dr_pepper',
            'email': 'drpepper@mail.ru',
            'nickname': 'Dr. Pepper'
        })

    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
    best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'signup.html', context)


@login_required
def logout_view(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('app:profile_edit')
    else:
        form = ProfileEditForm(instance=request.user)

    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
    best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'profile_edit.html', context)


@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            tags_list = form.cleaned_data.get('tags', [])
            for tag_name in tags_list:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)

            return redirect('app:question', question_id=question.id)
    else:
        form = QuestionForm()

    popular_tags = Tag.objects.annotate(question_count=Count('question')).order_by('-question_count')[:15]
    best_members = User.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]

    context = {
        'popular_tags': popular_tags,
        'best_members': best_members,
        'form': form,
    }
    return render(request, 'ask.html', context)
