from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


farm_patterns = patterns('farm.views',
	url(r'^farm/newgrid$', 'NewGrid'),
	url(r'^farm/newmoisture$', 'NewMoisture'),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'farmmonitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
) + farm_patterns
