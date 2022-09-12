<!--
 Copyright 2022 Indoc Research
 
 Licensed under the EUPL, Version 1.2 or – as soon they
 will be approved by the European Commission - subsequent
 versions of the EUPL (the "Licence");
 You may not use this work except in compliance with the
 Licence.
 You may obtain a copy of the Licence at:
 
 https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12
 
 Unless required by applicable law or agreed to in
 writing, software distributed under the Licence is
 distributed on an "AS IS" basis,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 express or implied.
 See the Licence for the specific language governing
 permissions and limitations under the Licence.
 
-->

# Neo4j Api Service

the service wrap up some basic neo4j query into API for further usage.

The service will running at `<host>:6062`

## Installation

follow the step below to setup the service

### Clone

- Clone this repo to machine using `https://git.indocresearch.org/platform/dataset_neo4j.git`

### Prerequisites

- [Poetry](https://python-poetry.org/) dependency manager.
- Vault connection credentials or custom-set environment variables.

### Installation

1. Install [Poetry](https://python-poetry.org/docs/#installation).
2. Configure access to internal package registry.

       poetry config http-basic.pilot ${PIP_USERNAME} ${PIP_PASSWORD}

3. Install dependencies.

       poetry install

4. Add environment variables into `.env`.
5. Run application.

       poetry run python app.py

## Features:

the service uses the swagger to make the api documents: see the detailed [doc](localhost:6062/v1/api-doc)

### Node Related API:

- Retrieve node by id

- Retrieve node by relationship

- Query node by input payload

- Add new nodes

- Update nodes attributes

- Retrieve nodes beyond the relationship

### Relation Related API:

- Retrive the relation between nodes

- Add new relationship between nodes

- Update the relationship between nodes



