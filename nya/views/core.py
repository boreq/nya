from flask import render_template
from ..cache import CachedBlueprint
from .api import get_stats


bl = CachedBlueprint('core', __name__)


@bl.route('/')
def index():
    return render_template('core/index.html')


@bl.route('/stats')
def stats():
    data = get_stats()

    stats = []
    for key, value in data.items():
        name = key.replace('_', ' ')
        name = name.capitalize()
        stats.append(name + ' ' + str(value))
    if (len(stats) == 0):
        stats.append('No stats are available')

    return render_template('core/stats.html', stats=stats)
