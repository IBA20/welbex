from django.urls import path


from .views import (
    ShipmentView,
    ShipmentListView,
    ShipmentCreateView,
    CarView,
    ShipmentDetailsView,
)


app_name = "cargo"

urlpatterns = [
    path('shipment/<int:pk>', ShipmentView.as_view()),
    path('shipment/details/<int:pk>', ShipmentDetailsView.as_view()),
    path('shipment/', ShipmentCreateView.as_view()),
    path('shipments/', ShipmentListView.as_view()),
    path('car/<int:pk>', CarView.as_view()),
]
