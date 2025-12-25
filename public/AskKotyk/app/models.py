from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Q

class DefaultModel(models.Model):
    class Meta:
        abstract = True

    is_active = models.BooleanField(default=True, verbose_name="Активен?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания", editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления", editable=False, null=True)

class User(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='app_user_set',
        related_query_name='app_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='app_user_set',
        related_query_name='app_user',
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    def get_display_name(self):
        """Получить отображаемое имя пользователя"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username

class Tag(models.Model):
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")

    def __str__(self):
        return self.name

class QuestionManager(models.Manager):
    def new_questions(self):
        return self.filter(is_active=True).order_by('-created_at')

    def hot_questions(self):
        return self.filter(is_active=True).annotate(
            answers_count=Count('answers')
        ).order_by('-answers_count', '-created_at')
    def with_tag(self, tag_name):
        """
        Возвращает вопросы с указанным тегом
        """
        return self.filter(
            is_active=True,
            tags__name=tag_name
        ).order_by('-created_at')

class Question(DefaultModel):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    objects = QuestionManager()

    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('app:question', kwargs={'question_id': self.id})

    def votes_count(self):
        likes = self.questionlike_set.filter(is_like=True).count()
        dislikes = self.questionlike_set.filter(is_like=False).count()
        return likes - dislikes

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super(Question, self).save(*args, **kwargs)
    def votes_count(self):
        likes = self.questionlike_set.filter(is_like=True).count()
        dislikes = self.questionlike_set.filter(is_like=False).count()
        return likes - dislikes

    def user_vote(self, user):
        """Получить голос пользователя для этого вопроса"""
        if not user.is_authenticated:
            return None
        try:
            vote = QuestionLike.objects.get(user=user, question=self)
            return 'like' if vote.is_like else 'dislike'
        except QuestionLike.DoesNotExist:
            return None


class Answer(DefaultModel):
    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Ответ на вопрос: {self.question.title}"

    def votes_count(self):
        likes = self.answerlike_set.filter(is_like=True).count()
        dislikes = self.answerlike_set.filter(is_like=False).count()
        return likes - dislikes
    def votes_count(self):
        likes = self.answerlike_set.filter(is_like=True).count()
        dislikes = self.answerlike_set.filter(is_like=False).count()
        return likes - dislikes

    def user_vote(self, user):
        """Получить голос пользователя для этого ответа"""
        if not user.is_authenticated:
            return None
        try:
            vote = AnswerLike.objects.get(user=user, answer=self)
            return 'like' if vote.is_like else 'dislike'
        except AnswerLike.DoesNotExist:
            return None

class QuestionLike(models.Model):
    class Meta:
        unique_together = ('user', 'question')
        verbose_name = 'Лайк вопроса'
        verbose_name_plural = 'Лайки вопросов'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.is_like else 'Dislike'} - {self.question.title}"

class AnswerLike(models.Model):
    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = 'Лайк ответа'
        verbose_name_plural = 'Лайки ответов'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {'Like' if self.is_like else 'Dislike'} - {self.answer.question.title}"
