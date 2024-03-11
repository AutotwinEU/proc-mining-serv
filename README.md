[![PyPI - License](https://img.shields.io/pypi/l/autotwin_pmswsgi)](https://github.com/AutotwinEU/proc-mining-serv/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/autotwin_pmswsgi)](https://www.python.org/downloads/)
[![PyPI - Version](https://img.shields.io/pypi/v/autotwin_pmswsgi)](https://pypi.org/project/autotwin_pmswsgi/)

# Processing Mining Service WSGI for Auto-Twin

The processing mining service WSGI implements a RESTful API that invokes
different system discovery modules to automatically create, update and delete
graph models, Petri nets and automata in a system knowledge graph.

# Services

## Automata Learning

Documentation available [here][automata_learning].

Environment variables to be set:

| **Variable**   | <div style="width:350px">**Description**</div>                     |
|----------------|--------------------------------------------------------------------|
| RES_PATH       | Path to [`resources`](resources) folder                            |
| SKG_RES_PATH   | Path to [`skg_resources`](resources/skg_resources) folder          |
| SEM_RES_PATH   | Path to [`sem_resources`](resources/sem_resources) folder          |
| LSHA_RES_PATH  | Path to [`lsha_resources`](resources/lsha_resources) folder        |
| NEO4J_URI      | Neo4j DB URI (e.g., 'neo4j://localhost:7687' for local instances). |
| NEO4J_USERNAME | Neo4j user (e.g., 'neo4j')                                         |
| NEO4J_PASSWORD | Neo4j DB password                                                  |
| NEO4J_SCHEMA   | Neo4j schema name (i.e., either 'pizzaLineV4' or 'croma')          |

### Request

`POST /automaton`

Requires three input parameters:
- pov: perspective of the automaton to be learned (currently only accepts "item" as value);
- start: beginning of the time window of events to be considered (must be an integer >= 0);
- end: ending of the time window of events to be considered (must be an integer > start).

Example payload:

    {
    "pov": "item",
    "start": 0,
    "end": 100000
    }

### Response

    {
    "status": "OK",
    "learned_sha_name": "AUTO_TWIN_SKG_ITEM-0",
    "pov": "ITEM",
    "from": "0",
    "to": "100000"
    }



[automata_learning]: https://github.com/AutotwinEU/autotwin_automata_learning/tree/master