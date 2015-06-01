from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from farmmonitor.settings import *


farm_patterns = patterns('farm.views',
	url(r'^farm/newsample$', 'NewSample'),
	url(r'^farm/testnetwork$', 'TestHttpConnection'),
	url(r'^farm/getdata$', 'GetDataPoints'),
	url(r'^farm/getdetail$', 'GetPointDetail'),
	url(r'^farm/gethistory$', 'GetHistoryData'),
	url(r'^farm/getimpodata$', 'GetImportantData'),
	url(r'^farm/getheatmap$', 'GetHeatMap'),
	url(r'^farm/deletepoints$', 'DeleteFakePoints'),
	# url(r'^farm/reset$', 'ResetPointPosition'),
	# url(r'^farm/newgrid$', 'NewGrid'),
	# url(r'^farm/newmoisture$', 'NewMoisture'),
)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'farmmonitor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT }),
) + farm_patterns
