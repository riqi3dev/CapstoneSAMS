JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "SAMS Administrator",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Admin",

    "theme": "minty",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "SAMS Adminstration",

    # # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "images/sams_app_logo_circle1.png",

     # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "images/sams_icon.png",

    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "images/sams_horizontal1.png", 
 
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": ["api.health_record"],

    # Welcome text on the login screen
    "welcome_sign": "Welcome to SAMS Dashboard",

    # Copyright on the footer
    "copyright": "Team GPT 3",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string 
    # "search_model": ["auth.User", "auth.Group"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # Links to put along the top menu
    "topmenu_links": [

        # Url that gets reversed (Permissions can be added)
        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},
        # {"name": "ssssss",  "url": "admin:index", "permissions": ["auth.view_user"]},

        # external url that opens in a new window (Permissions can be added)
        {"name": "Support", "url": "https://github.com/riqi3/CapstoneSAMS/issues", "new_window": True},

        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},

        # # App with dropdown menu to all its models pages (Permissions checked against models)
        # {"app": "books"},
    ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [ 
        {"name": "Support", "url": "https://github.com/riqi3/CapstoneSAMS/issues", "new_window": True},
        {"model": "auth.user"}
    ],

    #############
    # Side Menu #
    #############
 

    "custom_css": "/css/styles.css",

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True, 

    "icons": {
        "api.health_record": "fa fa-file-medical",
        "api.labresult": "fa fa-flask", 
        "api.medicine": "fas fa-pills",
        "api.patient": "fas fa-bed",
        "api.prescription": "fa fa-file-prescription",
        "api.healthsymptom": "fa fa-head-side-cough",
        "user.account": "fa fa-user",
        "user.data_log": "fa fa-hourglass-half",
        # "auth.Group": "fas fa-users",
    },
}


