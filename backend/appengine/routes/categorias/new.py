# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from categoria_app import categoria_facade
from routes import categorias
from tekton.gae.middleware.redirect import RedirectResponse
from gaepermission.decorator import permissions
from permission_app.model import ADMIN, MANAGER

@permissions(ADMIN, MANAGER)
@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'categorias/categoria_form.html')

@permissions(ADMIN, MANAGER)
def save(**categoria_properties):
    cmd = categoria_facade.save_categoria_cmd(**categoria_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'categoria': categoria_properties}

        return TemplateResponse(context, 'categorias/categoria_form.html')
    return RedirectResponse(router.to_path(categorias))

