from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, HiddenField, SubmitField
from .translation_utils import lazy_gettext as _


class RegisterForm(FlaskForm):
    """Register new user form."""
    password_validator_added = False

    next = HiddenField()        # for login_or_register.html
    reg_next = HiddenField()    # for register.html

    username = StringField(_('Username'), validators=[
        validators.DataRequired(_('Username is required')),
        username_validator,
        unique_username_validator])
    email = StringField(_('Email'), validators=[
        validators.DataRequired(_('Email is required')),
        validators.Email(_('Invalid Email')),
        unique_email_validator])
    password = PasswordField(_('Password'), validators=[
        validators.DataRequired(_('Password is required')),
        password_validator])
    retype_password = PasswordField(_('Retype Password'), validators=[
        validators.EqualTo('password', message=_('Password and Retype Password did not match'))])
    invite_token = HiddenField(_('Token'))

    submit = SubmitField(_('Register'))

    def validate(self):
        # remove certain form fields depending on user manager config
        user_manager =  current_app.user_manager
        if not user_manager.USER_ENABLE_USERNAME:
            delattr(self, 'username')
        if not user_manager.USER_ENABLE_EMAIL:
            delattr(self, 'email')
        if not user_manager.USER_REQUIRE_RETYPE_PASSWORD:
            delattr(self, 'retype_password')
        # # Add custom username validator if needed
        # if user_manager.USER_ENABLE_USERNAME:
        #     has_been_added = False
        #     for v in self.username.validators:
        #         if v==user_manager.username_validator:
        #             has_been_added = True
        #     if not has_been_added:
        #         self.username.validators.append(user_manager.username_validator)
        # # Add custom password validator if needed
        # has_been_added = False
        # for v in self.password.validators:
        #     if v==user_manager.password_validator:
        #         has_been_added = True
        # if not has_been_added:
        #     self.password.validators.append(user_manager.password_validator)
        # Validate field-validators
        if not super(RegisterForm, self).validate():
            return False
        # All is well
        return True
