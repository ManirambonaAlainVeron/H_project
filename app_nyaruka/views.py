from django.shortcuts import render, redirect
from django.http import request
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError 
from django.core.exceptions import ObjectDoesNotExist
from .models import Province, Colline, Commune, Acteur, Acteur_groupe, Utilisateur, Groupe, Categorie, Reports, Reponse
import ast
from django.contrib.auth import authenticate, login, logout

# Create your views here.

#Auth
def my_auth(request):
    return render(request,"Authentification.html")

def connexion_utilisateur(request):
     if request.method == 'POST':
        username = request.POST.get('txt_login')
        password = request.POST.get('txt_pass')
        if len(username) != 0 or len(password) != 0:
            user = authenticate(username=username, password=password)
            if user:
                try:
                    profil = Utilisateur.objects.values(
                        'profil').get(user__username=user)
                except ObjectDoesNotExist:
                    messages.info(request, "Impossible de se connecter, réessayez plus tard!")
                    type_msg = "error"
                    return render(request,"Authentification.html",{'type_msg':type_msg})
                if profil['profil'] == "admin":
                    login(request, user)
                    return redirect("act_url")
                else:
                    login(request, user)
                    return redirect("env_url")
            else:
                type_msg = "error"
                messages.info(request, "Echec de connexion, le numero ou le mot de passe est incorrecte ou tu es desactivé !")
                return render(request,"Authentification.html",{'type_msg':type_msg})
        else:
            messages.info(request,"Entrez le numero et le mot de passe svp!")
            type_msg = "error"
            return render(request,"Authentification.html",{'type_msg':type_msg})

def deconnexion_utilisateur(request):
    logout(request)
    return redirect("auth_url")
            
#env_sms
def afficher_envoyer_sms(request):
    groupes = Groupe.objects.all().order_by("nom_groupe")
    return render (request, "envoyer_sms.html",locals())

def afficher_sms_envoye(request):
    sms_envoyes = Reponse.objects.values('id','contenu_mes','date_mes','heure_mes','acteur__telephone_act','utilisateur__prenom_uti','acteur__prenom_act').order_by('date_mes','heure_mes')
    return render(request, "afficher_sms_envoyer.html", locals())

def supprimer_sms_envoyer(request, id_msg):
    Reponse.objects.get(pk = id_msg).delete()
    messages.info(request,"La suppresion est reussie avec succes !")
    return redirect("affenv_url")

