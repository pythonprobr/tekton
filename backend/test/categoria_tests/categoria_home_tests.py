# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from categoria_app.categoria_model import Categoria
from routes.categorias.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Categoria)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        categoria = mommy.save_one(Categoria)
        redirect_response = delete(categoria.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(categoria.key.get())

    def test_non_categoria_deletion(self):
        non_categoria = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_categoria.key.id())
        self.assertIsNotNone(non_categoria.key.get())

