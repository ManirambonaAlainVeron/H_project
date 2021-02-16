from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   
    #province
    path('pr', views.afficher_province, name='pro_url'),
    path('delpro/<int:id_p>', views.supprimer_province, name='del_pro_url'),
    path('edtpro/<int:id_p>', views.editer_province, name='edt_pro_url'),
    path('updpro/<int:id_p>', views.update_province, name='up_pro_url'),
    path('addpro', views.ajouter_province, name='add_pro_url'),

    #commune
    path('cm', views.afficher_commune, name='cm_url'),
    path('delcm/<int:id_cm>', views.supprimer_commune, name='del_cm_url'),
    path('edtcm/<int:id_cm>', views.editer_commune, name='edt_cm_url'),
    path('updcm/<int:id_cm>', views.update_commune, name='up_cm_url'),
    path('addcm', views.ajouter_commune, name='add_cm_url'),
    path('chrcm', views.chercher_commune, name='chr_cm_url'),

    #colline
    path('col', views.afficher_colline, name='col_url'),
    path('delcol/<int:id_co>', views.supprimer_colline, name='del_col_url'),
    path('edtcol/<int:id_co>', views.editer_colline, name='edt_col_url'),
    path('updcol/<int:id_co>', views.update_colline, name='up_col_url'),
    path('addcol', views.ajouter_colline, name='add_col_url'),
    path('chrcol', views.chercher_colline, name='chr_col_url'),

    #categorie
    path('cat', views.afficher_categorie, name='cat_url'),
    path('delcat/<int:id_cat>', views.supprimer_categorie, name='del_cat_url'),
    path('edtcat/<int:id_cat>', views.editer_categorie, name='edt_cat_url'),
    path('updcat/<int:id_cat>', views.update_categorie, name='up_cat_url'),
    path('addcat', views.ajouter_categorie, name='add_cat_url'),

    #groupe
    path('grp', views.afficher_groupe, name='grp_url'),
    path('delgrp/<int:id_g>', views.supprimer_groupe, name='del_grp_url'),
    path('edtgrp/<int:id_g>', views.editer_groupe, name='edt_grp_url'),
    path('updgrp/<int:id_g>', views.update_groupe, name='up_grp_url'),
    path('addgrp', views.ajouter_groupe, name='add_grp_url'),

    #acteur
    path('act', views.afficher_acteur, name='act_url'),
    path('delact/<int:id_act>', views.supprimer_acteur, name='del_act_url'),
    path('edtact/<int:id_act>', views.editer_acteur, name='edt_act_url'),
    path('updact/<int:id_act>', views.update_acteur, name='up_act_url'),
    path('addact', views.ajouter_acteur, name='add_act_url'),
    path('chract', views.chercher_acteur, name='chr_act_url'),

    #acteur_groupe
    path('actgrp', views.afficher_acteur_groupe, name='actgrp_url'),
    path('delactgrp/<int:id_actgrp>', views.retirer_acteur_groupe, name='del_actgrp_url'),
    path('edtactgrp/<int:id_actgrp>', views.editer_acteur_groupe, name='edt_actgrp_url'),
    path('updactgrp/<int:id_actgrp>', views.update_acteur_groupe, name='up_actgrp_url'),
    path('addactgrp', views.ajouter_acteur_groupe, name='add_actgrp_url'),
    path('chractgrpnum', views.chercher_acteur_groupe_num, name='chr_act_num_url'),
    path('chractgrpgrp', views.chercher_acteur_groupe_grp, name='chr_act_grp_url'),

    #utilisateur
    path('util', views.afficher_utilisateur, name='util_url'),
    path('delutil/<int:id_util>', views.supprimer_utilisateur, name='del_util_url'),
    path('edtutil/<int:id_util>', views.editer_utilisateur, name='edt_util_url'),
    path('updutil/<int:id_util>', views.update_utilisateur, name='up_util_url'),
    path('addutil', views.ajouter_utilisateur, name='add_util_url'),
    path('chrutil', views.chercher_utilisateur, name='chr_util_url'),

    #change_pass
    path('chg', views.afficher_change_pwd, name='chg_url'),
    path('addchg', views.change_pwd, name='addchg_url'),
]