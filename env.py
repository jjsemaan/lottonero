import os

os.environ.setdefault(
    "DATABASE_URL", 
    "postgresql://retool:5Pq4KfdgJQSI@ep-frosty-dew-a65kykh4.us-west-2.retooldb.com/retool?sslmode=require"
    )

os.environ.setdefault(
    "SECRET_KEY", 
    "(%yncfp82@n31)fys7fm!5!c6tv&kktngz8"
    )

os.environ['DEVELOPMENT'] = 'False'  # or 'False' based on your development status

os.environ['EMAIL_HOST_USER'] = 'donotreply@lottonero.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'Tru8tD@L0rdn8r0'
os.environ['DEFAULT_FROM_EMAIL'] = 'donotreply@lottonero.com'

os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51PNZDORqKPcp1RrsbRAW3U80hXCOvyDMKYGEqQYRPtIHPsnECtRdfGUqdfbPXvCRNUzd2p9JOTktuqBC06HbBXeI00ZFkWdNvq'
os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_51PNZDORqKPcp1Rrs1PYOOcfQ64miVJRpB2Iyyg8zse2ZK7h7rmqcqT6Wb6rIFUJhfv9QGcXYuj42eRA2kkLekmb200zB1Rq0N5'
os.environ['STRIPE_ENDPOINT_SECRET'] = 'whsec_806185019179ae9ac048b43f0664eb483da13d09ea3b5809d528af1008df8a4f'

os.environ['CLOUDINARY_CLOUD_NAME'] = 'dmebot5lf'
os.environ['CLOUDINARY_API_KEY'] = '765648534614641'
os.environ['CLOUDINARY_API_SECRET'] = '5tV3bz9vw519L3eV2b0IBw9lk6M'

os.environ['GOOGLE_CLIENT_ID'] = 'your_google_client_id'
os.environ['GOOGLE_CLIENT_SECRET'] = 'your_google_client_secret'

os.environ['FACEBOOK_APP_ID'] = 'your_facebook_app_id'
os.environ['FACEBOOK_APP_SECRET'] = 'your_facebook_app_secret'

os.environ['JAZZMIN_SITE_TITLE'] = 'Lottonero'
os.environ['JAZZMIN_SITE_HEADER'] = 'Lottonero Admin'

# Automate the DEBUG setting
os.environ['DEBUG'] = str(os.environ.get('DEVELOPMENT') == 'True')

# You can add more environment variables here as needed
