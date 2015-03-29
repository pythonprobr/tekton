# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from base import GAETestCase
from datetime import datetime, date
from decimal import Decimal
from categoria_app.categoria_model import Categoria
from routes.categorias.edit import index, save
from mommygae import mommy
from tekton.gae.middleware.redirect import RedirectResponse


class IndexTests(GAETestCase):
    def test_success(self):
        categoria = mommy.save_one(Categoria)
        template_response = index(categoria.key.id())
        self.assert_can_render(template_response)


class EditTests(GAETestCase):
    def test_success(self):
        categoria = mommy.save_one(Categoria)
        old_properties = categoria.to_dict()
        redirect_response = save(categoria.key.id(), nome='nome_string')
        self.assertIsInstance(redirect_response, RedirectResponse)
        edited_categoria = categoria.key.get()
        self.assertEquals('nome_string', edited_categoria.nome)
        self.assertNotEqual(old_properties, edited_categoria.to_dict())

    def test_error(self):
        categoria = mommy.save_one(Categoria)
        old_properties = categoria.to_dict()
        template_response = save(categoria.key.id())
        errors = template_response.context['errors']
        self.assertSetEqual(set(['nome']), set(errors.keys()))
        self.assertEqual(old_properties, categoria.key.get().to_dict())
        self.assert_can_render(template_response)
