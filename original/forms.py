# -*- coding: utf-8 -*-

"""Application forms."""

import hashlib
import random

from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields import (
    BooleanField,
    Field,
    HiddenField,
    StringField,
    TextAreaField,
)


def validate_comment_code(form):
    """Check provided code corresponds to checksum."""

    code_checksum = compute_antispam_checksum(form.commentspamcheck.data)

    if code_checksum != form.commentspamchecksum.data:
        form.commentspamcheck.errors.append(_('Invalid validation code'))
        return False
    else:
        return True


def compute_antispam_checksum(code):
    """Compute checksum of `code`."""
    data = hashlib.md5(code.encode('utf-8')).hexdigest()
    print('Input data:', code, 'output:', data)
    return hashlib.md5(code.encode('utf-8')).hexdigest()


class AntispamField(HiddenField):
    """Antispam checksum generator field."""

    def _value(self):
        print('Computing checksum of:', self.data)
        #if self._meta is None:
        return compute_antispam_checksum(self.data)
        #else:
        #    return self.data


class CommentForm(FlaskForm):
    """Comment submission form."""

    username = StringField(_('Name:'), [validators.DataRequired()])
    remember = BooleanField(_('Remember Name:'))

    commentspamchecksum = AntispamField(
        default=lambda : u'{:04d}'.format(random.randint(0, 9999))
    )
    commentspamcheck = StringField(_('Retype PIN Above:'))

    comment = TextAreaField(_('Comment:'), [validators.DataRequired()])

    def validate(self):
        valid = super(CommentForm, self).validate()
        return valid if not valid else validate_comment_code(self)
