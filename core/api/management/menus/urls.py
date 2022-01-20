from django.urls import path

from api.management.menus.views import (
    CreateListMenusView, RetrieveUpdateDeleteMenuView, ImageMenuView, ListMenuCategoriesView,
    BulkUpdateMenusView
)

urlpatterns = [
    path('menus/', CreateListMenusView.as_view(), name='create_list_menus'),
    path('menus/<int:pk>/', RetrieveUpdateDeleteMenuView.as_view(), name='retrieve_update_menu'),
    path('menus/<int:pk>/categories/', ListMenuCategoriesView.as_view(), name='list_menu_categories'),
    path('menus/<int:pk>/image/', ImageMenuView.as_view(), name='set_delete_menu_image'),
    path('menus_bulk/', BulkUpdateMenusView.as_view(), name='bulk_update_menus'),
]
