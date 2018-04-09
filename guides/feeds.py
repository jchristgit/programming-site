from django.contrib.syndication.views import Feed
from django.shortcuts import reverse
from django.urls import reverse_lazy
from django.utils.feedgenerator import Atom1Feed

from .models import Guide


class LatestGuidesRSSFeed(Feed):
    title = "Latest Programming Guides"
    description = "Newest programming guides created by our Members."
    link = reverse_lazy('guides:feed_rss')

    def items(self):
        return Guide.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.overview

    def item_link(self, item):
        return reverse('guides:detail', kwargs={'pk': item.id})

    def item_pubdate(self, item):
        return item.pub_datetime

    def item_updateddate(self, item):
        return item.edit_datetime

    def item_author_name(self, item):
        return item.author.first_name

    def item_author_link(self, item):
        return reverse('home:profile', kwargs={'pk': item.author.id})


class LatestGuidesAtomFeed(LatestGuidesRSSFeed):
    feed_type = Atom1Feed
    subtitle = LatestGuidesRSSFeed.description
    link = reverse_lazy('guides:feed_atom')
