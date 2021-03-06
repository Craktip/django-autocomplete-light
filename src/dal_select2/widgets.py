"""Select2 widget implementation module."""

from dal.widgets import (
    QuerySetSelectMixin,
    Select,
    SelectMultiple,
    WidgetMixin
)

from django import forms
from django.utils import six
from django.utils import translation
from django.conf import settings


class Select2WidgetMixin(object):
    """Mixin for Select2 widgets."""

    def build_attrs(self, *args, **kwargs):
        attrs = super(Select2WidgetMixin, self).build_attrs(*args, **kwargs)
        lang_code = self._get_language_code()
        if lang_code:
            attrs.setdefault('data-autocomplete-light-language', lang_code)
        return attrs

    def _get_language_code(self):
        # get_language can be return None
        lang_code = translation.get_language()
        if lang_code:
            lang_code = translation.to_locale(lang_code).replace('_', '-')
        return lang_code

    def _media(self):
        """Automatically include static files for the admin."""
        _min = '' if settings.DEBUG else 'min.'
        i18n_file = ()
        lang_code = self._get_language_code()

        if lang_code:
            i18n_file = (
                'autocomplete_light/vendor/select2/dist/js/i18n/{}.js'.format(
                    lang_code),
            )
        css = (
            'autocomplete_light/vendor/select2/dist/css/select2.{}css'.format(
                _min),
            'autocomplete_light/select2.css',
        )
        js = ('autocomplete_light/jquery.init.js',
              'autocomplete_light/autocomplete.init.js',
              'autocomplete_light/vendor/select2/dist/js/select2.full.{}js'.format(
                  _min),
              ) + i18n_file + (
            'autocomplete_light/forward.js',
            'autocomplete_light/select2.js',
        )

        return forms.Media(css={'all': css}, js=js)

    media = property(_media)
    autocomplete_function = 'select2'


class Select2(Select2WidgetMixin, Select):
    """Select2 widget for regular choices."""


class Select2Multiple(Select2WidgetMixin, SelectMultiple):
    """Select2Multiple widget for regular choices."""


class ListSelect2(WidgetMixin, Select2WidgetMixin, forms.Select):
    """Select widget for regular choices and Select2."""


class ModelSelect2(QuerySetSelectMixin,
                   Select2WidgetMixin,
                   forms.Select):
    """Select widget for QuerySet choices and Select2."""


class ModelSelect2Multiple(QuerySetSelectMixin,
                           Select2WidgetMixin,
                           forms.SelectMultiple):
    """SelectMultiple widget for QuerySet choices and Select2."""


class TagSelect2(WidgetMixin,
                 Select2WidgetMixin,
                 forms.SelectMultiple):
    """Select2 in tag mode."""

    def build_attrs(self, *args, **kwargs):
        """Automatically set data-tags=1."""
        attrs = super(TagSelect2, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-tags', 1)
        return attrs

    def value_from_datadict(self, data, files, name):
        """Return a comma-separated list of options.
        This is needed because Select2 uses a multiple select even in tag mode,
        and the model field expects a comma-separated list of tags.
        """
        values = super(TagSelect2, self).value_from_datadict(data, files, name)
        return six.text_type(',').join(values)
