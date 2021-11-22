import django_tables2 as tables
from .models import Contact

class CheckboxTable(tables.Table):
    edit = tables.TemplateColumn('<button class="button button2"><a href="../contact/{{record.id}}">edit</a></button')
    delete = tables.TemplateColumn('<button class="button button3"><a href="../contact/{{record.id}}/delete">delete</a></button')




    class Meta:
        model = Contact
        template_name = "django_tables2/bootstrap.html"
        fields = ( "contact_name","contact_organisation", "contact_email", "contact_mobile", "startlist", "results", "communiques",)
        orderable = False