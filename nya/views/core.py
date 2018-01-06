from flask import render_template
from ..cache import CachedBlueprint


bl = CachedBlueprint('core', __name__)


@bl.route('/')
def index():
    return render_template('core/index.html')
