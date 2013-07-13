from django.forms import ModelForm
from quiz.models import quiz


class quizForm(ModelForm):
	class Meta:
		model = quiz
		fields = ['title','questions_file','start_time','end_time','description','duration','number_of_questions','type']
			