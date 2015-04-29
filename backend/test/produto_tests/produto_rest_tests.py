# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from produto_app.produto_model import Produto
from routes.produtos import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Produto)
        mommy.save_one(Produto)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        produto_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'titulo', 'preco', 'descricao']), set(produto_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Produto.query().get())
        json_response = rest.new(None, titulo='titulo_string', preco='1.02', descricao='descricao_string')
        db_produto = Produto.query().get()
        self.assertIsNotNone(db_produto)
        self.assertEquals('titulo_string', db_produto.titulo)
        self.assertEquals(Decimal('1.02'), db_produto.preco)
        self.assertEquals('descricao_string', db_produto.descricao)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['titulo', 'preco', 'descricao']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        produto = mommy.save_one(Produto)
        old_properties = produto.to_dict()
        json_response = rest.edit(None, produto.key.id(), titulo='titulo_string', preco='1.02', descricao='descricao_string')
        db_produto = produto.key.get()
        self.assertEquals('titulo_string', db_produto.titulo)
        self.assertEquals(Decimal('1.02'), db_produto.preco)
        self.assertEquals('descricao_string', db_produto.descricao)
        self.assertNotEqual(old_properties, db_produto.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        produto = mommy.save_one(Produto)
        old_properties = produto.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, produto.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['titulo', 'preco', 'descricao']), set(errors.keys()))
        self.assertEqual(old_properties, produto.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        produto = mommy.save_one(Produto)
        rest.delete(None, produto.key.id())
        self.assertIsNone(produto.key.get())

    def test_non_produto_deletion(self):
        non_produto = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_produto.key.id())
        self.assertIsNotNone(non_produto.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