def envoyer_sms(request):
    if request.method == "POST":
        typ = request.POST.get('type')
        numero = request.POST.get('num').strip()
        grp = request.POST.get('select_grp')
        msg = request.POST.get('msg').strip()
        if len(typ) != 0:
                if typ == "acteur":
                    if len(numero) == 0:
                        groupes = Groupe.objects.all().order_by("nom_groupe")
                        messages.info(request,"Entrez le numero du destinateur svp !")
                        type_msg = "error"
                        return render (request, "envoyer_sms.html",{'type_msg':type_msg})
                    else:
                        if len(msg) == 0:
                            groupes = Groupe.objects.all().order_by("nom_groupe")
                            messages.info(request,"Tapez le message svp !")
                            type_msg = "error"
                            return render (request, "envoyer_sms.html",locals())
                        else:
                            #envoyer a un acteur
                            if Acteur.objects.filter(telephone_act=numero, etat_act="non bloquer").exists():
                                id_act = Acteur.objects.values('id').get(telephone_act=numero)
                                username_util = request.user.username
                                id_uti = Utilisateur.objects.values('id').get(user__username=username_util)
                                #----------send SMS----------

                                messages.info(request,"Message envoyé!")
                                return render (request, "envoyer_sms.html",locals())
                            else:
                                groupes = Groupe.objects.all().order_by("nom_groupe")
                                messages.info(request,"Echec,numero inconu ou bien l'acteur est bloqué !")
                                type_msg = "error"
                                return render (request, "envoyer_sms.html",locals()) 
                            #envoyer a un acteur
                else:
                    if len(grp) == 0:
                        groupes = Groupe.objects.all().order_by("nom_groupe")
                        messages.info(request,"Selectionnez le groupe destinateur svp !")
                        type_msg = "error"
                        return render (request, "envoyer_sms.html",locals())
                    else:
                        if len(msg) == 0:
                            groupes = Groupe.objects.all().order_by("nom_groupe")
                            messages.info(request,"Tapez le message svp !")
                            type_msg = "error"
                            return render (request, "envoyer_sms.html",locals())
                        else:
                        #envoyer a un groupe
                            if Acteur_groupe.objects.filter(groupe=grp, etat_act_group="non bloquer"):
                                username_util = request.user.username
                                id_uti = Utilisateur.objects.values('id').get(user__username=username_util)
                                #----select tous les membres(id,number)
                                list_member = Acteur_groupe.objects.values('acteur','acteur__telephone_act').filter(groupe=grp)
                                #----send SMS------

                                messages.info(request,"Message envoyé à tous les membres du groupe!")
                                return render (request, "envoyer_sms.html",locals())
                            else:
                                groupes = Groupe.objects.all().order_by("nom_groupe")
                                messages.info(request,"Echec,le groupe n'a pas des membres ou bien ils sont bloqués !")
                                type_msg = "error"
                                return render (request, "envoyer_sms.html",{'type_msg':type_msg})
        else:
            groupes = Groupe.objects.all().order_by("nom_groupe")
            messages.info(request,"Selectionnez le type du destinateur svp !")
            type_msg = "error"
            return render (request, "envoyer_sms.html",{'type_msg':type_msg})

