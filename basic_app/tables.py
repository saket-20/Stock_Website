from basic_app.models import UserProfileInfo,stocks
import django_tables2 as tables
class SimpleTable(tables.Table):
    class Meta:
        model = stocks
        attrs = {"class":"paleblue"}
        template_name = 'django_tables2/bootstrap.html'
