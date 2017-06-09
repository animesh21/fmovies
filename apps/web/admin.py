"""
This is admin panel configuration file for web module.
@author info@asquarexpert.com
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Permission
from django.contrib.admin.templatetags.admin_modify import *
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row
from apps.web.models import *
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.exceptions import PermissionDenied


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def submit_row(context):
    ctx = original_submit_row(context)
    ctx.update({
        'show_save_and_add_another': context.get('show_save_and_add_another', ctx['show_save_and_add_another']),
        'show_save_and_continue': context.get('show_save_and_continue', ctx['show_save_and_continue'])
        })
    return ctx


class MyUserAdmin(admin.ModelAdmin):
    # actions = None
    #def has_delete_permission(self, request, obj=None):
    #    return True
    exclude = ('is_staff',)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['really_hide_save_and_add_another_damnit'] = True
        return super(MyUserAdmin, self).change_view(request, object_id,
                                                     form_url, extra_context=extra_context)

    def get_fieldsets(self, request, obj=None):

        if not obj:
            return ['first_name']

        return [
                (_('Personal info'), {'fields':
                                          ('first_name',
                                           'last_name',
                                           'email',
                                           'score',
                                           'rank'
                                           )
                                      }
                 ),
        ]


class UpcomingMovie(admin.ModelAdmin):
    

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['really_hide_save_and_add_another_damnit'] = True
        return super(UpcomingMovie, self).change_view(request, object_id,
                                                    form_url, extra_context=extra_context)



class MapMovie(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('uobj', 'mobj')
        return self.readonly_fields

admin.site.register(User,MyUserAdmin)
admin.site.register(map_userMovie,MapMovie)
