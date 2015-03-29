# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode
from categoria_app.categoria_model import Categoria



class CategoriaSaveForm(ModelForm):
    """
    Form used to save and update Categoria
    """
    _model_class = Categoria
    _include = [Categoria.nome]


class CategoriaForm(ModelForm):
    """
    Form used to expose Categoria's properties for list or json
    """
    _model_class = Categoria


class GetCategoriaCommand(NodeSearch):
    _model_class = Categoria


class DeleteCategoriaCommand(DeleteNode):
    _model_class = Categoria


class SaveCategoriaCommand(SaveCommand):
    _model_form_class = CategoriaSaveForm


class UpdateCategoriaCommand(UpdateNode):
    _model_form_class = CategoriaSaveForm


class ListCategoriaCommand(ModelSearchCommand):
    def __init__(self):
        super(ListCategoriaCommand, self).__init__(Categoria.query_by_creation())

