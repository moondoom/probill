# -*- coding: utf-8 -*-

import operator
from django.db import models
from django.core.exceptions import FieldError
from django.core.paginator import Paginator, InvalidPage
from django.utils.encoding import smart_str
from dojango.util import json
from django.core.serializers.json import DjangoJSONEncoder
from django.conf.urls import patterns, url
from django.forms.models import modelform_factory
from django.shortcuts import HttpResponse, render_to_response, RequestContext
from django.core.urlresolvers import reverse
from django.db.models import NOT_PROVIDED , ForeignKey


import copy,re

def json_encode(data):
    encoder = DjangoJSONEncoder(sort_keys=True)
    return encoder.encode(data)




def profile_filter(method):
    def wrapper(self,request,*args,**kwargs):
        self.request = request
        return method(self,request,*args,**kwargs)
    return wrapper

class JqGrid(object):
    model = None
    fields = []
    custom_fields = {}
    joined_fields = {}
    actions = []
    filter = []
    allow_empty = True
    extra_config = {}
    pager_id = '#pager'
    url = None
    caption = None
    colmodel_overrides = {}
    autocomplete_fields = {}
    fields_size = 40



    INTEGER_FIELDS = ['IntegerField',
                      'SmallIntegerField',
                      'PositiveIntegerField',
                      'PositiveSmallIntegerField',
                      'BigIntegerField']

    FLOAT_FIELDS = ['FloatField',
                    'DecimalField']

    TOTAL_FIELDS = INTEGER_FIELDS+FLOAT_FIELDS

    CHAR_FIELDS = ['CharField',
                   'GenericIPAddressField',
                   'EmailField',
                   'IPAddressField',
                   'URLField']

    TEXT_FIELDS = TOTAL_FIELDS + CHAR_FIELDS

    TEXT_AREA_FIELDS = ['TextField',
                        'XMLField']

    RELATED_FIELDS = ['ForeignKey',
                      'OneToOneField',
                      'TreeForeignKey']

    MANY_FIELDS = ['ManyToManyField',
                   'OneToManyField']

    DATE_FIELDS = ['DateTimeField',
                   'DateField',]

    TIME_FIELDS = ['TimeField']

    SELECT_FIELDS = MANY_FIELDS + RELATED_FIELDS + TIME_FIELDS

    JQGRID_DATEPICKER = '''
    newfunc = function (elem) { $(elem).datepicker({ showButtonPanel: false, dateFormat:'yy-mm-dd'}) }
    '''

    JQGRID_MANY_FUNCTION = '''
    newfunc = function (elem) {
        setTimeout($(elem).multiselect({
            selectedText: "# из # выбрано",
            noneSelectedText: "Выберете вакансии",
            uncheckAllText: "Убрать все",
            checkAllText: "Выбрать все",
            }),100)}'''

    JQGRID_AUTOCOM = '''
       newfunc =  function (elem) {{
         setTimeout(function() {{
              $(elem).autocomplete({{
              source: '{0}',
              search: '',
              minLength: 0,
              multiple: false,
              formatItem: function (item, index, total, query) {{
                  return item.label;
              }},
              change: function (event, ui) {{
                   if (ui.item.value == 'None') {{
                        return false;
                   }}
                    $('#{1}_name').val(ui.item.label);
                    $('#{1}').val(ui.item.value);
                    return false;
              }},
              focus: function (event, ui) {{
                   if (ui.item.value == 'None') {{
                        return false;
                   }}
                    $('#{1}_name').val(ui.item.label);
                    $('#{1}').val(ui.item.value);

                    return false;
              }},
              select: function (event, ui) {{
                   if (ui.item.value == 'None') {{
                        return false;
                   }}
                    $('#{1}_name').val(ui.item.label);
                    $('#{1}').val(ui.item.value);
                    return false;
              }},
          }})
          }},100);
      }};
    '''



    def __init__(self):
        # TODO: Add auto perm discovery from model
        self.all_fields = self.get_field_dict()
        self._fields = self.all_fields
        self.m2m_fields = self.get_m2m_field_dict()
        self.queryset = self.get_queryset()


    def get_queryset(self):
        queryset = self.model.objects.all()
        if len(self.filter) == 1:
            queryset = queryset.filter(**{smart_str(self.filter[0][0]):smart_str(self.filter[0][1])})
        elif len(self.filter) > 1:
            q_filter = [models.Q(**{smart_str(f[0]):smart_str(f[1])}) for f in self.filter]
            queryset = queryset.filter(reduce(operator.iand, q_filter))
        return queryset


    def get_items(self, request):
        items = self.queryset
        items = self.filter_items(request, items)
        items = self.sort_items(request, items)
        return self.paginate_items(request, items)

    def get_filters(self, request):
        _search = request.GET.get('_search')
        filters = None

        if _search == 'true':
            _filters = request.GET.get('filters')
            try:
                filters = _filters and json.loads(_filters)
            except ValueError:
                return None
            if filters is None:
                field = request.GET.get('searchField')
                op = request.GET.get('searchOper')
                data = request.GET.get('searchString')

                if all([field, op, data]):
                    filters = {
                        'groupOp': 'AND',
                        'rules': [{ 'op': op, 'field': field, 'data': data }]
                    }
        return filters

    def filter_items(self, request, items):
        # TODO: Add option to use case insensitive filters
        # TODO: Add more support for RelatedFields (searching and displaying)
        # FIXME: Validate data types are correct for field being searched.
        filter_map = {
            # jqgrid op: (django_lookup, use_exclude)
            'ne': ('%(field)s__exact', True),
            'bn': ('%(field)s__startswith', True),
            'en': ('%(field)s__endswith',  True),
            'nc': ('%(field)s__contains', True),
            'ni': ('%(field)s__in', True),
            'in': ('%(field)s__in', False),
            'eq': ('%(field)s__exact', False),
            'bw': ('%(field)s__startswith', False),
            'gt': ('%(field)s__gt', False),
            'ge': ('%(field)s__gte', False),
            'lt': ('%(field)s__lt', False),
            'le': ('%(field)s__lte', False),
            'ew': ('%(field)s__endswith', False),
            'cn': ('%(field)s__contains', False)
        }
        _filters = self.get_filters(request)
        if _filters is None:
            return items

        q_filters = []
        for rule in _filters['rules']:
            op, field, data = rule['op'], rule['field'], rule['data']
            # FIXME: Restrict what lookups performed against RelatedFields
            field_class = self._fields[field]
            if isinstance(field_class, models.related.RelatedField):
                op = 'eq'
            filter_fmt, exclude = filter_map[op]
            filter_str = smart_str(filter_fmt % {'field': field})
            if filter_fmt.endswith('__in'):
                filter_kwargs = {filter_str: data.split(',')}
            else:
                filter_kwargs = {filter_str: smart_str(data)}

            if exclude:
                q_filters.append(~models.Q(**filter_kwargs))
            else:
                q_filters.append(models.Q(**filter_kwargs))

        if _filters['groupOp'].upper() == 'OR':
            filters = reduce(operator.ior, q_filters)
        else:
            filters = reduce(operator.iand, q_filters)
        return items.filter(filters)

    def sort_items(self, request, items):
        sidx = request.GET.get('sidx')
        if sidx is not None:
            sord = request.GET.get('sord')
            order_by = '%s%s' % (sord == 'desc' and '-' or '', sidx)
            try:
                items = items.order_by(order_by)
            except FieldError:
                pass
        return items

    def get_paginate_by(self, request):
        rows = request.GET.get('rows', self.get_config(False)['rowNum'])
        try:
            paginate_by = int(rows)
        except ValueError:
            paginate_by = 10
        return paginate_by

    def paginate_items(self, request, items):
        paginate_by = self.get_paginate_by(request)
        paginator = Paginator(items, paginate_by,
                              allow_empty_first_page=self.allow_empty)
        page = request.GET.get('page', 1)
        try:
            page_number = int(page)
            page = paginator.page(page_number)
        except (ValueError, InvalidPage):
            page = paginator.page(1)
        return paginator, page


    def get_field_value(self,obj,field):
        obj_field = getattr(obj,field)
        value = {}
        if field in self.m2m_fields:
            value[field] = ','.join([unicode(f.id) for f in obj_field.all()])
        elif self._fields[field].__class__.__name__ in self.RELATED_FIELDS and obj_field:
            value[field] = unicode(obj_field.id)
            if field in self.autocomplete_fields:
                value[field + '_name'] = unicode(obj_field)
        else:
            value[field] = unicode(obj_field)
        if value[field] == 'None':
            value[field] = ''
        return value

    def obj_to_row(self,obj):
        row = {}
        for field in self._fields:
            row.update(self.get_field_value(obj,field))
        return row

    def get_json(self, request):
        paginator, page = self.get_items(request)
        rows = []
        for obj in page.object_list:
            rows.append(self.obj_to_row(obj))
        data={
            'page': int(page.number),
            'total': int(paginator.num_pages),
            'rows': rows,
            'records': int(paginator.count),
        }
        return json_encode(data)


    def get_default_config(self):
        config = {
            'datatype': 'json',
            'autowidth': True,
            'forcefit': True,
            'shrinkToFit': True,
            'jsonReader': { 'repeatitems': False  },
            'rowNum': 25,
            'rowList': [10, 25, 50, 75, 100],
            'sortname': 'id',
            'viewrecords': True,
            'sortorder': "asc",
            'pager': self.pager_id,
            'altRows': True,
            'gridview': True,
            'height': 'auto',
            #'multikey': 'ctrlKey',
            #'multiboxonly': True,
            #'multiselect': True,
            #'toolbar': [False, 'bottom'],
            #'userData': None,
            #'rownumbers': False,
        }
        return config

    def reverse(self,function,**kwargs):
        return None

    def get_url(self):
        return str(self.url)

    def get_caption(self):
        if self.caption is None:
            opts = self.model._meta
            self.caption = opts.verbose_name_plural.capitalize()
        return self.caption

    def get_config(self, as_json=True):
        config = self.get_default_config()
        config.update(self.extra_config)
        config.update({
            'url': self.get_url(),
            'caption': self.get_caption(),
            'colModel': self.get_colmodels(),
        })
        if as_json:
            config = json_encode(config)
        return config


    def get_field_dict(self):
        fields = dict([[f.name,f] for f in self.model._meta.local_fields + self.model._meta.local_many_to_many])
        return fields

    def get_m2m_field_dict(self):
        fields = dict([[f.name,f] for f in self.model._meta.local_many_to_many])
        return fields

    def get_field_list(self):
        fields = [f.name for f in self.model._meta.local_fields + self.model._meta.local_many_to_many if f.name in self._fields]
        if self.fields:
            fields = [f for f in self.fields if f in fields]
        return fields

    def get_colmodels(self):
        colmodels = []
        if self.actions:
            colmodels += self.get_action()
        for field_name in self.get_field_list():
            colmodel = self.field_to_colmodel(self._fields[field_name])
            if colmodel:
                colmodels += colmodel
        return colmodels

    def get_action(self):
        colmodel = {
            'name': 'act',
            'index': 'act',
            'label': 'Действие',
        }
        return [colmodel]

    def get_field_choices(self,field,field_type):
        select = {}
        for id,val in field.get_choices():
            if not (field_type in self.MANY_FIELDS and not id):
                select[unicode(id)] = val
        return select

    def field_to_colmodel(self, field):
        """

        """
        # TODO: Сделать более правильные разбор полей возможно смигрировать таки на формы
        colmodel = [{
            'name': field.name,
            'index': field.name,
            'label': str(field.verbose_name),
            'editable': not field.primary_key and field.editable,
            'key': field.primary_key,
            'hidden': field.primary_key,
            'editoptions': {},
            'editrules': {
                'edithidden' : not field.editable,
                'required': not field.blank,
            }
        }]
        field_type = field.__class__.__name__
        if field.default <> NOT_PROVIDED:
            if hasattr(field.default,'__call__'):
                colmodel[0]['editoptions']['defaultValue'] = field.default()
            else:
                colmodel[0]['editoptions']['defaultValue'] = field.default
        if field_type in self.TEXT_FIELDS:
            if field.choices:
                colmodel[0]['edittype'] = 'select'
                colmodel[0]['formatter'] = 'select'
                colmodel[0]['editoptions']['value'] = self.get_field_choices(field,field_type)
            else:
                colmodel[0]['edittype'] = 'text'
                colmodel[0]['editoptions']['size'] = self.fields_size
            if field.max_length and not field.choices:
                colmodel[0]['editoptions']['max_length'] = field.max_length

        elif field_type == 'BooleanField':
            colmodel[0]['edittype'] = 'checkbox'
            colmodel[0]['formatter'] = 'checkbox'
            colmodel[0]['editoptions']['value'] = 'true:false'
            if 'defaultValue' in colmodel[0]['editoptions']:
                colmodel[0]['editoptions']['defaultValue'] = str(field.default).lower()
        elif field_type in self.DATE_FIELDS:
            colmodel[0]['edittype'] = 'text'
            colmodel[0]['editoptions']['dataInit'] =  self.JQGRID_DATEPICKER
        elif field_type in self.TEXT_AREA_FIELDS:
            colmodel[0]['edittype'] = 'textarea'
            colmodel[0]['editoptions']['cols'] = int(self.fields_size*0.8)
            colmodel[0]['editoptions']['rows'] = self.fields_size/5
        elif field_type in self.SELECT_FIELDS:
            if field_type in self.MANY_FIELDS:
                colmodel[0]['edittype'] = 'select'
                colmodel[0]['formatter'] = 'select'
                colmodel[0]['editoptions']['multiple'] = True

                colmodel[0]['editoptions']['value'] = self.get_field_choices(field,field_type)
            elif field.name in self.autocomplete_fields:
                colmodel[0]['formatter'] = 'text'
                colmodel[0]['edittype'] = 'text'
                colmodel.append(copy.copy(colmodel[0]))
                colmodel[0]['hidden'] = True
                del colmodel[0]['editoptions']
                colmodel[1]['name'] = field.name + '_name'
                colmodel[1]['index'] = field.name + '_name'
                colmodel[1]['editoptions']['dataInit'] = self.JQGRID_AUTOCOM.format(
                    self.reverse('autocomplete',args=(field.name,)), field.name
                )
                colmodel[1]['editoptions']['size'] = self.fields_size
            else:
                colmodel[0]['formatter'] = 'select'
                colmodel[0]['edittype'] = 'select'
                colmodel[0]['editoptions']['value'] = self.get_field_choices(field,field_type)
        if field.name in self.custom_fields:
            colmodel[0].update(self.custom_fields[field.name])
        return colmodel


