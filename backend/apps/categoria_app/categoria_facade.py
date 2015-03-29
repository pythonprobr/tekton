# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from categoria_app.categoria_commands import ListCategoriaCommand, SaveCategoriaCommand, UpdateCategoriaCommand, CategoriaForm,\
    GetCategoriaCommand, DeleteCategoriaCommand


def save_categoria_cmd(**categoria_properties):
    """
    Command to save Categoria entity
    :param categoria_properties: a dict of properties to save on model
    :return: a Command that save Categoria, validating and localizing properties received as strings
    """
    return SaveCategoriaCommand(**categoria_properties)


def update_categoria_cmd(categoria_id, **categoria_properties):
    """
    Command to update Categoria entity with id equals 'categoria_id'
    :param categoria_properties: a dict of properties to update model
    :return: a Command that update Categoria, validating and localizing properties received as strings
    """
    return UpdateCategoriaCommand(categoria_id, **categoria_properties)


def list_categorias_cmd():
    """
    Command to list Categoria entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListCategoriaCommand()


def categoria_form(**kwargs):
    """
    Function to get Categoria's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return CategoriaForm(**kwargs)


def get_categoria_cmd(categoria_id):
    """
    Find categoria by her id
    :param categoria_id: the categoria id
    :return: Command
    """
    return GetCategoriaCommand(categoria_id)



def delete_categoria_cmd(categoria_id):
    """
    Construct a command to delete a Categoria
    :param categoria_id: categoria's id
    :return: Command
    """
    return DeleteCategoriaCommand(categoria_id)

