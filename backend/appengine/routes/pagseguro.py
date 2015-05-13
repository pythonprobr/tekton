# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepagseguro import pagseguro_facade
from gaepermission.decorator import login_required, permissions
from permission_app.model import ADMIN
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@login_required
@no_csrf
def index():
    ctx = {'admin_path': to_path(admin)}
    return TemplateResponse(ctx, 'pagseguro/pagseguro_home.html')


@permissions(ADMIN)
@no_csrf
def admin():
    cmd=pagseguro_facade.search_access_data_cmd()
    ctx = {'save_path': to_path(save_admin),
           'app':cmd()}
    return TemplateResponse(ctx, 'pagseguro/pagseguro_admin.html')


@permissions(ADMIN)
def save_admin(email, token):
    pagseguro_facade.create_or_update_access_data_cmd(email, token).execute()
    return RedirectResponse(index)


