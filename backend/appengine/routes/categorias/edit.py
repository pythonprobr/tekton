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
def index(categoria_id):
    categoria = categoria_facade.get_categoria_cmd(categoria_id)()
    categoria_form = categoria_facade.categoria_form()
    context = {'save_path': router.to_path(save, categoria_id), 'categoria': categoria_form.fill_with_model(categoria)}
    return TemplateResponse(context, 'categorias/categoria_form.html')

@permissions(ADMIN, MANAGER)
def save(categoria_id, **categoria_properties):
    cmd = categoria_facade.update_categoria_cmd(categoria_id, **categoria_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'categoria': categoria_properties}

        return TemplateResponse(context, 'categorias/categoria_form.html')
    return RedirectResponse(router.to_path(categorias))

