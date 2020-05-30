import json
import random
import datetime

from django.views      import View
from django.http       import HttpResponse, JsonResponse
from django.db.models  import Count, Avg,  Q, Sum
from django.utils      import timezone

from .models           import Frip, Image, Detail, Host, SubRegion, FripSubRegion, Event
from user.models       import UserFrip, Review, Energy, PaymentMethod
from user.utils        import login_check, login_check_frip


FRIP_REVIEW_LIMIT=1

def find_location(frip_id):
    if SubRegion.objects.filter(fripsubregion__frip_id=frip_id).count() == 1:
        return SubRegion.objects.filter(fripsubregion__frip_id=frip_id).first().name
    elif  SubRegion.objects.filter(fripsubregion__frip_id=frip_id).count() > 1 :
        location=SubRegion.objects.filter(fripsubregion__frip_id=frip_id).first().name
        return f'{location} 외 {SubRegion.objects.filter(fripsubregion__frip_id=frip_id).count()-1} 지역'
    else :
        return None

class DetailView(View):
    def get(self, request, products_id):
        frip =[{
            'image_url':[one.image_url for one in  product.image_set.all()],
            'catch_phrase':product.catch_phrase,
            'title' : product.title,
            'price' : product.price,
            'faked_price' : product.faked_price if product.faked_price else None,
            'discount_percentage' : int(((product.faked_price-product.price)/product.faked_price) * 100) if product.faked_price else None,
            'liked' : product.userfrip_set.aggregate(Count('frip_id')).get('frip_id__count'),
            'duedate' : product.duedate,
            'location' : product.location,
            'review_average': [
                Review.objects.select_related('grade').filter(frip_id=products_id).aggregate(Avg('grade__number')).get('grade__number__avg') if product.host.review_set.all() else None],
            'host':{
                'host_image' :  product.host.image_url,
                'host_name' : product.host.name,
                'description' : product.host.description,
                'super_host' : product.host.super_host
            },
            'review' :[{
                'user_name' : review.user.nickname,
                'grade' : review.grade.number,
                'created_at' : review.created_at,
                'content' : review.content,
                'itinerary': review.itinerary.start_date if review.itinerary else None,
                'option' :review.option.name,
                'child_option': review.child_option.name if review.child_option else None
            } for review in Review.objects.select_related('itinerary','grade','user','option','child_option').filter(host_id=product.host_id) if product.review_set.all()][:FRIP_REVIEW_LIMIT],
            'content' : product.detail.content,
           'include' : product.detail.include,
            'exclude' : product.detail.exclude,
            'schedule': product.detail.schedule,
            'material' : product.detail.material,
            'notice' : product.detail.notice,
            'vennue' : {
                'location' : product.venue,
                'venue_lng' : product.venue_lng,
                'venue_lat' : product.venue_lat
            },
            'gathering_place': {
                'location' : product.gathering_place,
                'geopoint_lng' : product.geopoint_lng,
                'geopoint_lat' : product.geopoint_lat
            },
            'choice' : {
                'itinerary':[{
                    'start_date' : itinerary.start_date,
                    'end_date' :itinerary.end_date,
                    'max_quantity' : itinerary.max_quantity,
                }for itinerary in  product.itinerary_set.all() if product.itinerary_set.all()],
                'option':[{
                    'title' : option.name if product.option_set.filter(option_type=1) else None,
                    'content' : option.name if product.option_set.filter(option_type=0) else None,
                    'max_quantity' : option.max_quantity if option.max_quantity else None,
                    'price' : option.price if option.price else None,
                    'base_price' : option.base_price if option.base_price else None,
                    'option_type' : option.option_type.name
                }for option in product.option_set.all()],
                'child_option' : [{
                    'title' : child.name if product.childoption_set.filter(option_type=1) else None,
                    'content' : child.name if product.childoption_set.filter(option_type=0) else None,
                    'price' : child.price,
                    'base_price' : child.base_price if child.base_price else None,
                    'option_type' : child.option_type.name
                }for child in product.childoption_set.all() if product.childoption_set.all()]
            }
        }for product in Frip.objects.select_related('host', 'detail').prefetch_related('image_set', 'review_set', 'itinerary_set', 'option_set', 'childoption_set').filter(id=products_id)]

        return JsonResponse({'detail':frip}, status=200)

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