class JqGridView(JqGrid):
    app_name = None
    model_url = None
    view_perm = None
    edit_perm = None
    add_perm = None
    delete_perm = None
    aed = {
        'add': True,
        'edit': True,
        'delete': True,
    }
    index_template = 'moon/jquery_grid_menu.html'
    deny_template = 'moon/jquery_grid_deny.html'

    def __init__(self):
        super(JqGridView,self).__init__()
        meta = self.model._meta
        if not self.edit_perm:
            self.edit_perm = '{}.{}'.format(self.app_name,meta.get_change_permission())
        if not self.add_perm:
            self.add_perm = '{}.{}'.format(self.app_name,meta.get_add_permission())
        if not self.delete_perm:
            self.delete_perm = '{}.{}'.format(self.app_name,meta.get_delete_permission())
        if not self.view_perm:
            self.view_perm='{}.view_{}'.format(self.app_name,self.model_name)
            if self.view_perm not in meta.permissions:
                self.view_perm = self.add_perm

    def reverse(self,function,**kwargs):
        if self.app_name:
            url_format = '{}:{}_{{}}'.format(self.app_name,self.model_name)
        else:
            url_format = '{}_{{}}'.format(self.model_name)
        return reverse(url_format.format(function),**kwargs)

    def get_urls(self):
        urlpatterns = patterns('',
            url(r'^index$',self.view_index,name='%s_index' % self.model_name),
            url(r'^edit$',self.view_edit,name='%s_edit' % self.model_name),
            url(r'^handler$',self.view_handler,name='%s_handler' % self.model_name),
            url(r'^config$',self.view_config,name='%s_config' % self.model_name),
            url(r'^autocomplete/(.*)$',self.view_autocomplete,name='%s_autocomplete' % self.model_name),
            url(r'^action$',self.view_action,name='%s_action' % self.model_name),
            url(r'^form$',self.view_form,name='%s_form' % self.model_name),
        )
        return urlpatterns

    def get_url(self):
        return self.reverse('handler')


    @property
    def urls(self):
        return self.get_urls()

    @property
    def model_name(self):
        if self.model_url:
            return self.model_url
        return self.model.__name__.lower()

    def check_perm(self,request,perm):
        if request.user.is_superuser:
            return True
        elif  isinstance(perm,(str, unicode)):
            return request.user.has_perm(perm)
        else:
            return any(map(request.user.has_perm,perm))

    @profile_filter
    def view_index(self,request):
        context = RequestContext(request)
        if self.check_perm(request,self.view_perm):
            context['config_url'] = self.reverse('config')
            context['edit_url'] = self.reverse('edit')
            context['action_url'] = self.reverse('action')
            context['form_url'] = self.reverse('form')
            context['can_add'] = request.user.has_perm(self.add_perm)
            context['can_edit'] = request.user.has_perm(self.edit_perm)
            context['can_delete'] = request.user.has_perm(self.delete_perm)
            context['actions'] = self.actions
            context['aed'] = self.aed
            context['fields'] = self._fields
            return render_to_response(self.index_template,context)
        else:
            return render_to_response(self.deny_template,context)

    def get_field_choices(self,field,field_type):
        if field_type in self.RELATED_FIELDS:
            obj = field.rel.to
            queryset = obj.objects.all()
            return dict([[unicode(obj.id),unicode(obj)] for obj in queryset])
        else:
            return super(JqGridView,self).get_field_choices(field,field_type)

    @profile_filter
    def view_config(self,request):
        if self.check_perm(request,self.view_perm):
            self.request = request
            return HttpResponse(self.get_config(request), mimetype="application/json")
        else:
            return HttpResponse({}, mimetype="application/json")

    @profile_filter
    def view_handler(self,request):
        if self.check_perm(request,self.view_perm):
            return HttpResponse(self.get_json(request), mimetype="application/json")
        else:
            return HttpResponse({}, mimetype="application/json")


    def get_form(self,keys,instance=None):
        ModelForm = modelform_factory(self.model)
        form = ModelForm(keys,instance=instance)
        return form

    @profile_filter
    def view_edit(self,request):
        error = {}
        if 'oper' in request.POST:
            action = request.POST['oper']
            if (action == 'add' and self.check_perm(request,self.add_perm)) \
               or (action == 'edit' and self.check_perm(request,self.edit_perm)):
                keys = request.POST.copy()
                for key in request.POST:
                    if request.POST[key]:
                        if key in self.m2m_fields:
                            val = request.POST[key]
                            keys.setlist(key,val.split(','))
                    else:
                        del keys[key]
                instance = None
                if action == 'edit':
                    instance = self.model.objects.get(id=int(keys['id']))
                    if instance not in self.queryset:
                        error['server_error'] = u'\n У вас нет прав для редактирования этого объекта'
                form = self.get_form(keys,instance=instance)
                if form.is_valid() and not error:
                    form.save()
                else:
                    if 'server_error' not in error:
                        error['server_error'] = ''
                    error['server_error'] = u'Ошибка проверки формы!' + error['server_error']
                    for f in form.errors:
                        print f, form.errors[f]
                        error['server_error'].extend(u'{1} {0}'.format(self._fields[f].verbose_name,form.errors[f]))

            elif action == 'del' and self.check_perm(request,self.delete_perm):
                self.model.objects.get(id=int(request.POST['id'])).delete()
            else:
                error = {'server_error': 'Неверный запрос или недостаточно прав!'}
        else:
            error = {'server_error':'Не верный запрос!'}
        return HttpResponse(json_encode(error), mimetype="application/json")

    def check_action(self,request):
        action_str = request.GET['action']
        if action_str not in self.actions:
            return False, 'Action not found'
        elif not request.user.has_perm(self.actions[action_str]['perm']):
            return False, 'User don`t have {} perm'.format(self.actions[action_str]['perm'])
        else:
            return True, action_str

    @profile_filter
    def view_action(self,request):
        response = {'error':'','success':False}
        if 'id' in request.GET and 'action' in request.GET:
            ok, message = self.check_action(request)
            if ok:
                action_method = 'action_{}'.format(message)
                try:
                    id = int(request.GET['id'])
                    obj = self.model.objects.get(id=id)
                    if hasattr(obj,action_method) and obj in self.queryset:
                        kwargs = {'request':request}
                        if 'form' in self.actions[message]:
                            form = self.actions[message]['form']
                            for key in form['args']:
                                kwargs[key] = request.GET[key]
                        response['success'], response['error'] = getattr(obj,action_method)(**kwargs)
                    else:
                        response['error'] = 'Object don`t have {} method'.format(action_method)
                except Exception as error:
                    response['error'] = 'Other error: {}'.format(str(error))
            else:
                response['error'] = message
        return HttpResponse(json_encode(response),mimetype='application/json')

    @profile_filter
    def view_form(self,request):
        message = 'Not found'
        if 'action' in request.GET:
            ok, message = self.check_action(request)
            if ok:
                if 'form' in self.actions[message]:
                    instance = self.model.objects.get(id=request.GET['id'])
                    if instance in self.queryset:
                        context = RequestContext(request)
                        context['obj'] = instance
                        context['model'] = self.model
                        context['fields'] = self._fields
                        return render_to_response(self.actions[message]['form']['template'],context)
        return HttpResponse(message,mimetype='text/plain')

    def view_autocomplete(self,request,field_name):
        if not (self.check_perm(request,self.edit_perm) or self.check_perm(request,self.add_perm)):
            return  HttpResponse('{}', mimetype="application/json")
        json = '{}'
        if field_name in self._fields and 'term' in request.GET and field_name in self.autocomplete_fields:
            search_str = re.split(r'(?u)\s*',request.GET['term'])
            if len(search_str) <= len(self.autocomplete_fields[field_name]):
                search_fields =  self.autocomplete_fields[field_name][:len(search_str)]
            else:
                search_fields =  self.autocomplete_fields[field_name]
                search_str = search_str[:len(search_fields)]
            q_filters = []
            for term,field in  map(None,search_str,search_fields):
                filter_kwargs = {smart_str('{}__icontains'.format(field)):smart_str(term)}
                q_filters.append(models.Q(**filter_kwargs))
            mod = self._fields[field_name].rel.to
            items = mod.objects.all()
            items = items.filter(reduce(operator.iand, q_filters))
            json = [{'value':f.id,'label':str(f)} for f in items[:10]]
            if len(json) == 0:
                json = [{'value':'None','label':'Адрес не найден!'}]
        return HttpResponse(json_encode(json), mimetype="application/json")



class JqTreeGridView(JqGridView):

    def get_queryset(self):
        queryset = self.model.tree.all()
        return queryset

    def get_config(self, as_json=True):
        config = super(JqTreeGridView,self).get_config(as_json=False)
        config.update({
            'treeGrid':True,
            'treeGridModel':'nested',
            'ExpandColClick':True,
            #'treeIcons' : '',
            'ExpandColumn': 'name',
            'treeReader' : {
                'level_field': 'mptt_level',
                'left_field': 'lft',
                'right_field':'rght',
                'leaf_field': 'isLeaf',
                'expanded_field': 'expanded',
            }
            })

        if as_json:
            config = json_encode(config)
        return config

    def obj_to_row(self,obj):
        row = super(JqTreeGridView,self).obj_to_row(obj)
        row['isLeaf'] =  obj.is_leaf_node()
        row['expanded'] = not obj.is_leaf_node()
        return row

    def field_to_colmodel(self, field):
        field_model = super(JqTreeGridView,self).field_to_colmodel(field)
        if field.name in ['lft','rght','tree_id','auto_created','mptt_level']:
            field_model[0]['hidden'] = True
        return field_model
