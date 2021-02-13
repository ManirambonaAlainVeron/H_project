from django.shortcuts import render

# Create your views here.
def my_index(request):
    return render(request,"base.html")
# provinces
def afficher_province(request):
    provinces = Province.objects.all().order_by("id")
    return render(request,"province.html",locals())

def ajouter_province(request):
    if request.method == "POST":
        nom = request.POST.get("nom_prov")
        if len(nom) == 0:
            message.info(request,"Saisissez le nom du province svp !")
            type_msg = "error"
            return render(request,"province.html",{'type_msg':type_msg})
        else:
            p = Province(nom_pro = nom)
            p.save()
            message.info(request, "Enregistrement reussi avec succes !")
            return redirect("pro_url")

def supprimer_province(request, id_p): 
    Province.objects.get(pk = id_p).delete()
    message.info(request,"La suppresion est reussie avec succes !")
    return redirect("pro_url")

def editer_province(request, id_p):
    provinces = Province.objects.get(pk = id_p)
    return render(request,"province_edit.html",{'provinces':provinces})

def update_province(request, id_p):
    if request.method == "POST":
        nom = request.POST.get("nom_prov")
        if len(nom) == 0:
            message.info(request,"Saisissez le nom du province svp !")
            type_msg = "error"
            return render(request,"province.html",{'type_msg':type_msg})
        else:
            p = Province.objects.get(pk = id_p)
            p.nom_pro = request.POST.get("nom_prov")
            p.save()
            message.info(request,"La modification est reussie avec succes !")
            return redirect("pro_url")

#commune
def afficher_commune(request):
    communes = Commune.objects.all().order_by("id_com")
    provinces = Province.objects.all().order_by("nom_pro")
    return render(request, "commune.html", locals())

def ajouter_commune(request):
    if request.method == "POST":
        pro = request.POST.get("select_pro")
        com = request.POST.get("nom_com")
        if len(pro) == 0:
            message.info(request,"Selectionnez la province svp !")
            type_msg = "error"
            return render(request,"commune.html",{'type_msg':type_msg})
        elif len(com) == 0:
            message.info(request,"Saisissez le nom de la commune svp !")
            type_msg = "error"
            return render(request,"commune.html",{'type_msg':type_msg})
        else:
            c = Commune(nom_pro = Province(pro), nom_com = com)
            c.save()
            message.info(request, "Enregistrement reussi avec succes !")
            return redirect("com_url")

