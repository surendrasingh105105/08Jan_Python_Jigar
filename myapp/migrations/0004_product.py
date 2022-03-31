# Generated by Django 4.0.2 on 2022-03-08 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user_usertype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_collection', models.CharField(choices=[('men', 'men'), ('women', 'women'), ('kids', 'kids')], max_length=100)),
                ('product_category', models.CharField(choices=[('shirt', 'shirt'), ('tshirt', 'tshirt'), ('jeans', 'jeans')], max_length=100)),
                ('product_size', models.CharField(choices=[('s', 's'), ('m', 'm'), ('l', 'l')], max_length=100)),
                ('product_color', models.CharField(choices=[('blue', 'blue'), ('black', 'black'), ('white', 'white'), ('pink', 'pink'), ('green', 'green'), ('red', 'red'), ('yellow', 'yellow')], max_length=100)),
                ('product_price', models.PositiveIntegerField()),
                ('product_desc', models.TextField()),
                ('product_image', models.ImageField(upload_to='product_image/')),
                ('product_seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.user')),
            ],
        ),
    ]
