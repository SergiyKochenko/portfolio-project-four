from .models import Comment
from django import forms
from .models import Post


# ==============================================================================
from .models import Booking
from django.core.validators import MinValueValidator
import datetime





def get_min_date():
    """Returns the current date plus 2 days, so the user
    can book appointment 2 days in advance
     """
    return datetime.date.today() + datetime.timedelta(days=2)


class DateInput(forms.DateInput):
    """This class provides a calendar widget that the user can
    pick the booking date.
    """
    input_type = 'date'


class BookingForm(forms.ModelForm):
    """This class generates a form from the Booking model
    """

    date = forms.DateField(
        validators=[MinValueValidator(get_min_date)],
        widget=DateInput(attrs={'type': 'date', 'min': get_min_date}))

    class Meta:
        model = Booking
        fields = ('name', 'phone', 'email', 'service', 'date', 'time')
        widgets = {'date': DateInput()}



# ===========================================================================


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'content', 'featured_image')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'content', 'featured_image')