# provinces
def afficher_province(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        provinces = Province.objects.all().order_by("id")
        return render(request,"province.html",locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def ajouter_province(request):
    if request.method == "POST":
        nom = request.POST.get("nom_prov")
        if len(nom) == 0:
            messages.info(request,"Saisissez le nom du province svp !")
            type_msg = "error"
            provinces = Province.objects.all().order_by("id")
            return render(request,"province.html",{'type_msg':type_msg,'provinces':provinces})
        else:
            p = Province(nom_pro = nom)
            p.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect("pro_url")

def supprimer_province(request, id_p): 
    Province.objects.get(pk = id_p).delete()
    messages.info(request,"La suppresion est reussie avec succes !")
    return redirect("pro_url")

def editer_province(request, id_p):
    provinces = Province.objects.get(pk = id_p)
    return render(request,"province_edit.html",{'provinces':provinces})

def update_province(request, id_p):
    if request.method == "POST":
        nom = request.POST.get("nom_prov")
        if len(nom) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("pro_url")
        else:
            p = Province.objects.get(pk = id_p)
            p.nom_pro = request.POST.get("nom_prov")
            p.save()
            messages.info(request,"La modification est reussie avec succes !")
            return redirect("pro_url")

#commune
def afficher_commune(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        communes = Commune.objects.values('id','province__nom_pro','nom_com').order_by("id")
        provinces = Province.objects.all().order_by("nom_pro")
        return render(request, "commune.html", locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def ajouter_commune(request):
    if request.method == "POST":
        pro = request.POST.get("select_pro")
        com = request.POST.get("nom_com")
        if len(pro) == 0:
            provinces = Province.objects.all().order_by("nom_pro")
            communes = Commune.objects.values('id','province__nom_pro','nom_com').order_by("id")
            messages.info(request,"Selectionnez la province svp !")
            type_msg = "error"
            return render(request,"commune.html",{'type_msg':type_msg,'communes':communes,'provinces':provinces })
        elif len(com) == 0:
            provinces = Province.objects.all().order_by("nom_pro")
            communes = Commune.objects.values('id','province__nom_pro','nom_com').order_by("id")
            messages.info(request,"Saisissez le nom de la commune svp !")
            type_msg = "error"
            return render(request,"commune.html",{'type_msg':type_msg,'communes':communes, 'provinces':provinces})
        else:
            c = Commune(province = Province(pro), nom_com = com)
            c.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect("cm_url")

def supprimer_commune(request, id_cm): 
    Commune.objects.get(pk = id_cm).delete()
    messages.info(request,"La suppresion est reussie avec succes !")
    return redirect("cm_url")

def editer_commune(request, id_cm):
    communes = Commune.objects.get(pk = id_cm)
    provinces = Province.objects.all().order_by("nom_pro")
    id_province = Commune.objects.values("province").get(pk=id_cm)
    id_p = id_province['province']
    province = Province.objects.values("nom_pro").get(pk=id_p)
    nom_province = province['nom_pro']
    return render(request,"commune_edit.html",locals())

def update_commune(request, id_cm):
    if request.method == "POST":
        pro = request.POST.get("select_pro")
        com = request.POST.get("nom_com")
        if len(pro) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("cm_url")
        elif len(com) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("cm_url")
        else:
            c = Commune.objects.get(pk = id_cm)
            c.province = Province(pro)
            print("-------",Province(pro))
            c.nom_com = com
            c.save()
            messages.info(request,"La modification est reussie avec succes !")
            return redirect("cm_url")

'''def chercher_commune(request):
    if request.method == 'GET':
        nom = request.GET.get('cherch_com').strip()
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom de la commune à chercher svp !")
            return redirect('cm_url')
        else:
            liste = Commune.objects.values('id','province__nom_pro','nom_com').filter(nom_com=nom)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "La commune n'existe pas dans le system ou verifier l'orthographe svp !")
                return redirect('cm_url')
            else:
                return render(request, "commune.html",{'communes':liste})'''

#colline
def afficher_colline(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').filter(etat_act='non bloquer').order_by("nom_act")
        communes = Commune.objects.all().order_by("id")
        collines = Colline.objects.values('id','commune__nom_com','nom_col','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').order_by("id")
        return render(request, "colline.html", locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def ajouter_colline(request):
    if request.method == "POST":
        com = request.POST.get("select_com")
        col = request.POST.get("nom_col")
        act = request.POST.get("select_act")

        if len(act) == 0:
            acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').filter(etat_act='non bloquer').order_by("nom_act")
            communes = Commune.objects.all().order_by("id")
            collines = Colline.objects.values('id','commune__nom_com','nom_col','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').order_by("id")
            messages.info(request,"Selectionnez l'acteur' !")
            type_msg = "error"
            return render(request,"colline.html",locals())
        elif len(com) == 0:
            acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').filter(etat_act='non bloquer').order_by("nom_act")
            communes = Commune.objects.all().order_by("id")
            collines = Colline.objects.values('id','commune__nom_com','nom_col','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').order_by("id")
            messages.info(request,"Saisissez le nom de la commune svp !")
            type_msg = "error"
            return render(request,"colline.html",locals())
        elif len(col) == 0:
            acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').filter(etat_act='non bloquer').order_by("nom_act")
            communes = Commune.objects.all().order_by("id")
            collines = Colline.objects.values('id','commune__nom_com','nom_col','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').order_by("id")
            messages.info(request,"Saisissez le nom de la colline svp !")
            type_msg = "error"
            return render(request,"colline.html",locals())
        else:
            co = Colline(acteur = Acteur(act),commune=Commune(com), nom_col = col)
            co.save()
            acteur_nom = Acteur.objects.values('nom_act').get(pk=act)
            messages.info(request, ""+acteur_nom['nom_act']+" est maintenant le responsable de la colline "+col+"!")
            return redirect("col_url")

def supprimer_colline(request, id_co): 
    Colline.objects.get(pk = id_co).delete()
    messages.info(request,"La suppresion est reussie avec succes !")
    return redirect("col_url")

def editer_colline(request, id_co):
    collines = Colline.objects.get(pk = id_co)
    communes = Commune.objects.all().order_by("id")
    acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').filter(etat_act='non bloquer').order_by("nom_act")
    acteur_select = Colline.objects.values('id','acteur','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').get(pk=id_co)
    id_commune = Colline.objects.values("commune").get(pk=id_co)
    nom_commune = Commune.objects.values("nom_com").get(pk=id_commune['commune'])
    return render(request,"colline_edit.html",locals())

def update_colline(request, id_co):
    if request.method == "POST":
        com = request.POST.get("select_com")
        col = request.POST.get("nom_com")
        act = request.POST.get("select_act")
        if len(col) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("col_url")
        elif len(com) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("col_url")
        elif len(act) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("col_url")
        else:
            co = Colline.objects.get(pk = id_co)
            co.commune = Commune(com)
            co.nom_col = col
            co.acteur = Acteur(act)
            co.save()
            messages.info(request,"La modification est reussie avec succes !")
            return redirect("col_url")

'''def chercher_colline(request):
    if request.method == 'GET':
        nom = request.GET.get('cherch_col').strip()
        if len(nom) == 0:
            messagess.info(request, "Saisissez le nom de la colline à chercher svp !")
            return redirect('col_url')
        else:
            liste = Colline.objects.values('id','commune__nom_com','nom_col','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').filter(nom_col=nom)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messagess.info(request, "La colline n'existe pas dans le system ou verifier l'orthographe svp !")
                return redirect('col_url')
            else:
                return render(request, "colline.html",{'collines':liste})'''


# categorie
def afficher_categorie(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        categories = Categorie.objects.all().order_by("id")
        return render(request,"categorie.html",locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def ajouter_categorie(request):
    if request.method == "POST":
        nom = request.POST.get("nom_cat")
        if len(nom) == 0:
            categories = Categorie.objects.all().order_by("id")
            messages.info(request,"Saisissez le nom du categorie svp !")
            type_msg = "error"
            return render(request,"categorie.html",{'type_msg':type_msg,'categories':categories})
        else:
            cat = Categorie(nom_cat = nom)
            cat.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect("cat_url")

def supprimer_categorie(request, id_cat): 
    Categorie.objects.get(pk = id_cat).delete()
    messages.info(request,"La suppresion est reussie avec succes !")
    return redirect("cat_url")

def editer_categorie(request, id_cat):
    categorie = Categorie.objects.get(pk = id_cat)
    return render(request,"categorie_edit.html",{'categories':categorie})

def update_categorie(request, id_cat):
    if request.method == "POST":
        nom = request.POST.get("nom_cat")
        if len(nom) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("cat_url")
        else:
            cat = Categorie.objects.get(pk = id_cat)
            cat.nom_cat = request.POST.get("nom_cat")
            cat.save()
            messages.info(request,"La modification est reussie avec succes !")
            return redirect("cat_url")


# groupe
def afficher_groupe(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        groupes = Groupe.objects.all().order_by("id")
        return render(request,"groupe.html",locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def ajouter_groupe(request):
    if request.method == "POST":
        nom = request.POST.get("nom_grp")
        if len(nom) == 0:
            groupe = Groupe.objects.all().order_by("id")
            messages.info(request,"Saisissez le nom du groupe svp !")
            type_msg = "error"
            return render(request,"groupe.html",{'type_msg':type_msg,'groupe':groupe})
        else:
            g = Groupe(nom_groupe = nom)
            g.save()
            messages.info(request, "Enregistrement reussi avec succes !")
            return redirect("grp_url")

def supprimer_groupe(request, id_g): 
    Groupe.objects.get(pk = id_g).delete()
    messages.info(request,"La suppresion est reussie avec succes !")
    return redirect("grp_url")

def editer_groupe(request, id_g):
    groupes = Groupe.objects.get(pk = id_g)
    return render(request,"groupe_edit.html",{'groupes':groupes})

def update_groupe(request, id_g):
    if request.method == "POST":
        nom = request.POST.get("nom_grp")
        if len(nom) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("grp_url")
        else:
            g = Groupe.objects.get(pk = id_g)
            g.nom_groupe = request.POST.get("nom_grp")
            g.save()
            messages.info(request,"La modification est reussie avec succes !")
            return redirect("grp_url")


#acteur
def afficher_acteur(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        acteurs = Acteur.objects.all().order_by("id")
        return render(request,"acteur.html",locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def ajouter_acteur(request):
    if request.method == "POST":
        nom = request.POST.get("nom_act")
        prenom = request.POST.get("prenom_act")
        identite = request.POST.get("num_id")
        tel = request.POST.get("num_tel")
        etat = request.POST.get("etat_act")
        if len(nom) == 0:
            acteurs = Acteur.objects.all().order_by("id")
            messages.info(request,"Saisissez le nom de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur.html",{'type_msg':type_msg,'acteurs':acteurs})
        elif len(prenom) == 0:
            acteurs = Acteur.objects.all().order_by("id")
            messages.info(request,"Saisissez le prenom de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur.html",{'type_msg':type_msg,'acteurs':acteurs})
        elif len(tel) == 0:
            acteurs = Acteur.objects.all().order_by("id")
            messages.info(request,"Saisissez le numero de téléphone de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur.html",{'type_msg':type_msg,'acteurs':acteurs})
        else:
            if Acteur.objects.filter(telephone_act=tel).exists():
                acteurs = Acteur.objects.all().order_by("id")
                messages.info(request,"Echec, ce numero existe déjà la duplication des numero est interdit !")
                type_msg = "error"
                return render(request,"acteur.html",{'type_msg':type_msg,'acteurs':acteurs})
            else:
                act = Acteur(nom_act = nom, prenom_act = prenom, telephone_act = tel, num_ide_act = identite, etat_act = etat)
                act.save()
                messages.info(request, "Enregistrement reussi avec succes !")
                return redirect("act_url")

def supprimer_acteur(request, id_act): 
    Acteur.objects.get(pk = id_act).delete()
    messages.info(request,"La suppresion est reussie avec succes !")
    return redirect("act_url")

def editer_acteur(request, id_act):
    acteur = Acteur.objects.get(pk = id_act)
    etat = Acteur.objects.values("etat_act").get(pk=id_act)
    return render(request,"acteur_edit.html",locals())

def update_acteur(request, id_act):
    if request.method == "POST":
        nom = request.POST.get("nom_act")
        prenom = request.POST.get("prenom_act")
        identite = request.POST.get("num_id")
        tel = request.POST.get("num_tel")
        etat = request.POST.get("etat_act")
        if len(nom) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("act_url")
        elif len(prenom) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("act_url")
        elif len(tel) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("act_url")
        else:
            act = Acteur.objects.get(pk = id_act)
            act.nom_act = nom
            act.prenom_act = prenom
            act.telephone_act = tel
            act.num_ide_act = identite
            act.etat_act = etat
            act.save()
            messages.info(request,"La modification est reussie avec succes !")
            return redirect("act_url")

'''def chercher_acteur(request):
    if request.method == 'GET':
        numero = request.GET.get('cherch_act').strip()
        if len(numero) == 0:
            acteurs = Acteur.objects.all().order_by("id")
            messages.info(request, "Saisissez le numero de l'acteur communauteur à chercher svp !")
            type_msg = "error"
            return render(request,"acteur.html",{'type_msg':type_msg,'acteurs':acteurs})
        else:
            liste = Acteur.objects.values('id','nom_act','prenom_act','num_ide_act','telephone_act','etat_act').filter(telephone_act=numero)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "L'acteur n'existe pas dans le system ou bien verifier les numero !")
                return redirect('act_url')
            else:
                return render(request, "acteur.html",{'acteurs':liste})'''


#acteur_groupe
def afficher_acteur_groupe(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').filter(etat_act='non bloquer').order_by("nom_act")
        groupes = Groupe.objects.all().order_by("id")
        acteur_groupe = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_act','acteur__telephone_act','groupe__nom_groupe','etat_act_group').order_by("id")
        return render(request, "acteur_groupe.html", locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def retirer_acteur_groupe(request,id_actgrp):
    act = Acteur_groupe.objects.values('acteur__nom_act','acteur__prenom_act').get(pk = id_actgrp)
    Acteur_groupe.objects.get(pk = id_actgrp).delete()
    messages.info(request,"L'acteur communauteur "+act['acteur__nom_act']+" "+act['acteur__prenom_act']+" est retiré dans le groupe !")
    return redirect("actgrp_url")

def ajouter_acteur_groupe(request):
        if request.method == "POST":
            acteur = request.POST.get("select_act")
            groupe = request.POST.get("select_grp")
            etat = request.POST.get("etat_actgrp")
            if len(acteur) == 0:
                acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').order_by("nom_act")
                groupes = Groupe.objects.all().order_by("id")
                acteur_groupe = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_act','acteur__telephone_act','groupe__nom_groupe','etat_act_group').order_by("id")
                messages.info(request,"Selectionnez l'acteur svp!")
                type_msg = "error"
                return render(request,"acteur_groupe.html",locals())
            elif len(groupe) == 0:
                acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').order_by("nom_act")
                groupes = Groupe.objects.all().order_by("id")
                acteur_groupe = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_cat','acteur__telephone_act','groupe__nom_groupe','etat_act_group').order_by("id")
                messages.info(request,"Selectionnez le groupe svp!")
                type_msg = "error"
                return render(request,"acteur_groupe.html",locals())
            else:
                act = Acteur_groupe(acteur = Acteur(acteur), groupe = Groupe(groupe), etat_act_group = etat)
                act.save()
                messages.info(request, "Enregistrement reussi avec succes !")
                return redirect("actgrp_url")

'''def chercher_acteur_groupe_num(request):
    if request.method == 'GET':
        num = request.GET.get('cherch_actgrp').strip()
        num.trim()
        if len(num) == 0:
            acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').order_by("nom_act")
            groupes = Groupe.objects.all().order_by("id")
            acteur_groupe = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_act','acteur__telephone_act','groupe__nom_groupe','etat_act_group').order_by("id")
            messages.info(request, "Saisissez le numero de l'acteur communauteur à chercher svp !")
            type_msg = "error"
            return render(request,"acteur_groupe.html",locals())
        else:
            liste = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_act','acteur__telephone_act','groupe__nom_groupe','etat_act_group').filter(acteur__telephone_act=num)
            nbr = liste.count()
            if nbr == 0:
                acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').order_by("nom_act")
                groupes = Groupe.objects.all().order_by("id")
                acteur_groupe = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_cat','acteur__telephone_act','groupe__nom_groupe','etat_act_group').order_by("id")
                type_msg = "error"
                messages.info(request, "L'acteur appartient à aucun groupe !")
                return render(request,"acteur_groupe.html",locals())
            else:
                return render(request, "acteur_groupe.html",{'acteur_groupe':liste})'''


'''def chercher_acteur_groupe_grp(request):
    if request.method == 'GET':
        grp = request.GET.get('cherch_grpact').strip()
        if len(grp) == 0:
            messages.info(request, "Saisissez le nom du groupe à chercher svp !")
            acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').order_by("nom_act")
            groupes = Groupe.objects.all().order_by("id")
            acteur_groupe = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_act','acteur__telephone_act','groupe__nom_groupe','etat_act_group').order_by("id")
            type_msg = "error"
            return render(request,"acteur_groupe.html",locals())
        else:
            liste = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_act','acteur__telephone_act','groupe__nom_groupe','etat_act_group').filter(groupe__nom_groupe=grp)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "Le groupe a aucun acteur !")
                return redirect('act_actgrp_url')
            else:
                return render(request, "acteur_groupe.html",{'acteur_groupe':liste})'''


def editer_acteur_groupe(request, id_actgrp):
    acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').filter(etat_act='non bloquer').order_by("nom_act")
    acteur_select = Acteur_groupe.objects.values('id','acteur','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').get(pk=id_actgrp)
    groupes = Groupe.objects.all().order_by("id")
    groupe_select = Acteur_groupe.objects.values('groupe','groupe__nom_groupe').get(pk=id_actgrp)
    etat = Acteur_groupe.objects.values("etat_act_group").get(pk=id_actgrp)
    return render(request,"acteur_groupe_edit.html",locals())

def update_acteur_groupe(request, id_actgrp):
    if request.method == "POST":
        act = request.POST.get("select_act")
        grp = request.POST.get("select_grp")
        et = request.POST.get("etat_actgrp")
        if len(act) == 0:
            messages.info(request,"Selectionnez l'acteur svp !")
            type_msg = "error"
            return render(request,"acteur_groupe_edit.html",{'type_msg':type_msg})
        if len(grp) == 0:
            messages.info(request,"Selectionnez le groupe svp !")
            type_msg = "error"
            return render(request,"acteur_groupe_edit.html",{'type_msg':type_msg})
        else:
            act_grp = Acteur_groupe.objects.get(pk = id_actgrp)
            act_grp.acteur = Acteur(act)
            act_grp.groupe = Groupe(grp)
            act_grp.etat_act_group = et
            act_grp.save()
            messages.info(request,"La modification est reussie avec succes !")
            return redirect('actgrp_url')


#utilisateur
def afficher_utilisateur(request):
    try:
        user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
        utilisateurs = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'num_id_uti','user__username', 'profil', 'user__is_active').order_by("id")
        return render(request,"utilisateur.html",locals())
    except ObjectDoesNotExist:
        return redirect("auth_url")

def ajouter_utilisateur(request):
    if request.method == "POST":
        nom = request.POST.get('txt_nom')
        prenom = request.POST.get('txt_prenom')
        identifiant = request.POST.get('txt_num_id')
        telephone = request.POST.get('txt_tel')
        password = request.POST.get('txt_pass')
        etat = request.POST.get('txt_etat')
        profil = request.POST.get('txt_profil')
        if len(nom) == 0 or len(prenom) == 0 or len(telephone) == 0 or len(password) == 0 or len(etat) == 0 or len(profil) == 0:
            utilisateurs = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'num_id_uti','user__username', 'profil', 'user__is_active').order_by("id")
            type_msg = "error"
            messages.info(request, "Completez tous les informations svp !")
            return render(request,"utilisateur.html",{'type_msg':type_msg,'utilisateurs':utilisateurs})
        else:
            password_confirm = request.POST.get('txt_conf')
            if password != password_confirm:
                utilisateurs = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'num_id_uti','user__username', 'profil', 'user__is_active').order_by("id")
                type_msg = "error"
                messages.info(request, "Echec, mot de passe et la confirmation n'est pas identique !")
                return render(request,"utilisateur.html",{'type_msg':type_msg,'utilisateurs':utilisateurs})
            else:
                if Utilisateur.objects.filter(user__username=telephone).exists():
                    utilisateurs = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'num_id_uti','user__username', 'profil', 'user__is_active').order_by("id")
                    type_msg = "error"
                    messages.info(request, "Echec! ce numero existe déjà la duplication des numero de téléphone est interdit !")
                    return render(request,"utilisateur.html",{'type_msg':type_msg,'utilisateurs':utilisateurs})
                else:
                    try:
                        user = User.objects.create_user(username=telephone, password=password, is_active=etat)
                        utilisateur = Utilisateur(user = user, nom_uti = nom, prenom_uti = prenom, num_id_uti = identifiant ,profil = profil)
                        utilisateur.save()
                        messages.info(request, "La creation d'un utilisateur reussi avec succes !")
                        return redirect('util_url')
                    except IntegrityError :
                        utilisateurs = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'num_id_uti','user__username', 'profil', 'user__is_active').order_by("id")
                        type_msg = "error"
                        messages.info(request, "Echec!! le numero ou le mot de passe existe déjà !")
                        return render(request,"utilisateur.html",{'type_msg':type_msg,'utilisateurs':utilisateurs})
                

def supprimer_utilisateur(request, id_util): 
        utilisateur = Utilisateur.objects.get(pk=id_util)
        users = utilisateur.user
        utilisateur.delete()
        users.delete()
        messages.info(request, "La suppression est reussie avec succes !")
        return redirect("util_url")

def editer_utilisateur(request, id_util):
    utilisateurs = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'user__username','num_id_uti', 'user__is_active', 'profil').get(pk=id_util)
    return render(request, "utilisateur_edit.html", {'utilisateurs':utilisateurs})

def update_utilisateur(request, id_util):
    if request.method == "POST":
        nom = request.POST.get('txt_nom')
        prenom = request.POST.get('txt_prenom')
        identifiant = request.POST.get('txt_num_id')
        telephone = request.POST.get('txt_tel')
        etat = request.POST.get('txt_etat')
        profil = request.POST.get('txt_profil')
        if len(nom) == 0 or len(prenom) == 0 or len(telephone) == 0 or len(etat) == 0 or len(profil) == 0:
            messages.info(request,"Attention, vous n'avez pas mis la nouvelle valeur !!")
            return redirect("util_url")
        else:
            
            uti = Utilisateur.objects.get(pk = id_util)
            print(telephone,"----",etat)
            uti.nom_uti = nom
            uti.prenom_uti = prenom
            uti.num_id_uti = identifiant
            uti.profil = profil
            u = uti.user
            u.is_active = etat
            u.username = telephone
            uti.save()
            u.save()
            messages.info(request, "La modification est reussie avec succes !")
            return redirect("util_url")

'''def chercher_utilisateur(request):
    if request.method == 'GET':
        numero = request.GET.get('cherch_util').strip()
        if len(numero) == 0:
            messages.info(request, "Saisissez le numero de l'utilisateur à chercher svp !")
            return redirect('util_url')
        else:
            liste = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'num_id_uti','user__username', 'profil', 'user__is_active').filter(user__username=numero)
            nbr = liste.count()
            if nbr == 0:
                utilisateurs = Utilisateur.objects.values('id', 'nom_uti', 'prenom_uti', 'num_id_uti','user__username', 'profil', 'user__is_active').order_by("id")
                type_msg = "error"
                messages.info(request, "L'utilisateur n'existe pas dans le system ou bien verifier le numero !")
                return render(request,"utilisateur.html",{'utilisateurs':utilisateurs,'type_msg':type_msg})
            else:
                return render(request, "utilisateur.html",{'utilisateurs':liste})'''

#change_pwd
def afficher_change_pwd(request):
    user = Utilisateur.objects.values('nom_uti','prenom_uti').get(user__username=request.user.username)
    return render(request,"change_password.html",locals())

def change_pwd(request):
    if request.method == 'POST':
        num = request.POST.get('txt_num')
        anc_pass = request.POST.get('txt_pswd_anc')
        nouv_pass = request.POST.get('txt_pswd')
        confirm = request.POST.get('txt_pswd_anc_conf')
        if len(num) == 0 or len(anc_pass) == 0 or len(nouv_pass) == 0 or len(confirm) == 0:
            type_msg = "error"
            messages.info(request, "Completez tous les informations svp !")
            return render(request,"change_password.html",{'type_msg':type_msg})
        else:
            if nouv_pass != confirm:
                type_msg = "error"
                messages.info(request, "Echec,nouveau mot de passe et sa confirmation ne sont pas identifque !")
                return render(request,"change_password.html",{'type_msg':type_msg})
            else:
                user= User.objects.get(username=num)
                passwd_exist = user.check_password(anc_pass)
                if user and passwd_exist:
                    user.set_password(nouv_pass)
                    user.save()
                    messages.info(request, "Ok, maintenant vous avez le nouveau mode passe !")
                    return render(request,"change_password.html")
                else:
                    type_msg = "error"
                    messages.info(request, "Echec,le numero ou le mot de passe n'existe pas ou vous êtes bloqué !")
                    return render(request,"change_password.html",{'type_msg':type_msg})


                