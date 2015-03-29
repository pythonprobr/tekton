# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime, date
from decimal import Decimal
from base import GAETestCase
from categoria_app.categoria_model import Categoria
from routes.categorias import rest
from gaegraph.model import Node
from mock import Mock
from mommygae import mommy


class IndexTests(GAETestCase):
    def test_success(self):
        mommy.save_one(Categoria)
        mommy.save_one(Categoria)
        json_response = rest.index()
        context = json_response.context
        self.assertEqual(2, len(context))
        categoria_dct = context[0]
        self.assertSetEqual(set(['id', 'creation', 'nome']), set(categoria_dct.iterkeys()))
        self.assert_can_serialize_as_json(json_response)


class NewTests(GAETestCase):
    def test_success(self):
        self.assertIsNone(Categoria.query().get())
        json_response = rest.new(None, nome='nome_string')
        db_categoria = Categoria.query().get()
        self.assertIsNotNone(db_categoria)
        self.assertEquals('nome_string', db_categoria.nome)
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        resp = Mock()
        json_response = rest.new(resp)
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['nome']), set(errors.keys()))
        self.assert_can_serialize_as_json(json_response)


class EditTests(GAETestCase):
    def test_success(self):
        categoria = mommy.save_one(Categoria)
        old_properties = categoria.to_dict()
        json_response = rest.edit(None, categoria.key.id(), nome='nome_string')
        db_categoria = categoria.key.get()
        self.assertEquals('nome_string', db_categoria.nome)
        self.assertNotEqual(old_properties, db_categoria.to_dict())
        self.assert_can_serialize_as_json(json_response)

    def test_error(self):
        categoria = mommy.save_one(Categoria)
        old_properties = categoria.to_dict()
        resp = Mock()
        json_response = rest.edit(resp, categoria.key.id())
        errors = json_response.context
        self.assertEqual(500, resp.status_code)
        self.assertSetEqual(set(['nome']), set(errors.keys()))
        self.assertEqual(old_properties, categoria.key.get().to_dict())
        self.assert_can_serialize_as_json(json_response)


class DeleteTests(GAETestCase):
    def test_success(self):
        categoria = mommy.save_one(Categoria)
        rest.delete(None, categoria.key.id())
        self.assertIsNone(categoria.key.get())

    def test_non_categoria_deletion(self):
        non_categoria = mommy.save_one(Node)
        response = Mock()
        json_response = rest.delete(response, non_categoria.key.id())
        self.assertIsNotNone(non_categoria.key.get())
        self.assertEqual(500, response.status_code)
        self.assert_can_serialize_as_json(json_response)

