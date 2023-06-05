import csv 

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from unesco.models import Category, State, Iso, Region, Site


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    Category.objects.all().delete()
    State.objects.all().delete()
    Iso.objects.all().delete()
    Region.objects.all().delete()
    Site.objects.all().delete()
    
    # Format
    # name,description,justification,year,longitude,latitude,area_hectares,category,state,region,iso
    # jane@tsugi.org,I,Python
    # ed@tsugi.org,L,Python

    for row in reader:
        print(row)

        c, created = Category.objects.get_or_create(name=row[7])
        s, created = State.objects.get_or_create(name=row[8])
        i, created = Iso.objects.get_or_create(name=row[10])
        r, created = Region.objects.get_or_create(name=row[9])
        n=row[0]
        y=row[3]
        d=row[1]
        j=row[2]
        lon=row[4]
        lat=row[5]
        a=row[6]
        if row[6] == '':
            a = None
            
        site = Site(name=n, year=y, description=d, justification=j, longitude=lon, latitude=lat,area_hectares=a, category=c, state=s, iso=i, region=r)
        site.save()
