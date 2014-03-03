import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listing.settings")
from core.models import Site



def main():
    print "script working"
    if len(sys.argv) < 2:
        sys.exit("Must provide an option")
    else:
        if sys.argv[1] == 'csv':
            save_csv(sys.argv[2])
        elif sys.argv[1] == 'reinstall-csv':
            delete_feeds()
            save_csv(sys.argv[2])
        elif sys.argv[1] == 'trends':
            save_trend()
        elif sys.argv[1] == 'clean-posts':
            clean_posts()
        elif sys.argv[1] == 'reduce':
            reduce_posts()
        else:
            sys.exit("Invalid option")
