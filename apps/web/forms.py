from django.forms import *


class MovieSearchForm(Form):
    title = CharField(max_length=50,label = '',widget=TextInput(
                                                                attrs={
                                                                    'placeholder': 'Enter movie title here',
                                                                    'class' : 'form-control input-lg',
                                                                    # 'width':'40%',
                                                                    'id':'movietitle'

                                                                }))


class ProfileForm(Form):

    first_name = CharField(max_length=50, label='First Name', widget=TextInput(
        attrs={
            'placeholder': 'First Name',
            'class': 'form-control input-lg',
            'width': '40%',
            'id': 'firstname'

        }))


    last_name = CharField(max_length=50, label='Last Name', widget=TextInput(
            attrs={
            'placeholder': 'Last Name',
            'class': 'form-control input-lg',
                'width': '40%',
            'id': 'lastname'

            }))
    phone = CharField(max_length=11, label='Phone', widget=TextInput(
        attrs={
            'placeholder': 'phone',
            'class': 'form-control input-lg',
            'width': '40px',
            'id': 'phone'

        }))

    gender = CharField(max_length=50, label='Gender', widget=TextInput(
        attrs={
            'placeholder': 'gender',
            'width':'40%',
            'class': 'form-control input-lg',
            'id': 'gender'

        }))

    # picture = FileField(max_length=50, label='')
