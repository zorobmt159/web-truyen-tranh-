from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(name='Tag',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('name',models.CharField(max_length=50,unique=True)),('slug',models.SlugField(blank=True,null=True,unique=True)),],),
        migrations.CreateModel(name='Comic',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('title',models.CharField(max_length=200)),('description',models.TextField(blank=True)),('cover_image',models.ImageField(blank=True,null=True,upload_to='covers/')),('views',models.IntegerField(default=0)),('likes',models.IntegerField(default=0)),('created_at',models.DateTimeField(auto_now_add=True)),('updated_at',models.DateTimeField(auto_now=True)),('tags',models.ManyToManyField(blank=True,related_name='comics',to='blog.tag')),('followers',models.ManyToManyField(blank=True,related_name='followed_comics',to=settings.AUTH_USER_MODEL)),],),
        migrations.CreateModel(name='Chapter',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('chapter_number',models.FloatField()),('title',models.CharField(blank=True,max_length=200)),('created_at',models.DateTimeField(auto_now_add=True)),('comic',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,related_name='chapters',to='blog.comic')),],options={'ordering':['chapter_number']},),
        migrations.CreateModel(name='UserProfile',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('avatar',models.ImageField(blank=True,null=True,upload_to='avatars/')),('plan',models.CharField(choices=[('free','Free'),('pro','Pro'),('premium','Premium')],default='free',max_length=20)),('plan_expires_at',models.DateTimeField(blank=True,null=True)),('created_at',models.DateTimeField(auto_now_add=True)),('user',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name='profile',to=settings.AUTH_USER_MODEL)),],),
        migrations.CreateModel(name='Subscription',fields=[('id',models.BigAutoField(auto_created=True,primary_key=True,serialize=False,verbose_name='ID')),('plan',models.CharField(choices=[('free','Free'),('pro','Pro'),('premium','Premium')],default='free',max_length=20)),('started_at',models.DateTimeField(auto_now_add=True)),('expires_at',models.DateTimeField(blank=True,null=True)),('is_active',models.BooleanField(default=True)),('user',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE,related_name='subscription',to=settings.AUTH_USER_MODEL)),],),
    ]
