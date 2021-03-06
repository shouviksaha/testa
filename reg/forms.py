from django import forms

class loginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput())
	
class clientRegistrationForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput())
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	details = forms.CharField(widget=forms.Textarea,max_length=500)



class studentRegistrationForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput())
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name = forms.CharField(max_length=100)
	college = forms.CharField(max_length = 250)
	department_choices = (
                ('IT', 'IT'),
                ('CSE', 'CSE'),
                ('MCA', 'MCA'),
                ('BT', 'BT'),
                ('CE', 'CE'),
                ('CHE', 'CHE'),
                ('ECE', 'ECE'),
                ('EE', 'EE'),
                ('ME', 'ME'),
                ('MME', 'MME'),
                ('Other', 'Other'),
            )
	department = forms.ChoiceField(choices=department_choices)
	year_choices = (
					 ('2014', '2014'),
                ('2015', '2015'),                
                ('2016', '2016'),
        )
	year = forms.ChoiceField(choices=year_choices,label = 'Expected year of passing')
	phone = forms.IntegerField()
	