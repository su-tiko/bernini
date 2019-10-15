from django.contrib.auth.forms import AuthenticationForm


class UserAdminAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        return super().confirm_login_allowed(user)
