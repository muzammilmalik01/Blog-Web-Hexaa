from rest_framework import permissions


"""
How Permissions are meant to work:

Note: 
- has_permissions -> ListCreateAPIView
- has_object_permissions -> RetrieveUpdateDeleteAPIView
- Header:
    Authorization: Bearer [access token with brackets]

#* Orders:
! NOTE: Order Permissions applied to Order and OrderItem Views
- An authenticated User can create an Order
- An authenticated User can see his Order details
- Only SuperUser / Admin can get the list of Orders
- Only SuperUser / Admin can UPDATE or DELETE an Order

#* Products
! NOTE: Product Permission is applied to all views of Products Category, Colors, Products, Images, Attributes
- Anyone can GET Products Category, Colors, Products, Images, Attributes List and Details
- Admin can POST, PATCH, PUT, DELETE Products Category, Colors, Products, Attributes
- Tested Permissions for Colors. All Permissions were working as intended. Same permssions applied to Product Category, Products, Images, Attributes but not tested, hopefully will work ok :D

"""


class ProductPermissions(permissions.BasePermission):
    # * Tested Working *
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # Anyone can view List
            return True
        else:  # Only Admin or Staff Member can Create
            return request.user.is_superuser or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
        ):  # Anyone can view detailed object
            return True
        else:  # Only Admin or Staff Member can Update or Delete
            return request.user.is_superuser or request.user.is_staff


class OrderPermission(permissions.BasePermission):
    # * Tested Working *
    def has_permission(self, request, view):
        # ! Anyone with an Access Token can place an order for some other person !
        if (
            request.method in permissions.SAFE_METHODS
        ):  # Get List will be granted to SuperUser/ Admin
            return request.user.is_authenticated or request.user.is_superuser
        else:  # POST (Create new Order) by Authenticated User or Admin
            return request.user.is_authenticated or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":  # Only Customer or Admin can GET Details of Order
            return (
                request.user == obj.customer
                or request.user.is_superuser
                or request.user.is_staff
            )
        else:  # Order can only be Update/Deleted by Admin
            return request.user.is_superuser or request.user.is_staff
