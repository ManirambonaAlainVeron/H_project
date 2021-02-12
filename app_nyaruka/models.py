from django.db import models
from django.contrib.auth.models import User

class Province(models.Model):
    nom_pro = models.CharField(max_length=50)

    class Meta:
        db_table = 'Province'

class Commune(models.Model):
    nom_com = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    class Meta:
        db_table = 'Commune'

class Acteur(models.Model):
    nom_act = models.CharField(max_length=50)
    prenom_act = models.CharField(max_length=50)
    telephone_act = models.CharField(max_length=50)
    num_ide_act = models.CharField(max_length=50)
    etat_act = models.CharField(max_length=50)

    class Meta:
        db_table = 'Acteur'
    
class Colline(models.Model):
    nom_col = models.CharField(max_length=50)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE)
    acteur = models.ForeignKey(Acteur, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Colline'

class Groupe(models.Model):
    nom_groupe = models.CharField(max_length=50)

    class Meta:
        db_table = 'Groupe'

class Acteur_groupe(models.Model):
    groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE)
    acteur = models.ForeignKey(Acteur, on_delete=models.CASCADE)
    etat_act_group = models.CharField(max_length=50)

    class Meta:
        db_table = 'Acteur_groupe'

class Categorie(models.Model):
    nom_cat = models.CharField(max_length=80)

    class Meta:
        db_table = 'Categorie'

class Reports(models.Model):
    acteur = models.ForeignKey(Acteur, on_delete=models.CASCADE)
    contenu_mes = models.TextField()
    date_mes = models.DateField(auto_now_add=True)
    heure_mes = models.TimeField(auto_now_add=True)
    categories = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Reports'

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_uti = models.CharField(max_length=50)
    prenom_uti = models.CharField(max_length=50)
    num_id_uti = models.CharField(max_length=50)
    telephone_uti = models.CharField(max_length=50)
    profil_act = models.CharField(max_length=50)
    etat_act = models.CharField(max_length=50)

    class Meta:
        db_table = 'Utilisateur'

class Reponse(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    acteur = models.ForeignKey(Acteur, on_delete=models.CASCADE)
    contenu_mes = models.TextField()
    date_mes = models.DateField(auto_now_add=True)
    heure_mes = models.TimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Reponse'

