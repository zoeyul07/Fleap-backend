from django.views import View
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Avg

from .models import Frip, Image, Detail, Host
from user.models import UserFrip, Review

FRIP_REVIEW_LIMIT=1

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

