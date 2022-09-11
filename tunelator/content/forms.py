from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget

class SocialContentForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'
