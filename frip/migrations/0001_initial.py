# Generated by Django 3.0.6 on 2020-05-17 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChildOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('price', models.IntegerField()),
                ('base_price', models.IntegerField()),
            ],
            options={
                'db_table': 'child_options',
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('include', models.TextField()),
                ('exclude', models.TextField()),
                ('schedule', models.TextField()),
                ('material', models.TextField()),
                ('notice', models.TextField()),
            ],
            options={
                'db_table': 'details',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
            ],
            options={
                'db_table': 'events',
            },
        ),
        migrations.CreateModel(
            name='FirstCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'first_categories',
            },
        ),
        migrations.CreateModel(
            name='FourthCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'fourth_categories',
            },
        ),
        migrations.CreateModel(
            name='Frip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('catch_phrase', models.CharField(max_length=300)),
                ('price', models.IntegerField()),
                ('faked_price', models.IntegerField()),
                ('duedate', models.IntegerField()),
                ('location', models.CharField(max_length=300)),
                ('venue', models.CharField(max_length=1000)),
                ('venue_lng', models.DecimalField(decimal_places=6, max_digits=10)),
                ('venue_lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('gathering_place', models.CharField(max_length=1000)),
                ('geopoint_lng', models.DecimalField(decimal_places=6, max_digits=10)),
                ('geopoint_lat', models.DecimalField(decimal_places=6, max_digits=10)),
                ('today', models.BooleanField()),
                ('ticket', models.BooleanField()),
                ('sale', models.BooleanField(default=0)),
                ('dateValidFrom', models.DateTimeField()),
                ('dateValidTo', models.DateTimeField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('detail', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Detail')),
            ],
            options={
                'db_table': 'frips',
            },
        ),
        migrations.CreateModel(
            name='FripCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.FirstCategory')),
                ('fourth_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.FourthCategory')),
                ('frip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip')),
            ],
            options={
                'db_table': 'frips_categories',
            },
        ),
        migrations.CreateModel(
            name='FripSubRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip')),
            ],
            options={
                'db_table': 'frips_sub_regions',
            },
        ),
        migrations.CreateModel(
            name='FripTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip')),
            ],
            options={
                'db_table': 'frips_themes',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image_url', models.URLField(max_length=2000)),
                ('description', models.TextField()),
                ('super_host', models.BooleanField()),
            ],
            options={
                'db_table': 'hosts',
            },
        ),
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('max_quantity', models.IntegerField()),
                ('frip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip')),
            ],
            options={
                'db_table': 'itineraries',
            },
        ),
        migrations.CreateModel(
            name='MainTab',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'main_tabs',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('base_price', models.IntegerField()),
                ('max_quantity', models.IntegerField()),
            ],
            options={
                'db_table': 'options',
            },
        ),
        migrations.CreateModel(
            name='OptionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'option_types',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'regions',
            },
        ),
        migrations.CreateModel(
            name='SecondCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('first_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.FirstCategory')),
                ('frip', models.ManyToManyField(through='frip.FripCategory', to='frip.Frip')),
            ],
            options={
                'db_table': 'second_categories',
            },
        ),
        migrations.CreateModel(
            name='ThirdCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('frip', models.ManyToManyField(through='frip.FripCategory', to='frip.Frip')),
                ('second_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.SecondCategory')),
            ],
            options={
                'db_table': 'third_categories',
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('frip', models.ManyToManyField(through='frip.FripTheme', to='frip.Frip')),
            ],
            options={
                'db_table': 'themes',
            },
        ),
        migrations.CreateModel(
            name='SubRegion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('frip', models.ManyToManyField(through='frip.FripSubRegion', to='frip.Frip')),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Region')),
            ],
            options={
                'db_table': 'sub_regions',
            },
        ),
        migrations.CreateModel(
            name='OptionChildOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.ChildOption')),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Option')),
            ],
            options={
                'db_table': 'options_child_options',
            },
        ),
        migrations.AddField(
            model_name='option',
            name='child_option',
            field=models.ManyToManyField(through='frip.OptionChildOption', to='frip.ChildOption'),
        ),
        migrations.AddField(
            model_name='option',
            name='frip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip'),
        ),
        migrations.AddField(
            model_name='option',
            name='option_type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.OptionType'),
        ),
        migrations.CreateModel(
            name='ItineraryOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itinerary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Itinerary')),
                ('option', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Option')),
            ],
            options={
                'db_table': 'itineraries_options',
            },
        ),
        migrations.AddField(
            model_name='itinerary',
            name='option',
            field=models.ManyToManyField(through='frip.ItineraryOption', to='frip.Option'),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(max_length=2000)),
                ('frip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip')),
            ],
            options={
                'db_table': 'images',
            },
        ),
        migrations.AddField(
            model_name='friptheme',
            name='theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Theme'),
        ),
        migrations.AddField(
            model_name='fripsubregion',
            name='sub_region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.SubRegion'),
        ),
        migrations.CreateModel(
            name='FripEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Event')),
                ('frip', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip')),
            ],
            options={
                'db_table': 'frips_evnets',
            },
        ),
        migrations.AddField(
            model_name='fripcategory',
            name='second_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.SecondCategory'),
        ),
        migrations.AddField(
            model_name='fripcategory',
            name='third_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.ThirdCategory'),
        ),
        migrations.AddField(
            model_name='frip',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Host'),
        ),
        migrations.AddField(
            model_name='fourthcategory',
            name='frip',
            field=models.ManyToManyField(through='frip.FripCategory', to='frip.Frip'),
        ),
        migrations.AddField(
            model_name='fourthcategory',
            name='third_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.ThirdCategory'),
        ),
        migrations.AddField(
            model_name='firstcategory',
            name='frip',
            field=models.ManyToManyField(through='frip.FripCategory', to='frip.Frip'),
        ),
        migrations.AddField(
            model_name='firstcategory',
            name='main_tab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.MainTab'),
        ),
        migrations.AddField(
            model_name='event',
            name='frip',
            field=models.ManyToManyField(through='frip.FripEvent', to='frip.Frip'),
        ),
        migrations.AddField(
            model_name='childoption',
            name='frip',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.Frip'),
        ),
        migrations.AddField(
            model_name='childoption',
            name='option_type',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='frip.OptionType'),
        ),
    ]
