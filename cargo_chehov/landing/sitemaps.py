from django.http import HttpResponse
from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.template.loader import render_to_string


class MySitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0
    lastmod = timezone.now().strftime("%Y-%m-%d")

    def item(self):
        return "https://cargo-chehov.ru/"



def generate_sitemap(request):
    sitemap = MySitemap()

    xml = render_to_string('sitemap.xml', {'urlset': sitemap})
    return HttpResponse(xml, content_type="application/xml")
