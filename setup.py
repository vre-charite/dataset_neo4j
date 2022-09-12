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

from neo4j_api import neo4j_connection

neo4j_session = neo4j_connection.session()

user_init = 'create (n:User) set n = {email:"ivana.zhangyf@gmail.com", \
first_name:"admin", last_name:"admin", name:"stage-admin", path:"users", role:"admin"} return n'

neo4j_session.run(user_init)


db_constraint_init = '''
    CREATE CONSTRAINT constraint_code
    ON (n:Container)
    ASSERT n.code IS UNIQUE
'''

neo4j_session.run(db_constraint_init)