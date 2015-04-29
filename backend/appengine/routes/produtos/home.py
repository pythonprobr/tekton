# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from tekton import router
from gaecookie.decorator import no_csrf
from produto_app import produto_facade
from routes.produtos import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index():
    cmd = produto_facade.list_produtos_cmd()
    produtos = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    produto_form = produto_facade.produto_form()

    def localize_produto(produto):
        produto_dct = produto_form.fill_with_model(produto)
        produto_dct['edit_path'] = router.to_path(edit_path, produto_dct['id'])
        produto_dct['delete_path'] = router.to_path(delete_path, produto_dct['id'])
        return produto_dct

    localized_produtos = [localize_produto(produto) for produto in produtos]
    context = {'produtos': localized_produtos,
               'new_path': router.to_path(new)}
    return TemplateResponse(context, 'produtos/produto_home.html')


def delete(produto_id):
    produto_facade.delete_produto_cmd(produto_id)()
    return RedirectResponse(router.to_path(index))

