import os

os.environ.setdefault(
    "DATABASE_URL", 
    "postgresql://retool:N7dLvtqM1rBw@ep-still-king-a6ehxueb.us-west-2.retooldb.com/retool?sslmode=require"
    )

os.environ.setdefault(
    "SECRET_KEY", 
    "N7dLvtqM1rBw"
    )

# Set DEVELOPMENT to True by default if not already set
os.environ.setdefault("DEVELOPMENT", "True")

os.environ['EMAIL_HOST_USER'] = 'donotreply@lottonero.com'
os.environ['EMAIL_HOST_PASSWORD'] = 'Tru8tD@L0rdn8r0'
os.environ['DEFAULT_FROM_EMAIL'] = 'donotreply@lottonero.com'

os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51PNZDORqKPcp1RrsbRAW3U80hXCOvyDMKYGEqQYRPtIHPsnECtRdfGUqdfbPXvCRNUzd2p9JOTktuqBC06HbBXeI00ZFkWdNvq'
os.environ['STRIPE_PUBLISHABLE_KEY'] = 'pk_test_51PNZDORqKPcp1Rrs1PYOOcfQ64miVJRpB2Iyyg8zse2ZK7h7rmqcqT6Wb6rIFUJhfv9QGcXYuj42eRA2kkLekmb200zB1Rq0N5'

# AI Predictions Pricing Table
os.environ['PREDICTIONS_STRIPE_PRICING_TABLE_ID'] = 'prctbl_1PU5KuRqKPcp1RrsX1yTC5in'
# Statistics Pricing Table
os.environ['STATISTICS_STRIPE_PRICING_TABLE_ID'] = 'prctbl_1PU5XIRqKPcp1RrsUubo7zvk'
# Premium Access Pricing Table
os.environ['PREMIUM_STRIPE_PRICING_TABLE_ID'] = 'prctbl_1PU5cTRqKPcp1RrsznoyI6b6'

os.environ['DJSTRIPE_WEBHOOK_SECRET'] = 'whsec_ZOab0DfROU2AsjVxjoNlHuyYI29mha7e'

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
DEBUG = 'DEVELOPMENT'