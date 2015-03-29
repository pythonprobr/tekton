# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaepermission.decorator import permissions
from permission_app.model import ADMIN, MANAGER
from tekton import router
from gaecookie.decorator import no_csrf
from categoria_app import categoria_facade
from routes.categorias import new, edit
from tekton.gae.middleware.redirect import RedirectResponse

@permissions(ADMIN, MANAGER)
@no_csrf
def index():
    cmd = categoria_facade.list_categorias_cmd()
    categorias = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    categoria_form = categoria_facade.categoria_form()

    def localize_categoria(categoria):
        categoria_dct = categoria_form.fill_with_model(categoria)
        categoria_dct['edit_path'] = router.to_path(edit_path, categoria_dct['id'])
        categoria_dct['delete_path'] = router.to_path(delete_path, categoria_dct['id'])
        return categoria_dct

    localized_categorias = [localize_categoria(categoria) for categoria in categorias]
    context = {'categorias': localized_categorias,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'categorias/categoria_home.html')

@permissions(ADMIN)
def delete(categoria_id):
    categoria_facade.delete_categoria_cmd(categoria_id)()
    return RedirectResponse(router.to_path(index))

