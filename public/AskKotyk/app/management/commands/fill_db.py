import os
import random
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.core.files import File
from app.models import User, Question, Answer, Tag, QuestionLike, AnswerLike

def assign_avatars_to_users():
    """Назначает аватары пользователям"""
    avatars_count = 5
    all_users = User.objects.all()
    
    special_avatars = {
        'Kotyk Kotykov': 1,
        'tech_guru': 2,
        'Murzyk': 3,
        'Pushok': 4,
        'Anigilus': 5
    }

    for user in all_users:
        if not user.avatar:
            if user.username in special_avatars:
                avatar_number = special_avatars[user.username]
            else:
                avatar_number = (user.id % avatars_count) + 1

            avatar_filename = f'avatar{avatar_number}.png'
            avatar_path = os.path.join('static', 'avatars', avatar_filename)

            if os.path.exists(avatar_path):
                with open(avatar_path, 'rb') as f:
                    user.avatar.save(avatar_filename, File(f))
                print(f"Assigned {avatar_filename} to {user.username}")

class Command(BaseCommand):
    help = 'Fill database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Multiplication ratio for data generation')

    def handle(self, *args, **options):
        ratio = options['ratio']

        with transaction.atomic():
            self.stdout.write(f'Generating data with ratio {ratio}...')
            popular_tag_names = ["perl", "python", "TechnoPark", "MySQL", "django",
                               "Mail.Ru", "Voloshin", "Firefox", "moon", "park",
                               "puzzle", "space", "engineering", "javascript", "html",
                               "css", "programming", "web", "development"]

            tags_to_create = []
            for tag_name in popular_tag_names:
                if not Tag.objects.filter(name=tag_name).exists():
                    tags_to_create.append(Tag(name=tag_name))

            existing_tags_count = Tag.objects.count()
            for i in range(max(0, ratio - existing_tags_count)):
                tag_name = f'tag_{i + existing_tags_count}'
                if not Tag.objects.filter(name=tag_name).exists():
                    tags_to_create.append(Tag(name=tag_name))

            if tags_to_create:
                Tag.objects.bulk_create(tags_to_create, batch_size=1000)
                self.stdout.write(f'Created {len(tags_to_create)} tags')

            all_tags = list(Tag.objects.all())

            users_to_create = []
            special_usernames = ['Kotyk Kotykov', 'tech_guru', 'Murzyk', 'Pushok', 'Anigilus']

            for username in special_usernames:
                if not User.objects.filter(username=username).exists():
                    user = User(
                        username=username,
                        email=f'{username.replace(" ", "_").lower()}@example.com',
                        first_name=username.split()[0] if ' ' in username else username,
                        last_name=username.split()[1] if ' ' in username else '',
                        password=make_password('password123')
                    )
                    users_to_create.append(user)

            existing_users_count = User.objects.count()
            users_needed = max(0, ratio - existing_users_count)

            for i in range(users_needed):
                username = f'user_{i + existing_users_count}'
                if not User.objects.filter(username=username).exists():
                    user = User(
                        username=username,
                        email=f'{username}@example.com',
                        first_name=f'First_{i}',
                        last_name=f'Last_{i}',
                        password=make_password('password123')
                    )
                    users_to_create.append(user)

            if users_to_create:
                User.objects.bulk_create(users_to_create, batch_size=1000)
                self.stdout.write(f'Created {len(users_to_create)} users')

            all_users = list(User.objects.all())

            questions_to_create = []
            existing_questions_count = Question.objects.count()
            questions_needed = max(0, (ratio * 10) - existing_questions_count)

            for i in range(questions_needed):
                author = random.choice(all_users)
                question = Question(
                    title=f'How to build a moon park? #{i + existing_questions_count}',
                    text=f'Guys, i have trouble with a moon park. Can\'t find the black-jack... Question {i + existing_questions_count}. ' * 3,
                    author=author
                )
                questions_to_create.append(question)

            if questions_to_create:
                Question.objects.bulk_create(questions_to_create, batch_size=1000)
                self.stdout.write(f'Created {len(questions_to_create)} questions')

            all_questions = list(Question.objects.all())
            questions_without_tags = [q for q in all_questions if q.tags.count() == 0]

            for question in questions_without_tags:
                question_tags = random.sample(all_tags, min(3, len(all_tags)))
                question.tags.set(question_tags)

            self.stdout.write(f'Added tags to {len(questions_without_tags)} questions')
            answers_to_create = []
            existing_answers_count = Answer.objects.count()
            answers_needed = max(0, (ratio * 100) - existing_answers_count)

            for i in range(answers_needed):
                question = random.choice(all_questions)
                author = random.choice(all_users)
                answer = Answer(
                    question=question,
                    author=author,
                    text=f'First of all I would like to thank you for the invitation... Answer #{i + existing_answers_count}. ' * 2,
                    is_correct=(i % 5 == 0)
                )
                answers_to_create.append(answer)

            if answers_to_create:
                Answer.objects.bulk_create(answers_to_create, batch_size=1000)
                self.stdout.write(f'Created {len(answers_to_create)} answers')
            question_likes_to_create = []
            existing_question_likes = QuestionLike.objects.count()
            question_likes_needed = max(0, (ratio * 200) - existing_question_likes)

            existing_likes_set = set(
                QuestionLike.objects.values_list('user_id', 'question_id')
            )

            for i in range(question_likes_needed):
                user = random.choice(all_users)
                question = random.choice(all_questions)

                if (user.id, question.id) not in existing_likes_set:
                    question_like = QuestionLike(
                        user=user,
                        question=question,
                        is_like=random.choice([True, False])
                    )
                    question_likes_to_create.append(question_like)
                    existing_likes_set.add((user.id, question.id))

            if question_likes_to_create:
                QuestionLike.objects.bulk_create(question_likes_to_create, batch_size=1000)
                self.stdout.write(f'Created {len(question_likes_to_create)} question likes')

            all_answers = list(Answer.objects.all())
            answer_likes_to_create = []
            existing_answer_likes = AnswerLike.objects.count()
            answer_likes_needed = max(0, (ratio * 200) - existing_answer_likes)

            existing_answer_likes_set = set(
                AnswerLike.objects.values_list('user_id', 'answer_id')
            )

            for i in range(answer_likes_needed):
                user = random.choice(all_users)
                answer = random.choice(all_answers)

                if (user.id, answer.id) not in existing_answer_likes_set:
                    answer_like = AnswerLike(
                        user=user,
                        answer=answer,
                        is_like=random.choice([True, False])
                    )
                    answer_likes_to_create.append(answer_like)
                    existing_answer_likes_set.add((user.id, answer.id))

            if answer_likes_to_create:
                AnswerLike.objects.bulk_create(answer_likes_to_create, batch_size=1000)
                self.stdout.write(f'Created {len(answer_likes_to_create)} answer likes')

            self.stdout.write("Assigning avatars to users...")
            assign_avatars_to_users()

        self.stdout.write(self.style.SUCCESS('Database filled successfully!'))

        self.stdout.write(f"\n--- FINAL STATISTICS ---")
        self.stdout.write(f"Users: {User.objects.count()}")
        self.stdout.write(f"Tags: {Tag.objects.count()}")
        self.stdout.write(f"Questions: {Question.objects.count()}")
        self.stdout.write(f"Answers: {Answer.objects.count()}")
        self.stdout.write(f"Question likes: {QuestionLike.objects.count()}")
        self.stdout.write(f"Answer likes: {AnswerLike.objects.count()}")
