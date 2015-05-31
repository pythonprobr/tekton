# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from categoria_app import categoria_facade
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandParallel
from routes.pagseguro import form
from tekton import router
from gaecookie.decorator import no_csrf
from produto_app import produto_facade
from routes.produtos import new, edit
from tekton.gae.middleware.redirect import RedirectResponse


@no_csrf
def index(categoria=''):
    if categoria:
        list_produtos_cmd = produto_facade.listar_produtos_por_categoria_cmd(categoria)
    else:
        list_produtos_cmd = produto_facade.list_produtos_cmd()
    list_categorias_cmd = categoria_facade.list_categorias_cmd()
    CommandParallel(list_categorias_cmd, list_produtos_cmd).execute()
    categorias = list_categorias_cmd.result

    if categoria:
        categoria=int(categoria)
        for cat in categorias:
            if cat.key.id()==categoria:
                categoria_selecionda=cat
                break
    else:
        categoria_selecionda=None

    produtos = list_produtos_cmd.result
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    pay_path = router.to_path(form)
    produto_form = produto_facade.produto_form()

    def localize_produto(produto):
        produto_dct = produto_form.fill_with_model(produto)
        produto_dct['edit_path'] = router.to_path(edit_path, produto_dct['id'])
        produto_dct['delete_path'] = router.to_path(delete_path, produto_dct['id'])
        produto_dct['pay_path'] = router.to_path(pay_path, produto_id=produto_dct['id'])
        return produto_dct

    localized_produtos = [localize_produto(produto) for produto in produtos]
    context = {'produtos': localized_produtos,
               'new_path': router.to_path(new),
               'categorias': categorias,
               'categoria':categoria_selecionda,
               'busca_path': router.to_path(index)}
    return TemplateResponse(context, 'produtos/produto_home.html')


def delete(produto_id):
    produto_facade.delete_produto_cmd(produto_id)()
    return RedirectResponse(router.to_path(index))

