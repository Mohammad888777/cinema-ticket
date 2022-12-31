from .models import Movie,Seat
from django.db.models.signals import post_save,post_delete


def autoCreate(sender,instance,created,**kwargs):

    
    # for i in range(1,49):
    #     Seat.objects.create(
    #     movie=instance,number=i,day=d
    #     )

    moviesDay=instance.days.all()
    print(instance.name)
    print()
    print(moviesDay,"$$$$$$$$$$$$$$$$$$$$$$$$$######################")
    sat=None
    sun=None
    mon=None
    tues=None
    wed=None
    thurs=None
    fri=None

    for d in moviesDay:

        if d.day_week=="Saturday":
            sat=True

        if d.day_week=="Sunday":
            sun=True
        
        if d.day_week=="Monday":
            mon=True

        if d.day_week=="Tuesday":
            tues=True

        
        if d.day_week=="Wednesday":
            wed=True
        
        if d.day_week=="Thursdays":
            thurs=True
        
        if d.day_week=="Friday":
            fri=True
    print(sat)
    print(sun)
    print(mon)
    print(tues)
    print(wed)
    print(thurs)
    print(fri)
    # print(list(filter(lambda d:d.day_week=="Wednesday",moviesDay))[0])

    if sat:
        for i in range(1,49):
            Seat.objects.create(
            movie=instance,number=i,day=list(filter(lambda d:d.day_week=="Saturday",moviesDay))[0]
            )
    if sun:
        for i in range(1,49):
            Seat.objects.create(
            movie=instance,number=i,day=list(filter(lambda d:d.day_week=="Sunday",moviesDay))[0]
            )
    
    if mon:
        for i in range(1,49):
            Seat.objects.create(
            movie=instance,number=i,day=list(filter(lambda d:d.day_week=="Monday",moviesDay))[0]
            )
    

    if tues:
        for i in range(1,49):
            Seat.objects.create(
            movie=instance,number=i,day=list(filter(lambda d:d.day_week=="Tuesday",moviesDay))[0]
            )
    
    if wed:
        for i in range(1,49):
            Seat.objects.create(
            movie=instance,number=i,day=list(filter(lambda d:d.day_week=="Wednesday",moviesDay))[0]
            )

    if thurs:
        for i in range(1,49):
            Seat.objects.create(
            movie=instance,number=i,day=list(filter(lambda d:d.day_week=="Thursdays",moviesDay))[0]
            )
        
    
    if fri:
        for i in range(1,49):
            Seat.objects.create(
            movie=instance,number=i,day=list(filter(lambda d:d.day_week=="Friday",moviesDay))[0]
            )
    




post_save.connect(autoCreate,sender=Movie)
