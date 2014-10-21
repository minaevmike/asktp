from django import forms

class AskForm(forms.Form):
	header = forms.CharField(widget = forms.Textarea(attrs={'type':'title', 'class':'form-control', 'placeholder':'Type title here','rows':'1','required':''}))
	body = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control','placeholder':'Type your question here','required':''}))
	tags = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control','placeholder':'Tags','rows':'1','required':''}))

class AnswerForm(forms.Form):
	content = forms.CharField(widget = forms.Textarea(attrs={'class':'form-control','placeholder':'Type your answer here','required':''}))

