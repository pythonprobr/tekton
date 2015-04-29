# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from produto_app.produto_model import Produto
from routes.produtos.home import index, delete
from gaebusiness.business import CommandExecutionException
from gaegraph.model import Node
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Produto)
        template_response = index()
        self.assert_can_render(template_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        produto = mommy.save_one(Produto)
        redirect_response = delete(produto.key.id())
        self.assertIsInstance(redirect_response, RedirectResponse)
        self.assertIsNone(produto.key.get())

    def test_non_produto_deletion(self):
        non_produto = mommy.save_one(Node)
        self.assertRaises(CommandExecutionException, delete, non_produto.key.id())
        self.assertIsNotNone(non_produto.key.get())

