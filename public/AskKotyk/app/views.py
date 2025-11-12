
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page', 1)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return objects

def index(request):
    questions = []
    for i in range(1, 30):
        questions.append({
            'title': f'How to build a moon park? #{i}',
            'id': i,
            'text': f'Guys, i have trouble with a moon park. Can\'t find the black-jack... Question {i}',
            'tags': ['python', 'django', 'moon'],
            'author': f'user{i}',
            'votes': 42 - i
        })

    paginated_questions = paginate(questions, request, 5)

    context = {
        'questions': paginated_questions,
        'page_title': 'New Questions',
        'popular_tags': ['perl', 'python', 'Technopark', 'MySQL', 'django'],
        'best_members': ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok'],
    }
    return render(request, 'index.html', context)

def hot_questions(request):
    questions = []
    for i in range(1, 25):
        questions.append({
            'title': f'Hot Question about Python #{i}',
            'id': i,
            'text': f'This is very popular question about Python programming. Question {i}',
            'tags': ['python', 'hot', 'popular'],
            'author': f'user{i}',
            'votes': 50 + i
        })

    paginated_questions = paginate(questions, request, 5)

    context = {
        'questions': paginated_questions,
        'page_title': 'Hot Questions',
        'popular_tags': ['perl', 'python', 'Technopark', 'MySQL', 'django'],
        'best_members': ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok'],
    }
    return render(request, 'index.html', context)

def tag_questions(request, tag_name):
    questions = []
    for i in range(1, 20):
        questions.append({
            'title': f'Question about {tag_name} #{i}',
            'id': i,
            'text': f'This question is specifically about {tag_name}.',
            'tags': [tag_name, 'help', 'question'],
            'author': f'user{i}',
            'votes': 30 + i
        })

    paginated_questions = paginate(questions, request, 5)

    context = {
        'questions': paginated_questions,
        'tag_name': tag_name,
        'page_title': f'Tag: {tag_name}',
        'popular_tags': ['perl', 'python', 'Technopark', 'MySQL', 'django'],
        'best_members': ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok'],
    }
    return render(request, 'tag.html', context)

def question_detail(request, question_id):
    question = {
        'id': question_id,
        'title': f'How to build a moon park? #{question_id}',
        'text': 'Lorem ipsum — dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat.',
        'tags': ['moon', 'park', 'puzzle'],
        'author': 'tech_guru',
        'votes': 42
    }

    answers = []
    authors = ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok', 'Anigilus']
    for i in range(1, 8):
        answers.append({
            'id': i,
            'text': f'First of all I would like to thank you for the invitation... Answer #{i}',
            'author': authors[i % len(authors)],
            'votes': 15 - i,
            'is_correct': i == 1
        })

    paginated_answers = paginate(answers, request, 3)

    context = {
        'question': question,
        'answers': paginated_answers,
        'popular_tags': ['perl', 'python', 'Technopark', 'MySQL', 'django'],
        'best_members': ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok'],
    }
    return render(request, 'question.html', context)

def login_view(request):
    context = {
        'popular_tags': ['perl', 'python', 'Technopark', 'MySQL', 'django'],
        'best_members': ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok'],
    }
    return render(request, 'login.html', context)

def signup_view(request):
    context = {
        'popular_tags': ['perl', 'python', 'Technopark', 'MySQL', 'django'],
        'best_members': ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok'],
    }
    return render(request, 'signup.html', context)

def ask_question(request):
    if request.method == 'POST':
        return redirect('app:index')

    context = {
        'popular_tags': ['perl', 'python', 'Technopark', 'MySQL', 'django'],
        'best_members': ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok'],
    }
    return render(request, 'ask.html', context)
