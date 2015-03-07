from rest_framework import permissions

class ReadOnly(permissions.BasePermission):
	"""
	Create default read only permissions for all of our APIs
	"""
	def has_permission(self, request, view):
		# if it's in the same permissions, return True, otherwise, false
		return request.method in permissions.SAFE_METHODS