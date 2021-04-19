from django.forms.models import BaseInlineFormSet, inlineformset_factory

from .models import *
from .forms import SeccionForm, PlatoForm


class BaseSeccionesFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
    
        #save the formset in the 'nested' property
        form.nested = PlatosFormset(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix=f'{form.prefix}-{PlatosFormset.get_default_prefix()}'
        )
    
    def is_valid(self):
        result = super().is_valid()
        
        if self.is_bound:
            for form in self.forms:
                if not self._should_delete_form(form):
                    result = result and form.nested.is_valid()
                    
        return result
    
    def save(self, commit=True):
        result = super().save(commit=commit)
        
        for form in self.forms:
            if not self._should_delete_form(form):
                form.nested.save(commit=commit)
                
        return result
    
    def full_clean(self):
        super().full_clean()

        for error in self._non_form_errors.as_data():
            if error.code == 'too_many_forms':
                error.message = f'Por favor, envía menos de {self.max_num} secciones.'
            if error.code == 'too_few_forms':
                error.message = f'No se puede guardar una carta vacía.'
    
    
SeccionesFormset = inlineformset_factory(Carta, Seccion, form=SeccionForm, formset=BaseSeccionesFormset, extra=0, min_num=1, max_num=20, validate_min=True)

PlatosFormset = inlineformset_factory(Seccion, Plato, form=PlatoForm, extra=0, min_num=1, max_num=50, validate_min=True)