# Generated by Django 4.1.3 on 2022-11-02 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='API',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('key', models.CharField(max_length=200)),
                ('website', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='security',
            name='api',
        ),
        migrations.AddField(
            model_name='security',
            name='api_in_use',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='market.api'),
        ),
    ]
