{% block content %}
{% for post in object_list %}
<p>{{ post.datetime }}</p>
<h2><a href="{{ post.get_absolute_url }}">{{ post.title }}</a></h2>
<p>{{ post.content }}</p>
{% empty %}
<p>Нет постов</p>
{% endfor %}

{% endblock %}
