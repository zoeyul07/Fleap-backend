import os
import django
import csv
import sys

os.chdir(".")
print("Current dir=", end=""), print(os.getcwd())

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("BASE_DIR=", end=""), print(BASE_DIR)

sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fleap.settings")
django.setup()

from frip.models import *
from user.models import *

# account
CSV_PATH = './csv/account.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Account.objects.create(
            name  = row['name'],
        )

# user
CSV_PATH = './csv/user.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        User.objects.create(
            email = row['email'],
            nickname = row['nickname'],
            password = row['password'],
            phone_number = row['phone_number'],
            coupon = row['coupon'],
            account = Account.objects.get(id=row['account_id']),
            created_at = row['created_at']
        )

# interest
CSV_PATH = './csv/interest.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Interest.objects.create(
            name = row['name'],
        )

# interest_detail
CSV_PATH = './csv/interestdetail.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        InterestDetail.objects.create(
            name = row['name'],
            interest = Interest.objects.get(id=row['interest_id'])
        )

# host
CSV_PATH = './csv/host.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Host.objects.create(
            name = row['name'],
            image_url = row['image_url'],
            description = row['description'],
            super_host = row['super_host']
        )

# user_host
CSV_PATH = './csv/userhost.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        UserHost.objects.create(
            host = Host.objects.get(id= row['host_id']),
            user = User.objects.get(id=row['user_id'])
        )

# detail
CSV_PATH = './csv/detail.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Detail.objects.create(
            content = row['content'],
            include = row['include'],
            exclude = row['exclude'],
            schedule = row['schedule'],
            material = row['material'],
            notice = row['notice']
        )

# frip
CSV_PATH = './csv/frip.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Frip.objects.create(
            title = row['title'],
            catch_phrase = row['catchphrase'],
            price = row['price'],
            faked_price = None if row['fakedprice'] == '' else row['fakedprice'],
            duedate = None if row['duedate'] == '' else row['duedate'],
            location = row['location'],
            venue = row['venue'],
            venue_lng = row['venue_lng'],
            venue_lat = row['venue_lat'],
            gathering_place = row['gather'],
            geopoint_lng = row['geo_lng'],
            geopoint_lat = row['geo_lat'],
            today = row['today'],
            ticket = row['ticket'],
            sale = row['sale'],
            dateValidFrom = row['datevalidfrom'],
            dateValidTo = row['datevalidto'],
            created_at = row['created_at'],
            updated_at = row['updated_at'],
            host = None if row['host_id'] == '' else Host.objects.get(id=row['host_id']),
            detail = None if row['detail_id'] == '' else Detail.objects.get(id=row['detail_id'])
        )

# image
CSV_PATH = './csv/image.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Image.objects.create(
            image_url  = row['image_url'],
            frip = Frip.objects.get(id=row['frip_id'])
        )

# user_frip
CSV_PATH = './csv/userfrip.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        UserFrip.objects.create(
            frip = Frip.objects.get(id=row['frip_id']),
            user = User.objects.get(id=row['user_id'])
        )

# grade
CSV_PATH = './csv/grade.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Grade.objects.create(
            number = row['number'],
        )

# maintab
CSV_PATH = './csv/maintab.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        MainTab.objects.create(
            name = row['name'],
        )

# itinerary
CSV_PATH = './csv/itinerary.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Itinerary.objects.create(
            start_date = row['start_date'],
            end_date = row['end_date'],
            max_quantity = row['max_quantity'],
            frip = Frip.objects.get(id=row['frip_id']),
        )

# option_type
CSV_PATH = './csv/optiontype.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        OptionType.objects.create(
            name = row['name']
        )

# option
CSV_PATH = './csv/option.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Option.objects.create(
            name = row['name'],
            price = None if row['price'] == '' else row['price'],
            base_price = None if row['base_price'] == '' else row['base_price'],
            max_quantity = row['max_quantity'],
            frip = Frip.objects.get(id=row['frip_id']),
            option_type = OptionType.objects.get(id=row['option_type']),
        )

# itinerary_option
CSV_PATH = './csv/itineraryoption.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        ItineraryOption.objects.create(
            itinerary = Itinerary.objects.get(id=row['Itinerary_id']),
            option = Option.objects.get(id=row['option_id'])
        )

# child_option
CSV_PATH = './csv/childoption.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        ChildOption.objects.create(
            name = row['name'],
            price = None if row['price'] == '' else  row['price'],
            base_price = None if row['base_price'] == '' else row['base_price'],
            frip = Frip.objects.get(id=row['frip_id']),
            option_type = OptionType.objects.get(id=row['option_type']),
        )

