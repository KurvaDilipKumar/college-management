from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0026_alter_faculty_options_alter_marks_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faculty',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
