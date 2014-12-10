from flask import render_template
from ..cache import CachedBlueprint
from ..views.api import get_stats
from ..helpers import hr_size


bl = CachedBlueprint('core', __name__)


@bl.route('/')
def index():
    return render_template('core/index.html')


@bl.route('/stats')
def stats():
    stats = get_stats()
    stats = [
        'Total files %d' % stats['total_files'],
        'Total size %s' % hr_size(stats['total_size'])
    ]
    return render_template('core/stats.html', stats=stats)
