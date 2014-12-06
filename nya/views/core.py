from flask import render_template
from ..cache import CachedBlueprint
from ..views.api import get_stats
from ..helpers import hr_size


bl = CachedBlueprint('core', __name__)


def index():
    return render_template('core/index.html')


def stats():
    data = get_stats()
    stats = [
        'Total files %d' % data['total_files'],
        'Total size %s' % hr_size(data['total_size'])
    ]
    return render_template('core/stats.html', stats=stats)


bl.add_url_rule('/', view_func=index)
bl.add_url_rule('/stats', view_func=stats)
