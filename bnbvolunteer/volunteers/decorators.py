from bnbvolunteer import settings
from django.http import Http404
from django.http.response import HttpResponseRedirect
from re import search

"""
If HTTPS_REDIRECT is enabled, redirect an insecure page to its secure counterpart.
"""
def redirect_to_https(viewFunction):
    def _redirect_to_https(request, *args, **kwargs):
        if search("http://", request.build_absolute_uri(request.get_full_path())):
            if getattr(settings, "HTTPS_REDIRECT", False):
                redirect = request.build_absolute_uri(request.get_full_path()).replace("http://", "https://")
                return HttpResponseRedirect(redirect)
        return viewFunction(request, *args, **kwargs)
    return _redirect_to_https

"""
Limit page access to staff only. Non-staff users will see the usual 404 page.
"""
def staff_only(viewFunction):
    def _staff_only(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        else:
            return viewFunction(request, *args, **kwargs)
    return _staff_only
