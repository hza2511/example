from django.urls import path

# from api.management.working_schedule.views import (
#     ListWorkingDayView, RetrieveUpdateWorkingDayView,
#     CreateListWorkingHoursView, RetrieveUpdateDeleteWorkingHoursView,
#     ListWorkingDayWorkingHoursView
# )
from api.management.venue.views import (
    ListCreateAreaView, RetrieveUpdateDeleteAreaView,
    ListCreateTableView, RetrieveUpdateDeleteTableView,
    ListAreaTablesView
)


urlpatterns = [
    path('areas/', ListCreateAreaView.as_view(), name='list_create_areas'),
    path('areas/<int:pk>/', RetrieveUpdateDeleteAreaView.as_view(), name='retrieve_update_delete_area'),
    path('tables/', ListCreateTableView.as_view(), name='list_create_tables'),
    path('tables/<int:pk>/', RetrieveUpdateDeleteTableView.as_view(), name='retrieve_update_delete_table'),
    path('areas/<int:pk>/tables/', ListAreaTablesView.as_view(), name='list_area_tables'),
]
