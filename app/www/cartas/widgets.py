from django.forms import widgets

    
class LabeledInput(widgets.TextInput):
    label_text = ''
    template_name = 'widgets/labeled_input.html'
    
    def __init__(self, attrs=None):
        if attrs is not None:
            attrs = attrs.copy()
            self.label_text = attrs.pop('label', self.label_text)
            self.label_right = attrs.pop('right', False)
        super().__init__(attrs)
        
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label'] = self.label_text
        context['widget']['right'] = self.label_right
        return context