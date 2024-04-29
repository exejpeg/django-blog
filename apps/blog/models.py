from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey

STATUS_OPTIONS = (
    ('published', 'Опубликовано'),
    ('draft', 'Черновик')
)

class Post(models.Model): #Модель постов блога
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(verbose_name="URL", max_length=255, blank=True)
    description = models.TextField(verbose_name="Краткое описание", max_length=500)
    text = models.TextField(verbose_name="Полный текст")
    thumbnail = models.ImageField(
        verbose_name="Изображение",
        default="default.jpg",
        upload_to="images/thumbnails/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'gif'])]
    )
    status = models.CharField(choices=STATUS_OPTIONS, default="published", max_length=10, verbose_name="Статус")
    create = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления")
    update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    author = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, verbose_name="Автор", related_name="author_posts", default=1)
    updater = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, verbose_name="Обновил", related_name="updater_posts", blank=True)
    fixed = models.BooleanField(default=False, verbose_name="Прикреплено")
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name="posts", verbose_name="Категория")

    class Meta:
        db_table = "blog_post"
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['fixed', '-create', '-status'])]
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

class Category(MPTTModel): #Модель категории с вложенностью
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="URL", blank=True)
    description = models.TextField(verbose_name="Описание", max_length=300)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name="children", verbose_name="Родительская категория", null=True, blank=True, db_index=True)

    class MPTTMeta:
        order_insertion_by = ('title',)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        db_table = "app_categories"

    def __str__(self):
        return self.title