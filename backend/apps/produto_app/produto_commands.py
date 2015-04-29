# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode, NodeSearch, DeleteNode, DestinationsSearch, CreateSingleOriginArc
from produto_app.produto_model import Produto, CategoriaParaProduto


class ProdutoSaveForm(ModelForm):
    """
    Form used to save and update Produto
    """
    _model_class = Produto
    _include = [Produto.titulo, 
                Produto.preco, 
                Produto.descricao]


class ProdutoForm(ModelForm):
    """
    Form used to expose Produto's properties for list or json
    """
    _model_class = Produto


class GetProdutoCommand(NodeSearch):
    _model_class = Produto


class DeleteProdutoCommand(DeleteNode):
    _model_class = Produto


class SaveProdutoCommand(SaveCommand):
    _model_form_class = ProdutoSaveForm

class SalvarProdutoAtreladoACategoria(CreateSingleOriginArc):
    arc_class = CategoriaParaProduto

    def __init__(self, categoria, **produto_propriedades):
        destination = SaveProdutoCommand(**produto_propriedades)
        super(SalvarProdutoAtreladoACategoria, self).__init__(categoria, destination)


class UpdateProdutoCommand(UpdateNode):
    _model_form_class = ProdutoSaveForm


class ListProdutoCommand(ModelSearchCommand):
    def __init__(self):
        super(ListProdutoCommand, self).__init__(Produto.query_by_creation())

class ListarProdutosPorCategoria(DestinationsSearch):
    arc_class = CategoriaParaProduto

