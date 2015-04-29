# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from google.appengine.ext import ndb

from categoria_app.categoria_model import Categoria
from gaegraph.model import Node, Arc
from gaeforms.ndb import property


class Produto(Node):
    titulo = ndb.StringProperty(required=True)
    descricao = ndb.TextProperty(required=True)
    preco = property.SimpleCurrency(required=True)


class CategoriaParaProduto(Arc):
    origin = ndb.KeyProperty(Categoria, required=True)
    destination = ndb.KeyProperty(Produto, required=True)


