import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webh2.settings")
import django
django.setup()

import json
from webh2.wsgi import *
from main.models import *

# Create your models here.

with open('./data/infor_member.json', 'r', encoding='utf-8') as f:
    members = json.load(f)
    for user in members:
        # if user["role"] != "member":
        user = ModAdmin.objects.create_user( 
            username =user["user_name"],
            password = user["mssv"],
            full_name = user["full_name"],
            describe = user["describe"],
            role = user["role"],
            email = user["email"],
            mssv = user["mssv"],
            class_school = user["class_school"],
            image = user["image"],
            is_staff = True if user["role"] != "member" else False,
            is_active = True if user["role"] != "member" else False,
            is_superuser = False,  
        )
        
superuser = ModAdmin.objects.create_superuser(username="admin", email="admin@gmail.com", password="admin", full_name="admin", describe="admin", role="member", mssv="admin", class_school="admin", image="https://avatars.githubusercontent.com/u/83393197?v=4", is_staff=True, is_active=True, is_superuser=True)


with open('./data/paper.json', 'r', encoding='utf-8') as f:
    infor_papers = json.load(f)
    admin = ModAdmin.objects.get(is_superuser=True)
    for i in infor_papers:
        s = Paper(
            # id_paper = i["id_paper"],
            title = i["title"],
            author = i["author"],
            abstract = i["abstract"],
            link_paper = i["link_paper"],
            # link_github = i["link_github"],
            institute = i["institute"],
            interest = i["interest"],
            id_user = admin,
            year = i["year"],
        )
        s.save()