class MainView(View):
    @login_check_frip
    def get(self, request):
            FILTER_RULES = {
                "userfrip__user_id" : lambda userfrip__user_id: True if tag == "hotfrip" else False,
                "sale" : lambda sale : True if tag == "sale" else False,
                "host__super_host" : lambda host__super_host: True if tag == "superhost" else False,
                "secondcategory__name" : lambda secondcategory__name: "공예·DIY" if tag == "enjoy" else False,
                "thirdcategory__name" : lambda thirdcategory__name: "서핑" if event == "surfing" else False,
            }

            is_slider = request.GET.get('slider', None)
            limit = int(request.GET.get('limit', 20))
            tag = request.GET.get('tag', None)
            event = request.GET.get('event', None)
            all_event = request.GET.get('all', None)

            if is_slider is not None:
                slider = {
                "firstSlider" : list(Event.objects.values_list('image_url', flat=True))[0:4],
                "secondSlider" : list(Event.objects.values_list('image_url', flat=True))[4:6],
                }
                return JsonResponse({"slider": slider}, status=200)

            if tag == 'newfrip': 
                filter_dict = {}
                filter_dict['created_at__range'] = [timezone.now()-datetime.timedelta(days=60),timezone.now()] 

            for filters, rules in FILTER_RULES.items():
                if rules(filters) == True:
                    filter_dict = {filters : rules(filters)}
                if rules(filters) == [timezone.now()-datetime.timedelta(days=60),timezone.now()]:
                    filter_dict = {filters : rules(filters)}
                if rules(filters) == "공예·DIY":
                    filter_dict = {filters : rules(filters)}
                if rules(filters) == "서핑":
                    filter_dict = {filters : rules(filters)}

            frips = Frip.objects.filter(**filter_dict)

            if tag == "newfrip":
                frips = frips.order_by('-created_at')[:limit]
            if tag == "hotfrip":
                frips = Frip.objects.prefetch_related('userfrip_set').annotate(count=Count('userfrip__id')).order_by('?')[:limit]
            if tag == "superhost":
                frips = frips.order_by('?')[:limit]
            if tag == "enjoy":
                frips = frips.order_by('?')[:limit]
            if event == "서핑":
                frips = frips.order_by('?')[:limit]

            new_frips=Frip.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=60),created_at__lte=timezone.now())
            is_new=[new_frip.id for new_frip in new_frips]

            try:
                user_id = request.user.id
            except:
                user_id = None

            frip_list = [
                    {"frip_id":frip.id,
                    "catch_phrase":frip.catch_phrase,
                    "title":frip.title,
                    "image":[image.image_url for image in Image.objects.filter(frip_id=frip.id)][0],
                    "price":frip.price,
                    "faked_price": frip.faked_price,
                    "new":True if frip.id in is_new else False,
                    "grade": Review.objects.filter(frip_id=frip.id).aggregate(Avg('grade__number')).get('grade__number__avg'),
                    "like":True if UserFrip.objects.filter(user_id=user_id, frip_id=frip.id) else False,
                    "location":find_location(frip.id)
                    } for frip in frips]

            return JsonResponse({"data": frip_list}, status=200)

class SearchView(View):
    def get(self, request):
        keyword = request.GET.get('keyword', None)
        frip_search = Frip.objects.filter(Q(title__icontains=keyword) | Q(detail__content__icontains=keyword)).distinct()

        new_frips=Frip.objects.filter(created_at__gte=timezone.now()-datetime.timedelta(days=60),created_at__lte=timezone.now())
        is_new=[new_frip.id for new_frip in new_frips]

        frip_list = [
                    {"frip_id":frip.id,
                    "catch_phrase":frip.catch_phrase,
                    "title":frip.title,
                    "image":[image.image_url for image in Image.objects.filter(frip_id=frip.id)][0],
                    "price":format(frip.price, ","),
                    "faked_price": frip.faked_price,
                    "new":True if frip.id in is_new else False,
                    "grade": Review.objects.filter(frip_id=frip.id).aggregate(Avg('grade__number')).get('grade__number__avg'),
                    "like":True if UserFrip.objects.filter(user_id=user_id, frip_id=frip.id) else False,
                    "location":find_location(frip.id)
                    } for frip in frip_search]

        return JsonResponse({"data": frip_list}, status=200)