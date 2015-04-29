# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from tekton import router
from gaecookie.decorator import no_csrf
from produto_app import produto_facade
from routes import produtos
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    return TemplateResponse({'save_path': router.to_path(save)}, 'produtos/produto_form.html')


def save(**produto_properties):
    cmd = produto_facade.save_produto_cmd(**produto_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'produto': produto_properties}

        return TemplateResponse(context, 'produtos/produto_form.html')
    return RedirectResponse(router.to_path(produtos))

