from django.contrib import admin
from . models import Province,Commune,Acteur,Colline,Groupe,Acteur_groupe,Reports,Utilisateur,Reponse

# Register your models here.
admin.site.register(Province)
admin.site.register(Commune)
admin.site.register(Acteur)
admin.site.register(Colline)
admin.site.register(Groupe)
admin.site.register(Acteur_groupe)
admin.site.register(Reports)
admin.site.register(Utilisateur)
admin.site.register(Reponse)