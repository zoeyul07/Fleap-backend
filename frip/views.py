import json
import random
import datetime

from django.views       import View
from django.http        import HttpResponse, JsonResponse
from django.utils       import timezone
from django.db.models   import Q, Avg, Count, Sum

from .models            import Frip, Image, SubRegion, FripSubRegion, Detail, Host, Event
from user.models        import Review, UserFrip, Energy, PaymentMethod
from user.utils         import login_check, login_check_frip

def find_location(frip_id):
    if SubRegion.objects.filter(fripsubregion__frip_id=frip_id).count() == 1:
        return SubRegion.objects.filter(fripsubregion__frip_id=frip_id).first().name
    elif  SubRegion.objects.filter(fripsubregion__frip_id=frip_id).count() > 1 :
        location=SubRegion.objects.filter(fripsubregion__frip_id=frip_id).first().name
        return f'{location} 외 {SubRegion.objects.filter(fripsubregion__frip_id=frip_id).count()-1} 지역'
    else :
        return None

class DailyView(View):
    @login_check_frip
    def get(self,request):
        first_category = request.GET.get('fid',None)
        second_category = request.GET.get('sid',None)
        third_category = request.GET.get('tid',None)
        limit = int(request.GET.get('limit',20))
        offset = int(request.GET.get('offset',0))
        tag = request.GET.get('tag',None)
        startdate = str(request.GET.get('startdate',"1920-01-01"))
        enddate = str(request.GET.get('enddate', "2030-01-01"))
        location = request.GET.get('location',None)
        order_by = request.GET.get('order_by',None)
        include = request.GET.getlist('include',None)
        province = request.GET.get('province',None)

        filter_dict={}
        region_filter_dict={}

        if first_category:
            filter_dict['firstcategory'] = first_category
            region_filter_dict['frip__firstcategory'] = first_category
        if second_category:
            filter_dict['secondcategory'] = second_category
            region_filter_dict['frip__secondcategory'] = second_category
        if third_category:
            filter_dict['thirdcategory'] = third_category
            region_filter_dict['frip__thirdcategory'] = third_category
        if tag == 'new':
            filter_dict['created_at__range'] = [timezone.now()-datetime.timedelta(days=60),timezone.now()]
            region_filter_dict['frip__created_at__range'] = [timezone.now()-datetime.timedelta(days=60),timezone.now()]
        if startdate:
            if enddate:
                filter_dict['dateValidTo__date__gte'] = startdate
                region_filter_dict['frip__dateValidFrom__date__gte'] = startdate
        if 'today' in include:
            filter_dict['today'] = True
            region_filter_dict['frip__today'] = True
        if 'superhost' in include:
            filter_dict['host__super_host'] = True
            region_filter_dict['frip__host__super_host'] = True
        if location is not None:
            filter_dict['subregion'] = location
            region_filter_dict['id'] = location
        if province is not None:
            filter_dict['subregion__region_id'] = province
            region_filter_dict['region_id'] = province

        frips=Frip.objects.filter(**filter_dict)

        new_frips=Frip.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=60),created_at__lte=timezone.now())
        is_new=[new_frip.id for new_frip in new_frips]

        if tag == 'new' or order_by == 'latest':
            frips=frips.order_by('-created_at')

        if tag == 'hot' or order_by == 'popular':
            count_dict={}
            for hot_frip in frips:
                count_dict[hot_frip.id]=UserFrip.objects.filter(frip_id=hot_frip.id).count()
            frips=[]
            for key, value in sorted(count_dict.items(), key=lambda item: item[1], reverse=True):
                frips.append(Frip.objects.get(id=key))

        if order_by == 'rate':
            count_dict={}
            for star_frip in frips:
                if  Review.objects.filter(frip_id=star_frip.id).aggregate(Avg('grade__number')).get('grade__number__avg') is not None:
                    count_dict[star_frip.id]=Review.objects.filter(frip_id=star_frip.id).aggregate(Avg('grade__number')).get('grade__number__avg')
                else :
                    count_dict[star_frip.id]=0
            frips=[]
            for key,value in sorted(count_dict.items(), key=lambda item: item[1], reverse=True):
                frips.append(Frip.objects.get(id=key))

        if tag == 'pick':
            random_number= random.randrange(1,6)
            frips=frips.order_by('?')[:random_number]

        if order_by == 'low_price':
            frips=frips.order_by('price')

        if order_by == 'high_price':
            frips=frips.order_by('-price')

        try:
            user_id = request.user.id
        except:
            user_id = None

        frip_list=[
                {
                 "frip_id":frip.id,
                 "catch_phrase":frip.catch_phrase,
                 "title":frip.title,
                 "location":find_location(frip.id),
                 "image":[image.image_url for image in Image.objects.filter(frip_id=frip.id)][0],
                 "price":frip.price,
                 "faked_price":frip.faked_price,
                 "new":True if frip.id in is_new else False,
                 "like":True if UserFrip.objects.filter(user_id=user_id, frip_id=frip.id) else False,
                 "startdate":frip.dateValidFrom,
                 "enddate":frip.dateValidTo,
                 "grade":Review.objects.filter(frip_id=frip.id).aggregate(Avg('grade__number')).get('grade__number__avg'),
                 "total":Frip.objects.filter(**filter_dict).count() if tag =='hot' or order_by == 'popular' or order_by == 'rate' else frips.count()
                 }for frip in frips]

        frip_list=frip_list[offset:limit+offset]

        if tag=='pick':
            return JsonResponse({"data":frip_list},status=200)

        regions=SubRegion.objects.select_related('region').filter(**region_filter_dict).order_by('id')

        find_subregion_frip_dict={}
        find_subregion_frip_list=[]
        for filter_frip_id in frips:
            frip_subregion=FripSubRegion.objects.filter(frip_id=filter_frip_id)
            for count_subregion in frip_subregion:
                find_subregion_frip_list.append(count_subregion.sub_region.id)
        for subregion_count_dict in find_subregion_frip_list:
            find_subregion_frip_dict[subregion_count_dict]=find_subregion_frip_list.count(subregion_count_dict)
        for subregion_count_dict in find_subregion_frip_list:
            find_subregion_frip_dict[subregion_count_dict]=find_subregion_frip_list.count(subregion_count_dict)

        find_subregion_region={}
        for i in regions:
            find_subregion_region[i.id]=i.region.id

        region_dict={}
        subregion_dict={}
        for city in regions:
            region_dict[city.region.id]=city.region.name
            subregion_dict[city.id]=city.name

        total_list=[]
        for region in region_dict.keys():
            for subregion in subregion_dict.keys():
                if find_subregion_region[subregion]==region:
                    total_list.append(find_subregion_frip_dict[subregion])

        sub_region_list=[
            {"id":region,
             "name":region_dict[region],
             "sub_region_date":
            [{"id":subregion,
              "name":subregion_dict[subregion],
              "total":find_subregion_frip_dict[subregion],
              "total_count" :sum(total_list)}
             for subregion in subregion_dict.keys() if find_subregion_region[subregion]==region]}
            for region in region_dict.keys()]

        return JsonResponse({"region_data":sub_region_list,"data":frip_list},status=200)
