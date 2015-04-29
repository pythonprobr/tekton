# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from produto_app.produto_commands import ListProdutoCommand, UpdateProdutoCommand, ProdutoForm,\
    GetProdutoCommand, DeleteProdutoCommand, ListarProdutosPorCategoria, SalvarProdutoAtreladoACategoria


def save_produto_cmd(categoria, **produto_properties):
    """
    Command to save Produto entity
    :param produto_properties: a dict of properties to save on model
    :return: a Command that save Produto, validating and localizing properties received as strings
    """
    return SalvarProdutoAtreladoACategoria(categoria, **produto_properties)


def update_produto_cmd(produto_id, **produto_properties):
    """
    Command to update Produto entity with id equals 'produto_id'
    :param produto_properties: a dict of properties to update model
    :return: a Command that update Produto, validating and localizing properties received as strings
    """
    return UpdateProdutoCommand(produto_id, **produto_properties)


def list_produtos_cmd():
    """
    Command to list Produto entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListProdutoCommand()


def produto_form(**kwargs):
    """
    Function to get Produto's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return ProdutoForm(**kwargs)


def get_produto_cmd(produto_id):
    """
    Find produto by her id
    :param produto_id: the produto id
    :return: Command
    """
    return GetProdutoCommand(produto_id)



def delete_produto_cmd(produto_id):
    """
    Construct a command to delete a Produto
    :param produto_id: produto's id
    :return: Command
    """
    return DeleteProdutoCommand(produto_id)


def listar_produtos_por_categoria_cmd(categoria):
    return ListarProdutosPorCategoria(categoria)