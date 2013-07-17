# -*- coding: utf-8 -*-
from django.contrib import admin
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.contrib.admin.util import unquote
from django.utils.encoding import force_unicode
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.db import models, transaction, router
from django.template.response import  TemplateResponse
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.utils.html import escape

csrf_protect_m = method_decorator(csrf_protect)


class FastDelete(admin.ModelAdmin):

    def delete_view(self, request, object_id, extra_context=None):
        "The 'delete' admin view for this model."
        opts = self.model._meta
        app_label = opts.app_label

        obj = self.get_object(request, unquote(object_id))

        if not self.has_delete_permission(request, obj):
            raise PermissionDenied

        if obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name': force_unicode(opts.verbose_name), 'key': escape(object_id)})

        using = router.db_for_write(self.model)

        # Populate deleted_objects, a data structure of all related objects that
        # will also be deleted.

        (deleted_objects, perms_needed, protected) = (['Все связанные модели!'], None, None)

        if request.POST: # The user has already confirmed the deletion.
            if perms_needed:
                raise PermissionDenied
            obj_display = force_unicode(obj)
            self.log_deletion(request, obj, obj_display)
            self.delete_model(request, obj)

            self.message_user(request, _('The %(name)s "%(obj)s" was deleted successfully.') % {'name': force_unicode(opts.verbose_name), 'obj': force_unicode(obj_display)})

            if not self.has_change_permission(request, None):
                return HttpResponseRedirect(reverse('admin:index',
                                                    current_app=self.admin_site.name))
            return HttpResponseRedirect(reverse('admin:%s_%s_changelist' %
                                        (opts.app_label, opts.module_name),
                                        current_app=self.admin_site.name))

        object_name = force_unicode(opts.verbose_name)

        if perms_needed or protected:
            title = _("Cannot delete %(name)s") % {"name": object_name}
        else:
            title = _("Are you sure?")

        context = {
            "title": title,
            "object_name": object_name,
            "object": obj,
            "deleted_objects": deleted_objects,
            "perms_lacking": perms_needed,
            "protected": protected,
            "opts": opts,
            "app_label": app_label,
        }
        context.update(extra_context or {})

        return TemplateResponse(request, self.delete_confirmation_template or [
            "admin/%s/%s/delete_confirmation.html" % (app_label, opts.object_name.lower()),
            "admin/%s/delete_confirmation.html" % app_label,
            "admin/delete_confirmation.html"
        ], context, current_app=self.admin_site.name)