# Copyright 2022 Indoc Research
# 
# Licensed under the EUPL, Version 1.2 or – as soon they
# will be approved by the European Commission - subsequent
# versions of the EUPL (the "Licence");
# You may not use this work except in compliance with the
# Licence.
# You may obtain a copy of the Licence at:
# 
# https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
# 
# Unless required by applicable law or agreed to in
# writing, software distributed under the Licence is
# distributed on an "AS IS" basis,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied.
# See the Licence for the specific language governing
# permissions and limitations under the Licence.
# 

from unittest.mock import Mock

import pytest
from opentelemetry.trace import INVALID_SPAN
from opentelemetry.trace import SpanKind
from py2neo import Transaction

from app.opentelemetry.instrumentation.py2neo import Py2NeoInstrumentor


@pytest.fixture
def transaction():
    class Profile(Mock):
        protocol = 'bolt'

    class Connector(Mock):
        @property
        def profile(self):
            return Profile()

        def run_in_tx(self, *args, **kwds):
            return []

    class Graph(Mock):
        @property
        def service(self):
            return self

        @property
        def connector(self):
            return Connector()

    yield Transaction(Graph())


@pytest.fixture
def py2neo_instrumentor():
    yield Py2NeoInstrumentor()


class TestPy2NeoInstrumentor:
    def test_instrumentor_wraps_py2neo_transaction_run_method_with_tracer_span(
        self, faker, py2neo_instrumentor, transaction, mocker
    ):
        py2neo_instrumentor.instrument()

        mock_start_as_current_span = mocker.patch.context_manager(
            py2neo_instrumentor._tracer, 'start_as_current_span', return_value=INVALID_SPAN
        )

        expected_cypher = faker.pystr()

        transaction.run(expected_cypher)

        mock_start_as_current_span.assert_called_once_with(expected_cypher, kind=SpanKind.CLIENT)

        py2neo_instrumentor.uninstrument()
