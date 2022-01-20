from django.urls import path

from api.management.modifiers.views import (
    ListCreateModifiersGroupsView, RetrieveUpdateModifiersGroupView,
    ListCreateUpdateModifiersOptionView,
    DeleteModifiersOptionsView, BulkUpdateModifiersOptionsView
)

urlpatterns = [
    path('modifiers_groups/', ListCreateModifiersGroupsView.as_view(), name='list_create_modifiers_groups'),
    path('modifiers_groups/<int:pk>/', RetrieveUpdateModifiersGroupView.as_view(),
         name='retrieve_update_delete_modifiers_group'),
    path('modifiers_options/', ListCreateUpdateModifiersOptionView.as_view(), name='list_create_update_modifiers_options'),
    path('modifiers_options/<int:pk>/', DeleteModifiersOptionsView.as_view(), name='delete_modifiers_options'),
    path('modifiers_options_bulk/', BulkUpdateModifiersOptionsView.as_view(), name='bulk_update_modifiers_options'),
]
