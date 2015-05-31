# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import logging

from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from gaepagseguro import pagseguro_facade
from gaepermission.decorator import login_required, permissions
from permission_app.model import ADMIN
from produto_app import produto_facade
import settings
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@login_required
@no_csrf
def form(produto_id):
    cmd = produto_facade.get_produto_cmd(produto_id)

    ctx = {'save_path': to_path(redirecionar), 'produto': cmd()}
    return TemplateResponse(ctx, 'pagseguro/pagseguro_form.html')


@login_required
def redirecionar(_logged_user, produto_id, **kwargs):
    cmd = produto_facade.get_produto_cmd(produto_id)
    produto = cmd()
    item_cmd = pagseguro_facade.validate_item_cmd(produto.titulo, produto.preco, 1, produto.key)
    endereco = {k: kwargs[k] for k in 'street, number, quarter, postalcode, town, state, complement'.split(', ')}
    adress_cmd = pagseguro_facade.validate_address_cmd(**endereco)
    path = to_path(ok)
    url = settings.APP_URL + path
    generate_cmd = pagseguro_facade.generate_payment(url, kwargs['client_name'], kwargs['client_email'], _logged_user,
                                                     adress_cmd, item_cmd)
    try:
        generate_cmd()
    except CommandExecutionException:
        ctx = {'save_path': to_path(redirecionar), 'produto': produto, 'errors': generate_cmd.errors,
               'dados': kwargs}
        return TemplateResponse(ctx, 'pagseguro/pagseguro_form.html')

    url = pagseguro_facade.pagseguro_url(generate_cmd.checkout_code)
    return RedirectResponse(url)


@login_required
@no_csrf
def ok(*args, **kwargs):
    logging.info('Pagamento')


@login_required
@no_csrf
def index():
    ctx = {'admin_path': to_path(admin)}
    return TemplateResponse(ctx, 'pagseguro/pagseguro_home.html')


@permissions(ADMIN)
@no_csrf
def admin():
    cmd = pagseguro_facade.search_access_data_cmd()
    ctx = {'save_path': to_path(save_admin),
           'app': cmd()}
    return TemplateResponse(ctx, 'pagseguro/pagseguro_admin.html')


@permissions(ADMIN)
def save_admin(email, token):
    pagseguro_facade.create_or_update_access_data_cmd(email, token).execute()
    return RedirectResponse(index)