def supprimer_commune((request, id_c): 
    Commune.objects.get(id_com = id_c).delete()
    message.info(request,"La suppresion est reussie avec succes !")
    return redirect("com_url")

def editer_commune((request, id_cm):
    communes = Commune.objects.get(id_com = id_cm)
    id_province = Commune.objects.values("province").get(pk=id_cm)
    nom_province = Province.objects.values("nom_pro").get(pk=id_province)
    return render(request,"commune_edit.html",locals())

def update_commune(request, id_cm):
    if request.method == "POST":
        pro = request.POST.get("select_pro")
        com = request.POST.get("nom_com")
        if len(pro) == 0:
            message.info(request,"Selectionnez la province svp !")
            type_msg = "error"
            return render(request,"commune_edit.html",{'type_msg':type_msg})
        elif len(com) == 0:
            message.info(request,"Saisissez le nom de la commune svp !")
            type_msg = "error"
            return render(request,"commune_edit.html",{'type_msg':type_msg})
        else:
            c = Commune.objects.get(pk = id_cm)
            c.province = request.POST.get("select_pro")
            c.nom_com = request.POST.get("nom_com")
            c.save()
            message.info(request,"La modification est reussie avec succes !")
            return redirect("com_url")

def chercher_commune(request):
    if request.method == 'GET':
        nom = request.GET.get('cherch_com')
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom de la commune à chercher svp !")
            return redirect('com_url')
        else:
            liste = Commune.objects.values('id','province__nom_pro','nom_com').filter(nom_com=nom)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "La commune n'existe pas dans le system ou verifier l'orthographe svp !")
                return redirect('com_url')
            else:
                return render(request, "commune.html",{'communes':liste})

#colline
def afficher_colline(request):
    provinces = Province.objects.all().order_by("nom_pro")
    communes = Commune.objects.all().order_by("id_com")
    collines = Colline.objects.values('id','province__nom_province','commune__nom_com','nom_col').order_by("id")
    return render(request, "colline.html", locals())

def ajouter_colline((request):
    if request.method == "POST":
        pro = request.POST.get("select_pro")
        com = request.POST.get("select_com")
        col = request.POST.get("nom_col")
        if len(pro) == 0:
            message.info(request,"Selectionnez la province svp !")
            type_msg = "error"
            return render(request,"colline.html",{'type_msg':type_msg})
        elif len(com) == 0:
            message.info(request,"Saisissez le nom de la commune svp !")
            type_msg = "error"
            return render(request,"colline.html",{'type_msg':type_msg})
        elif len(col) == 0:
            message.info(request,"Saisissez le nom de la colline svp !")
            type_msg = "error"
            return render(request,"colline.html",{'type_msg':type_msg})
        else:
            co = Colline(nom_pro = Province(pro),Commune(com), nom_col = col)
            co.save()
            message.info(request, "Enregistrement reussi avec succes !")
            return redirect("col_url")

def supprimer_colline((request, id_co): 
    Colline.objects.get(pk = id_co).delete()
    message.info(request,"La suppresion est reussie avec succes !")
    return redirect("col_url")

def editer_colline(request, id_co):
    collines = Colline.objects.get(pk = id_co)
    id_province = Colline.objects.values("province").get(pk=id_co)
    nom_province = Province.objects.values("nom_pro").get(pk=id_province)
    id_commune = Colline.objects.values("commune").get(pk=id_co)
    nom_commune = Commune.objects.values("nom_com").get(pk=id_commune)
    return render(request,"colline_edit.html",locals())

def update_colline(request, id_co):
    if request.method == "POST":
        pro = request.POST.get("select_pro")
        com = request.POST.get("select_com")
        col = request.POST.get("nom_col")
        if len(pro) == 0:
            message.info(request,"Selectionnez la province svp !")
            type_msg = "error"
            return render(request,"colline_edit.html",{'type_msg':type_msg})
        elif len(com) == 0:
            message.info(request,"Selectionnez la commune svp !")
            type_msg = "error"
            return render(request,"colline_edit.html",{'type_msg':type_msg})
        else:
            col = Colline.objects.get(pk = id_co)
            col.province = request.POST.get("select_pro")
            col.commune = request.POST.get("select_com")
            col.nom_col = request.POST.get("nom_col")
            col.save()
            message.info(request,"La modification est reussie avec succes !")
            return redirect("col_url")

def chercher_colline(request):
    if request.method == 'GET':
        nom = request.GET.get('cherch_col')
        if len(nom) == 0:
            messages.info(request, "Saisissez le nom de la colline à chercher svp !")
            return redirect('col_url')
        else:
            liste = Colline.objects.values('id','province__nom_pro','commune__nom_com','nom_col').filter(nom_col=nom)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "La colline n'existe pas dans le system ou verifier l'orthographe svp !")
                return redirect('col_url')
            else:
                return render(request, "colline.html",{'collines':liste})


# categorie
def afficher_categorie(request):
    categorie = Categorie.objects.all().order_by("id")
    return render(request,"categorie.html",locals())

def ajouter_categorie(request):
    if request.method == "POST":
        nom = request.POST.get("nom_cat")
        if len(nom) == 0:
            message.info(request,"Saisissez le nom du categorie svp !")
            type_msg = "error"
            return render(request,"categorie.html",{'type_msg':type_msg})
        else:
            cat = Categorie(nom_cat = nom)
            cat.save()
            message.info(request, "Enregistrement reussi avec succes !")
            return redirect("cat_url")

def supprimer_categorie(request, id_cat): 
    Categorie.objects.get(pk = id_cat).delete()
    message.info(request,"La suppresion est reussie avec succes !")
    return redirect("cat_url")

def editer_categorie(request, id_cat):
    categorie = Categorie.objects.get(pk = id_cat)
    return render(request,"categorie_edit.html",{'categories':categorie})

def update_categorie(request, id_cat):
    if request.method == "POST":
        nom = request.POST.get("nom_cat")
        if len(nom) == 0:
            message.info(request,"Saisissez le nom du categorie svp !")
            type_msg = "error"
            return render(request,"categorie_edit.html",{'type_msg':type_msg})
        else:
            cat = Categorie.objects.get(pk = id_cat)
            cat.nom_cat = request.POST.get("nom_cat")
            cat.save()
            message.info(request,"La modification est reussie avec succes !")
            return redirect("cat_url")


# groupe
def afficher_groupe(request):
    groupe = Groupe.objects.all().order_by("id")
    return render(request,"groupe.html",locals())

def ajouter_groupe(request):
    if request.method == "POST":
        nom = request.POST.get("nom_groupe")
        if len(nom) == 0:
            message.info(request,"Saisissez le nom du groupe svp !")
            type_msg = "error"
            return render(request,"groupe.html",{'type_msg':type_msg})
        else:
            g = Groupe(nom_groupe = nom)
            g.save()
            message.info(request, "Enregistrement reussi avec succes !")
            return redirect("grp_url")

def supprimer_groupe(request, id_g): 
    Groupe.objects.get(pk = id_g).delete()
    message.info(request,"La suppresion est reussie avec succes !")
    return redirect("grp_url")

def editer_groupe(request, id_g):
    groupe = Groupe.objects.get(pk = id_g)
    return render(request,"groupe_edit.html",{'groupes':groupe})

def update_groupe(request, id_g):
    if request.method == "POST":
        nom = request.POST.get("nom_groupe")
        if len(nom) == 0:
            message.info(request,"Saisissez le nom du groupe svp !")
            type_msg = "error"
            return render(request,"groupe_edit.html",{'type_msg':type_msg})
        else:
            g = Groupe.objects.get(pk = id_g)
            g.nom_groupe = request.POST.get("nom_groupe")
            g.save()
            message.info(request,"La modification est reussie avec succes !")
            return redirect("grp_url")


#acteur
def afficher_acteur(request):
    acteurs = Acteur.objects.all().order_by("id")
    return render(request,"acteur.html",locals())

def ajouter_acteur(request):
    if request.method == "POST":
        nom = request.POST.get("nom_act")
        prenom = request.POST.get("prenom_act")
        identite = request.POST.get("num_id")
        tel = request.POST.get("num_tel")
        etat = request.POST.get("etat_act")
        if len(nom) == 0:
            message.info(request,"Saisissez le nom de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur.html",{'type_msg':type_msg})
        elif len(prenom) == 0:
            message.info(request,"Saisissez le prenom de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur.html",{'type_msg':type_msg})
        elif len(tel) == 0:
            message.info(request,"Saisissez le numero de téléphone de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur.html",{'type_msg':type_msg})
        else:
            act = Acteur(nom_act = nom, prenom_act = nom, telephone_act = tel, num_ide_act = identite, etat_act = etat)
            act.save()
            message.info(request, "Enregistrement reussi avec succes !")
            return redirect("act_url")

def supprimer_acteur(request, id_act): 
    Acteur.objects.get(pk = id_act).delete()
    message.info(request,"La suppresion est reussie avec succes !")
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
            message.info(request,"Saisissez le nom de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur_edit.html",{'type_msg':type_msg})
        elif len(prenom) == 0:
            message.info(request,"Saisissez le prenom de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur_edit.html",{'type_msg':type_msg})
        elif len(tel) == 0:
            message.info(request,"Saisissez le numero de téléphone de l'acteur communauteur !")
            type_msg = "error"
            return render(request,"acteur_edit.html",{'type_msg':type_msg})
        else:
            act = Acteur.objects.get(pk = id_act)
            act.nom_act = nom
            act.prenom_act = prenom
            act.telephone_act = tel
            act.num_ide_act = identite
            act.etat_act = etat
            act.save()
            message.info(request,"La modification est reussie avec succes !")
            return redirect("act_url")

def chercher_acteur(request):
    if request.method == 'GET':
        numero = request.GET.get('cherch_act')
        if len(numero) == 0:
            messages.info(request, "Saisissez le numero de l'acteur communauteur à chercher svp !")
            return redirect('act_url')
        else:
            liste = Acteur.objects.values('id','nom_act','prenom_act','num_ide_act','telephone_act','etat_act').filter(telephone_act=numero)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "L'acteur n'existe pas dans le system ou bien verifier les numero !")
                return redirect('act_url')
            else:
                return render(request, "acteur.html",{'acteurs':liste})


#acteur_groupe
def afficher_acteur_groupe(request):
    acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').order_by("nom_act")
    groupes = Groupe.objects.all().order_by("id_com")
    acteur_groupe = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_cat','acteur__telephone_act','groupe__nom_groupe','etat_act_group').order_by("id")
    return render(request, "acteur_groupe.html", locals())

def retirer_acteur_groupe(request,id_actgrp):
    act = Acteur_groupe.objects.values('acteur__nom_act','acteur__prenom_act').get(pk = id_actgrp)
    Acteur_groupe.objects.get(pk = id_actgrp).delete()
    message.info(request,"L'acteur communauteur"+act.acteur__nom_act+" "+act.acteur__prenom_act+" est retiré dans le groupe !")
    return redirect("actgrp_url")

def ajouter_acteur_groupe(request):
        if request.method == "POST":
            acteur = request.POST.get("nom_act")
            groupe = request.POST.get("prenom_act")
            etat = request.POST.get("num_id")
            if len(acteur) == 0:
                message.info(request,"Selectionnez l'acteur !")
                type_msg = "error"
                return render(request,"colline.html",{'type_msg':type_msg})
            elif len(groupe) == 0:
                message.info(request,"Selectionnez le groupe !")
                type_msg = "error"
                return render(request,"colline.html",{'type_msg':type_msg})
            else:
                act = Acteur(nom_act = nom, prenom_act = nom, telephone_act = tel, num_ide_act = identite, etat_act = etat)
                act.save()
                message.info(request, "Enregistrement reussi avec succes !")
                return redirect("act_url")

def chercher_acteur_groupe_num(request):
    if request.method == 'GET':
        num = request.GET.get('cherch_actgrp')
        if len(numero) == 0:
            messages.info(request, "Saisissez le numero de l'acteur communauteur à chercher svp !")
            return redirect('actgrp_url')
        else:
            liste = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_cat','acteur__telephone_act','groupe__nom_groupe','etat_act_group').filter(acteur__telephone_act=numero)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "L'acteur appartient à aucun groupe !")
                return redirect('act_actgrp_url')
            else:
                return render(request, "acteur_groupe.html",{'acteur_groupe':liste})


def chercher_acteur_groupe_grp(request):
    if request.method == 'GET':
        grp = request.GET.get('cherch_grpact')
        if len(grp) == 0:
            messages.info(request, "Saisissez le nom du groupe à chercher svp !")
            return redirect('actgrp_url')
        else:
            liste = Acteur_groupe.objects.values('id','acteur__nom_act','acteur__prenom_cat','acteur__telephone_act','groupe__nom_groupe','etat_act_group').filter(groupe__nom_groupe=numero)
            nbr = liste.count()
            if nbr == 0:
                type_msg = "error"
                messages.info(request, "Le groupe a aucun acteur !")
                return redirect('act_actgrp_url')
            else:
                return render(request, "acteur_groupe.html",{'acteur_groupe':liste})


def editer_acteur_groupe(request, id_actgrp):
    acteurs = Acteur.objects.values('id','nom_act','prenom_act','telephone_act').order_by("nom_act")
    acteur_select = Acteur_groupe.objects.values('id','acteur','acteur__nom_act','acteur__prenom_act','acteur__telephone_act').get(pk=id_actgrp)
    groupes = Groupe.objects.all().order_by("id_com")
    groupe_select = Acteur_groupe.objects.value('groupe','groupe__nom_groupe').get(pk=id_actgrp)
    etat = Acteur_groupe.objects.values("etat_act_group").get(pk=id_actgrp)
    return render(request,"acteur_groupe_edit.html",locals())

def update_acteur_groupe(request, id_actgrp)
    if request.method == "POST":
        act = request.POST.get("nom_groupe")
        grp = request.POST.get("nom_groupe")
        et = request.POST.get("nom_groupe")
        if len(act) == 0:
            message.info(request,"Selectionnez l'acteur svp !")
            type_msg = "error"
            return render(request,"acteur_groupe_edit.html",{'type_msg':type_msg})
        if len(grp) == 0:
            message.info(request,"Selectionnez le groupe svp !")
            type_msg = "error"
            return render(request,"acteur_groupe_edit.html",{'type_msg':type_msg})
        else:
            act_grp = Acteur_groupe.objects.get(pk = id_actgrp)
            act_grp.acteur = request.POST.get("nom_groupe")
            act_grp.groupe = request.POST.get("nom_groupe")
            act_grp.etat_act_group = request.POST.get("nom_groupe")
            act_grp.save()
            message.info(request,"La modification est reussie avec succes !")
            return redirect("grp_url")
