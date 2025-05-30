# Generated by Django 5.2 on 2025-05-20 13:50

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drink_shop', '0003_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='drink_shop.member', verbose_name='會員'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nickname', models.CharField(default='匿名用戶', max_length=50, verbose_name='暱稱')),
                ('message', models.TextField(verbose_name='評論內容')),
                ('del_pass', models.CharField(max_length=50, verbose_name='刪除密碼')),
                ('pub_time', models.DateTimeField(auto_now_add=True, verbose_name='發布時間')),
                ('enabled', models.BooleanField(default=False, verbose_name='是否顯示')),
                ('drink', models.CharField(choices=[('bubble-tea', '珍珠奶茶'), ('mango-green-tea', '芒果綠茶'), ('milk-tea', '鮮奶茶'), ('fruit-tea', '繽紛水果茶'), ('matcha-latte', '抹茶拿鐵'), ('lemon-winter-melon', '檸檬冬瓜茶')], max_length=50, verbose_name='飲品')),
                ('rating', models.IntegerField(choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')], default=5, verbose_name='評分')),
                ('member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to='drink_shop.member', verbose_name='會員')),
            ],
            options={
                'verbose_name': '評論',
                'verbose_name_plural': '評論',
                'ordering': ['-pub_time'],
            },
        ),
    ]
