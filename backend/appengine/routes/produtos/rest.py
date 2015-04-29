# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from tekton.gae.middleware.json_middleware import JsonResponse
from produto_app import produto_facade


def index():
    cmd = produto_facade.list_produtos_cmd()
    produto_list = cmd()
    produto_form = produto_facade.produto_form()
    produto_dcts = [produto_form.fill_with_model(m) for m in produto_list]
    return JsonResponse(produto_dcts)


def new(_resp, **produto_properties):
    cmd = produto_facade.save_produto_cmd(**produto_properties)
    return _save_or_update_json_response(cmd, _resp)


def edit(_resp, id, **produto_properties):
    cmd = produto_facade.update_produto_cmd(id, **produto_properties)
    return _save_or_update_json_response(cmd, _resp)


def delete(_resp, id):
    cmd = produto_facade.delete_produto_cmd(id)
    try:
        cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)


def _save_or_update_json_response(cmd, _resp):
    try:
        produto = cmd()
    except CommandExecutionException:
        _resp.status_code = 500
        return JsonResponse(cmd.errors)
    produto_form = produto_facade.produto_form()
    return JsonResponse(produto_form.fill_with_model(produto))

