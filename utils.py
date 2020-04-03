import tomd
import re

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def html2md(html) -> str:
    r_html = tomd.Tomd(html).markdown
    r_html = re.sub('<a.*?></a>', "", r_html)
    r_html = re.sub('<br>', "\n", r_html)
    html = r_html if r_html else html
    return html
