# Generated by Django 2.0.3 on 2018-05-16 17:39

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def get_guide_permissions():
    """Create or get the permissions used by the guides.
    As Django creates permissions in the `post_migrate`
    signal, these need to be created manually for proper
    running in a test suite or for a migration from 0.
    Returns:
        (Permission, Permission, Permission):
            A tuple of three permissions:
            - the `add_guide` permission
            - the `change_guide` permission
            - the `delete_guide` permission
    """

    guide_content_type, _ = ContentType.objects.get_or_create(app_label='guides', model='guide')
    add_guide, _ = Permission.objects.get_or_create(codename='add_guide', content_type=guide_content_type)
    change_guide, _ = Permission.objects.get_or_create(codename='change_guide', content_type=guide_content_type)
    delete_guide, _ = Permission.objects.get_or_create(codename='delete_guide', content_type=guide_content_type)
    return add_guide, change_guide, delete_guide


def add_member_permissions(apps, schema_editor):
    """Add the `add_guide` permission to the member group."""

    add_guide, _, _ = get_guide_permissions()
    member_group = Group.objects.get(name='member')
    member_group.permissions.add(add_guide)


def add_staff_permissions(apps, schema_editor):
    """Add the following permissions to the staff group:
    - `add_guide`
    - `change_guide`
    - `delete_guide`
    These apply on all guides, even those that staff does not own.
    """

    add_guide, change_guide, delete_guide = get_guide_permissions()
    staff_group = Group.objects.get(name='staff')
    staff_group.permissions.add(add_guide, change_guide, delete_guide)



class Migration(migrations.Migration):

    dependencies = [
        ('guides', '0005_remove_guide_editors'),
        ('home', '0001_create_permission_groups')
    ]

    operations = [
        migrations.RunPython(add_member_permissions),
        migrations.RunPython(add_staff_permissions)
    ]
