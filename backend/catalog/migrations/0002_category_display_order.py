from django.db import migrations, models

CATEGORY_ORDER = [
    'all-products',
    'best-sellers',
    'sugar-free',
    'mukhwas',
    'churan',
    'supari',
    'pan',
    'tiny-miny',
    'gifts-combos',
]


def set_display_order(apps, schema_editor):
    Category = apps.get_model('catalog', 'Category')
    for index, route in enumerate(CATEGORY_ORDER):
        Category.objects.filter(route=route).update(display_order=index)


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='display_order',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(set_display_order, migrations.RunPython.noop),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['display_order', 'name'], 'verbose_name_plural': 'Categories'},
        ),
    ]
