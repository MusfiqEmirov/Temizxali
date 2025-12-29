# Generated manually to fix database schema mismatch

from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    BloqTranslation = apps.get_model('services', 'BloqTranslation')
    
    for translation in BloqTranslation.objects.all():
        if not translation.slug and translation.name:
            # Generate slug from name
            slug = slugify(translation.name)
            
            # Make it unique
            unique_slug = slug
            num = 1
            while BloqTranslation.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{slug}-{num}"
                num += 1
            
            translation.slug = unique_slug
            translation.save()


def reverse_populate_slugs(apps, schema_editor):
    # Nothing to reverse
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        # Add view_count if it doesn't exist
        migrations.RunSQL(
            sql="ALTER TABLE services_bloq ADD COLUMN IF NOT EXISTS view_count INTEGER DEFAULT 0;",
            reverse_sql="ALTER TABLE services_bloq DROP COLUMN IF EXISTS view_count;"
        ),
        # Add slug if it doesn't exist (as nullable first)
        migrations.RunSQL(
            sql="ALTER TABLE services_bloqtranslation ADD COLUMN IF NOT EXISTS slug VARCHAR(80);",
            reverse_sql="ALTER TABLE services_bloqtranslation DROP COLUMN IF EXISTS slug;"
        ),
        # Populate slugs for existing records
        migrations.RunPython(populate_slugs, reverse_populate_slugs),
        # Add unique constraint to slug if it doesn't exist
        migrations.RunSQL(
            sql="""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'services_bloqtranslation_slug_key'
                    ) THEN
                        ALTER TABLE services_bloqtranslation 
                        ADD CONSTRAINT services_bloqtranslation_slug_key UNIQUE (slug);
                    END IF;
                END $$;
            """,
            reverse_sql="ALTER TABLE services_bloqtranslation DROP CONSTRAINT IF EXISTS services_bloqtranslation_slug_key;"
        ),
    ]

