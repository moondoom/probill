# -*- coding: utf-8 -*-
from django.db.models.fields import NOT_PROVIDED

class GenericField():

    def __init_(self,field,name=None):
        self.model_field = field
        if name:
            self.name = name
        else:
            self.name = self.model_field.name

    def is_key(self):
        return self.model_field.primary_key

    def is_hidden(self):
        return self.is_key

    def is_editable(self):
        return not self.is_key() and self.model_field.editable

    def is_required(self):
        return not self.model_field.blank

    def get_label(self):
        return unicode(self.model_field.verbose_name)

    def get_index(self):
        return self.model_field.name

    def get_default_value(self):
        if self.model_field.default <> NOT_PROVIDED:
            if hasattr(self.model_field.default,'__call__'):
                return self.model_field.default()
            else:
                return self.model_field.default

    def get_edit_options(self):
        return {}

    def get_edit_type(self):
        return 'text'

    def get_format_options(self):
        return {}

    def get_format_type(self):
        return self.get_edit_type()

    def get_edit_rules(self):
        return {
            'edithidden' : not self.is_editable(),
            'required': self.is_required(),
        }

    def has_choices(self):
        if self.model_field.choices:
            return True
        else:
            return False

    def get_choices(self):
        select = {}
        for id,val in self.model_field.get_choices():
           select[unicode(id)] = unicode(val)
        return select

    def get_values(self,obj):
        values = {}
        obj_field = getattr(obj,self.model_field.name)
        if obj_field:
            values[self.name] = unicode(obj_field)
        else:
            values[self.name] = ''
        return values

    def get_default_col_model(self):
        return {
            'name': self.get_index(),
            'index':  self.get_index(),
            'label': self.get_label(),
            'editable': self.is_editable(),
            'key': self.is_key(),
            'hidden': self.is_hidden(),
            'edittype': self.get_edit_type(),
            'editoptions': self.get_edit_options(),
            'editrules': self.get_edit_rules(),
            'formatter': self.get_format_type(),
            'formoptions': self.get_format_options(),
        }

    def get_col_models(self):
        col_model  = self.get_default_col_model()
        col_model.update(self.get_edit_options())
        col_model.update(self.get_format_options())
        return [col_model]

class TextField(GenericField):

    def get_edit_type(self):
        if self.has_choices():
            return 'select'

    def get_edit_options(self):
        if self.has_choices():
            return {'value': self.get_choices()}
        else:
            return {}

