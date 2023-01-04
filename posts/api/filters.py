from datetime import (
    date,
    timedelta
)
from rest_framework import filters
from taggit.models import Tag


class IsOwnerPostFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(author=request.user)


class TagFieldFilter(filters.SearchFilter):
    SEARCH_PARAM = 'tag'

    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('tag')
        if param:
            try:
                tag = Tag.objects.get(name__icontains=param)
            except Tag.DoesNotExist:
                return []
            else:
                return queryset.filter(tags__in=[tag])
        return queryset


class DaysFieldFilter(filters.SearchFilter):
    SEARCH_PARAM = 'days'

    def filter_queryset(self, request, queryset, view):
        param = request.query_params.get('days')
        if param:
            end_date = date.today()
            try:
                start_date = end_date - timedelta(days=int(param))
            except (ValueError, TypeError):
                return []
            else:
                return queryset.filter(updated__range=[start_date, end_date])