# option_childoption
CSV_PATH = './csv/optionchildoption.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        OptionChildOption.objects.create(
            option = Option.objects.get(id=row['option_id']),
            child_option = ChildOption.objects.get(id=row['child_option_id']),
        )

# review
CSV_PATH = './csv/review.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Review.objects.create(
            user = User.objects.get(id=row['user']),
            frip = Frip.objects.get(id=row['frip']),
            host = Host.objects.get(id=row['host']),
            itinerary = None if row['itinerary'] == '' else Itinerary.objects.get(id=row['itinerary']),
            option = Option.objects.get(id=row['option']),
            child_option = None if row['child_option'] == '' else ChildOption.objects.get(id=row['child_option']),
            grade = Grade.objects.get(id=row['grade']),
            content = row['content'],
            created_at = row['created_at']
        )

# payment_method
CSV_PATH = './csv/payment_method.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        PaymentMethod.objects.create(
            name = row['name'],
        )

# status
CSV_PATH = './csv/status.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Status.objects.create(
            name = row['name'],
        )

 ## purchase
 #CSV_PATH = './csv/purchase.csv'
 #
 #with open(CSV_PATH, newline='') as csvfile:
 #    data_reader = csv.DictReader(csvfile)
 #
 #    for row in data_reader:
 #        Purchase.objects.create(
 #            user = User.objects.get(id=row['users_id']),
 #            frip = Frip.objects.get(id=row['frips_id']),
 #            Itinerary = Itinerary.objects.get(id=row['itineraries_id']),
 #            option = OptionType.objects.get(id=row['options_id']),
 #            child_option = ChildOption.objects.get(id=row['child_options_id']),
 #            energy = Energy.objects.get(id=row['energies_id']),
 #            payment_method = PaymentMethod.objects.get(id=row['payment_method']),
 #            review = Review.objects.get(id=row['reviews_id']),
 #            status = Status.objects.get(id=row['status_id']),
 #            quantity = row['quantity'],
 #            created_at = row['created_at']
 #        )
 #
# first_category
CSV_PATH = './csv/firstcategory.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        FirstCategory.objects.create(
            name = row['name'],
            main_tab = MainTab.objects.get(id=row['main_tab_id']),
        )

# second_category
CSV_PATH = './csv/secondcategory.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        SecondCategory.objects.create(
            name = row['name'],
            first_category = FirstCategory.objects.get(id=row['first_category_id'])
        )

# third_category
CSV_PATH = './csv/thirdcategory.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        ThirdCategory.objects.create(
            name = row['name'],
            second_category = SecondCategory.objects.get(id=row['second_category_id']),
        )

# fourth_category
CSV_PATH = './csv/fourthcategory.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        FourthCategory.objects.create(
            name = row['name'],
            third_category = ThirdCategory.objects.get(id=row['third_category_id']),
        )

# event
CSV_PATH = './csv/event.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Event.objects.create(
            image_url = row['image_url'],
        )

# frip_event
CSV_PATH = './csv/fripevent.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        FripEvent.objects.create(
            frip = Frip.objects.get(id=row['frip_id']),
            event = Event.objects.get(id=row['event_id'])
        )

# theme
CSV_PATH = './csv/theme.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Theme.objects.create(
            name = row['name'],
        )

# frip_theme
CSV_PATH = './csv/friptheme.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        FripTheme.objects.create(
            frip = Frip.objects.get(id=row['frip_id']),
            theme = Theme.objects.get(id=row['theme_id'])
        )

# region
CSV_PATH = './csv/region.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        Region.objects.create(
            name = row['name']
        )

# subregion
CSV_PATH = './csv/subregion.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        SubRegion.objects.create(
            name = row['name'],
            region = Region.objects.get(id=row['region_id']),
        )

# frip_subregion
CSV_PATH = './csv/fripsubregion.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        FripSubRegion.objects.create(
            frip = Frip.objects.get(id=row['frip_id']),
            sub_region = SubRegion.objects.get(id=row['sub_region_id']),
        )

# frip_category
CSV_PATH = './csv/fripcategory.csv'

with open(CSV_PATH, newline='') as csvfile:
    data_reader = csv.DictReader(csvfile)

    for row in data_reader:
        FripCategory.objects.create(
            frip= Frip.objects.get(id=row['frip_id']),
            first_category = FirstCategory.objects.get(id=row['first_category_id']),
            second_category = SecondCategory.objects.get(id=row['second_category_id']),
            third_category = ThirdCategory.objects.get(id=row['third_category_id']),
            fourth_category = None if row['fourth_category_id'] == '' else FourthCategory.get(id=row['fourth_category_id'])
        )
