import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from app.models import Question, Answer, QuestionLike, AnswerLike

@csrf_exempt
@require_POST
@login_required
def vote_question(request):
    """AJAX запрос для лайка/дизлайка вопроса"""
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        vote_type = data.get('vote_type')

        if vote_type not in ['like', 'dislike']:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)

        question = get_object_or_404(Question, id=question_id)
        user = request.user

        try:
            existing_vote = QuestionLike.objects.get(user=user, question=question)
            if (existing_vote.is_like and vote_type == 'like') or \
               (not existing_vote.is_like and vote_type == 'dislike'):
                existing_vote.delete()
                action = 'removed'
            else:
                existing_vote.is_like = (vote_type == 'like')
                existing_vote.save()
                action = 'changed'
        except QuestionLike.DoesNotExist:
            QuestionLike.objects.create(
                user=user,
                question=question,
                is_like=(vote_type == 'like')
            )
            action = 'added'

        likes = question.questionlike_set.filter(is_like=True).count()
        dislikes = question.questionlike_set.filter(is_like=False).count()
        new_votes_count = likes - dislikes

        return JsonResponse({
            'success': True,
            'votes_count': new_votes_count,
            'user_vote': question.user_vote(user),
            'action': action
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
@login_required
def vote_answer(request):
    """AJAX запрос для лайка/дизлайка ответа"""
    try:
        data = json.loads(request.body)
        answer_id = data.get('answer_id')
        vote_type = data.get('vote_type')

        if vote_type not in ['like', 'dislike']:
            return JsonResponse({'error': 'Invalid vote type'}, status=400)

        answer = get_object_or_404(Answer, id=answer_id)
        user = request.user

        try:
            existing_vote = AnswerLike.objects.get(user=user, answer=answer)
            if (existing_vote.is_like and vote_type == 'like') or \
               (not existing_vote.is_like and vote_type == 'dislike'):
                existing_vote.delete()
                action = 'removed'
            else:
                existing_vote.is_like = (vote_type == 'like')
                existing_vote.save()
                action = 'changed'
        except AnswerLike.DoesNotExist:
            AnswerLike.objects.create(
                user=user,
                answer=answer,
                is_like=(vote_type == 'like')
            )
            action = 'added'

        likes = answer.answerlike_set.filter(is_like=True).count()
        dislikes = answer.answerlike_set.filter(is_like=False).count()
        new_votes_count = likes - dislikes

        return JsonResponse({
            'success': True,
            'votes_count': new_votes_count,
            'user_vote': answer.user_vote(user),
            'action': action
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_POST
@login_required
def mark_correct_answer(request):
    """AJAX запрос для отметки правильного ответа"""
    try:
        data = json.loads(request.body)
        answer_id = data.get('answer_id')

        answer = get_object_or_404(Answer, id=answer_id)
        question = answer.question

        if request.user != question.author:
            return JsonResponse({
                'error': 'Only the author of the question can mark correct answer'
            }, status=403)

        if answer.is_correct:
            answer.is_correct = False
            answer.save()
            return JsonResponse({
                'success': True,
                'is_correct': False,
                'message': 'Answer unmarked as correct'
            })
        else:
            Answer.objects.filter(question=question, is_correct=True).update(is_correct=False)
            answer.is_correct = True
            answer.save()
            return JsonResponse({
                'success': True,
                'is_correct': True,
                'message': 'Answer marked as correct'
            })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
