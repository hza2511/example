from django.urls import path

from api.management.working_schedule.views import (
    # ListWorkingDayView,
    # RetrieveUpdateWorkingDayView,
    # CreateListWorkingHoursView,
    RetrieveUpdateDeleteWorkingHoursView,
    # ListWorkingDayWorkingHoursView,
    BulkListWorkingDayView,
    BulkCreateListWorkingHoursView
)

urlpatterns = [
    # path('working_days/', ListWorkingDayView.as_view(), name='list_working_days'),
    # BULK
    path('working_days/', BulkListWorkingDayView.as_view(), name='bulk_list_update_working_days'),
    # path('working_days/<int:pk>/', RetrieveUpdateWorkingDayView.as_view(), name='retrieve_update_working_day'),
    # path('working_days/<int:pk>/working_hours/',
    #      ListWorkingDayWorkingHoursView.as_view(), name='list_working_day_working_hours'),
    # path('working_hours/', CreateListWorkingHoursView.as_view(), name='create_list_working_hours'),
    # BULK
    path('working_hours/', BulkCreateListWorkingHoursView.as_view(), name='bulk_create_list_working_hours'),
    path('working_hours/<int:pk>/', RetrieveUpdateDeleteWorkingHoursView.as_view(),
         name='delete_working_hour'),
         # name='retrieve_update_delete_working_hours'),
]
