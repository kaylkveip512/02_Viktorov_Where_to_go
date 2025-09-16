from django import forms

class PlaceForm(forms.Form):
    name = forms.CharField(
        max_length=200, 
        label="Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter the name of the place'})
    )
    
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe this place'})
    )
    
    PLACE_TYPES = [
        ('Synagogue', 'Gulliver'),
        ('KMC', 'Mohyla-Academy'),
        ('Bilui Naliv', 'Poshtova'),
        ('Troeschina', 'ny ce baza'),
        ('ATB', 'Kyiv'),
    ]
    
    place_type = forms.ChoiceField(
        choices=PLACE_TYPES,
        label="Place_type",
        initial='other'
    )
    
    location = forms.CharField(
        max_length=200, 
        label="Location",
        widget=forms.TextInput(attrs={'placeholder': 'Address'})
    )
    
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        label="Raiting",
        widget=forms.NumberInput(attrs={'min': 1, 'max': 5})
    )
    
    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating < 1 or rating > 5:
            raise forms.ValidationError("The rating should be from 1 to 5.")
        return rating
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name.strip():
            raise forms.ValidationError("The name cannot be empty")
        return name
