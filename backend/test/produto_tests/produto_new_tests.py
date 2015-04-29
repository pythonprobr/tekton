# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from decimal import Decimal

from base import GAETestCase
from categoria_app.categoria_model import Categoria
from mommygae import mommy
from produto_app import produto_facade
from produto_app.produto_model import Produto
from routes.produtos.new import index, save
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        template_response = index()
        self.assert_can_render(template_response)


class SaveTests(GAETestCase):
    def test_success(self):
        categoria = mommy.save_one(Categoria)
        self.assertIsNone(Produto.query().get())
        redirect_response = save(categoria=str(categoria.key.id()), titulo='titulo_string', preco='1.02',
                                 descricao='descricao_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        saved_produto = Produto.query().get()
        self.assertIsNotNone(saved_produto)
        self.assertEquals('titulo_string', saved_produto.titulo)
        self.assertEquals(Decimal('1.02'), saved_produto.preco)
        self.assertEquals('descricao_string', saved_produto.descricao)
        listar_produtos_cmd = produto_facade.listar_produtos_por_categoria_cmd(categoria)
        produtos = listar_produtos_cmd()
        self.assertListEqual([saved_produto], produtos)

    def test_error(self):
        template_response = save()
        errors = template_response.context['errors']
        self.assertSetEqual(set(['titulo', 'preco', 'descricao']), set(errors.keys()))
        self.assert_can_render(template_response)
