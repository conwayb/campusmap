import os
import site
import sys

root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
major, minor = sys.version_info[:2]
env_site_packages_path = os.path.join(
    root, '.env/lib/python{major}.{minor}/site-packages'.format(**locals()))

assert os.path.exists(env_site_packages_path), \
    'No site-packages found at {0}'.format(env_site_packages_path)

# Add the virtualenv's site-packages to sys.path, ensuring its packages
# take precedence over system packages (by moving them to the front of
# sys.path after they're added).
old_sys_path = list(sys.path)
site.addsitedir(env_site_packages_path)
new_sys_path = [item for item in sys.path if item not in old_sys_path]
sys.path = new_sys_path + old_sys_path

os.environ.setdefault('LOCAL_SETTINGS_FILE', os.path.join(root, 'local.cfg'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusmap.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
