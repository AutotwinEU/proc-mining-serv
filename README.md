[![PyPI - License](https://img.shields.io/pypi/l/autotwin_pmswsgi)](https://github.com/AutotwinEU/proc-mining-serv/blob/main/LICENSE)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/autotwin_pmswsgi)](https://www.python.org/downloads/)
[![PyPI - Version](https://img.shields.io/pypi/v/autotwin_pmswsgi)](https://pypi.org/project/autotwin_pmswsgi/)

# Processing Mining Service (PMS) WSGI for Auto-Twin

The processing mining service (PMS) WSGI implements a RESTful API that invokes
different system discovery modules to automatically create, update and delete
graph models, Petri nets and automata in a system knowledge graph (SKG).

## Installation
To facilitate installation, the PMS WSGI is released as a Python module,
`autotwin_pmswsgi`, in the PyPI repository. `autotwin_pmswsgi` implicitly
depends on `pygraphviz`. This dependency however cannot be resolved
automatically by `pip`. As a preparation, you need to install `pygraphviz`
manually, following instructions provided
[here](https://pygraphviz.github.io/documentation/stable/install.html).
Whenever `pygraphviz` is available, the latest version of `autotwin_pmswsgi`
can be easily installed with `pip`.

    pip install autotwin_pmswsgi

## Deployment
The PMS WSGI is almost ready to be deployed for production use once
`autotwin_pmswsgi` is installed successfully. Four environment variables are
additionally required to specify the [Neo4j](https://github.com/neo4j/neo4j)
instance that holds the SKG of the system under consideration.

| Name             | Description                                              |
|------------------|----------------------------------------------------------|
| `NEO4J_URI`      | URI of the Neo4j instance, e.g. `neo4j://localhost:7687` |
| `NEO4J_USERNAME` | Username for the Neo4j instance, e.g. `neo4j`            |
| `NEO4J_PASSWORD` | Password for the Neo4j instance, e.g. `12345678`         |
| `NEO4J_DATABASE` | Database where the SKG is stored, e.g. `neo4j`           |

After setting the above environment variables, you can start up the PMS WSGI on
a [Waitress](https://github.com/Pylons/waitress) server by executing

    waitress-serve autotwin_pmswsgi:wsgi

## Containerization
To enable containerization, the PMS WSGI is also released as a Docker image,
`ghcr.io/autotwineu/proc-mining-serv`, in the GHCR registry. Suppose that a
Docker engine is running on your machine. Deploying the PMS WSGI on a Docker
container named `proc-mining-serv` can be done via a single command.

    docker run --detach --env NEO4J_URI=<NEO4J_URI> --env NEO4J_USERNAME=<NEO4J_USERNAME> --env NEO4J_PASSWORD=<NEO4J_PASSWORD> --env NEO4J_DATABASE=<NEO4J_DATABASE> --name proc-mining-serv --pull always ghcr.io/autotwineu/proc-mining-serv

`<NEO4J_URI>`, `<NEO4J_USERNAME>`, `<NEO4J_PASSWORD>` and `<NEO4J_DATABASE>`
correspond to the values of the four environment variables required by the PMS
WSGI (see [Deployment](#deployment)).

## RESTful API
The PMS WSGI listens HTTP requests on port `8080` and is accessible through a
RESTful API that exposes the following endpoints for different types of models.
The content types of the request and response for each API endpoint are both
`application/json`.

--------------------------------------------------------------------------------

### API Endpoints for Graph Models

<details>
    <summary>
        <code>POST</code>
        <code><b>/graph-model</b></code>
        <code>(create a graph model in the SKG)</code>
    </summary>
    <br/>

**Parameters**
> None

**Body**
> Definition
>
> | Name                   | Type                    | Description                            |
> |------------------------|-------------------------|----------------------------------------|
> | `name`                 | `string`                | Name of the system to be discovered    |
> | `version`              | `string`                | Version of the system to be discovered |
> | `neo4j:interval`       | `array[number\|string]` | Interval of the event log to be used   |
> | `model:delays:seize`   | `number\|string`        | Delay in seizing a queued part         |
> | `model:delays:release` | `number\|string`        | Delay in releasing a blocked part      |

> Example
> ```json
> {
>     "name": "Pizza Line",
>     "version": "V3",
>     "neo4j": {
>         "interval": [0, 30000000]
>     },
>     "model": {
>         "delays": {
>             "seize": 0,
>             "release": 0
>         }
>     }
> }
> ```

**Response**
> Code: 201

> Definition
> 
> | Name       | Type     | Description                     |
> |------------|----------|---------------------------------|
> | `model_id` | `string` | ID of the generated graph model |

> Example
> ```json
> {
>     "model_id": "4:1b90f766-3bae-49da-b38f-60f0d84b2d08:226294"
> }
> ```

</details>

--------------------------------------------------------------------------------

### API Endpoints for Petri Nets

<details>
    <summary>
        <code>POST</code>
        <code><b>/petri-net</b></code>
        <code>(create a Petri net in the SKG)</code>
    </summary>
    <br/>

**Parameters**
> None

**Body**
> None

**Response**
> Code: 501

> Definition
> 
> | Name          | Type     | Description                   |
> |---------------|----------|-------------------------------|
> | `code`        | `string` | Code of the HTTP error        |
> | `name`        | `string` | Name of the HTTP error        |
> | `description` | `string` | Description of the HTTP error |

> Example
> ```json
> {
>     "code": 501,
>     "name": "Not Implemented",
>     "description": "The server does not support the action requested by the browser."
> }
> ```

</details>

--------------------------------------------------------------------------------

### API Endpoints for Automata

<details>
    <summary>
        <code>POST</code>
        <code><b>/automaton</b></code>
        <code>(create an automaton in the SKG)</code>
    </summary>
    <br/>

**Parameters**
> None

**Body**
> None

**Response**
> Code: 501

> Definition
> 
> | Name          | Type     | Description                   |
> |---------------|----------|-------------------------------|
> | `code`        | `string` | Code of the HTTP error        |
> | `name`        | `string` | Name of the HTTP error        |
> | `description` | `string` | Description of the HTTP error |

> Example
> ```json
> {
>     "code": 501,
>     "name": "Not Implemented",
>     "description": "The server does not support the action requested by the browser."
> }
> ```

</details>

--------------------------------------------------------------------------------
