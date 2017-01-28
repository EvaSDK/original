# -*- coding: utf-8 -*-

"""Application forms."""

import hashlib

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import (
    BooleanField,
    HiddenField,
    StringField,
    TextAreaField,
)


def validate_comment_code(form):
    """Check provided code corresponds to checksum."""

    code = form.commentspamcheck.data
    code_checksum = hashlib.md5(code.encode('utf-8')).hexdigest()

    if code_checksum != form.commentspamchecksum.data:
        form.commentspamcheck.errors.append(_('Invalid validation code'))
        return False
    else:
        return True


class CommentForm(FlaskForm):
    """Comment submission form."""

    username = StringField(_('Name:'), [validators.DataRequired()])
    remember = BooleanField(_('Remember Name:'))

    commentspamchecksum = HiddenField()
    commentspamcheck = StringField(_('Retype PIN Above:'))

    comment = TextAreaField(_('Comment:'), [validators.DataRequired()])

    def validate(self):
        valid = super(CommentForm, self).validate()
        return valid if not valid else validate_comment_code(self)
