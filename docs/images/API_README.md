### Descrição genérica:
This API manages the data persistence and the communication between the simulation and the agentic framework. The simulation uses the network protocol HTTP, to post the contextual and configuration data to the API. Then the API use the configuration data to set the framework ready and the contextual data for consult the agents, then  the simulation can get the answer back.
Besides that, the data persistence layer stores data, such as, agent's states and the response of the agentic framework. The relational database is set, using PostgreSQL tool, prioritizing the JSON format field.

### Funcionamento / Uso:
Explicação a ser feita...

<details>
<summary>1. Simulation:</summary>

* URL: http//:localhost:8000/simulations

<details>
<summary>post: enviar / criar</summary>

```
   {
        "platform": "Gama",
        "attributes": {
            "numPop": 500,
            "numStudants": 100,
            "numWorker": 300,
            "numRetired": 100
        },
        "simulation_id": 1,
        "created_at": "2026-07-21T15:31:57.737Z"
    }
```
</details>

<details>
 <summary>get: pegar dados</summary>

```
   {
        "platform": "Gama",
        "attributes": {
            "numPop": 500,
            "numWorker": 300,
            "numRetired": 100,
            "numStudants": 100
        },
        "simulation_id": 1,
        "created_at": "2026-07-28T16:55:50.839225Z",
        "finished_at": null
    }
```
</details>
<details>
 <summary>patch: Atualizar</summary>

```
 {
        "platform": "Gama",
        "attributes": {
            "numPop": 500,
            "numStudants": 100,
            "numWorker": 300,
            "numRetired": 100
        },
        "simulation_id": 1,
        "created_at": "2026-07-21T15:31:57.737Z"
    }
```
</details>
</details>
<details>
<summary>2. Round:</summary>

* URL: http//:localhost:8000/rounds

<details>
<summary>post: enviar / criar</summary>

```
   {

    "attributes": {
        "whether": "rainy",
        "dayOfTheWeek": "moonday"
    }

}
```
</details>
<details>
 <summary>get: pegar dados</summary>


```
   {
        "attributes": {
            "whether": "sunny",
            "dayOfTheWeek": "friday"
        },
        "simulation_id": 16,
        "round_id": 1,
        "created_at": "2026-07-28T16:56:33.101865Z",
        "metrics": null,
        "finished_at": null
    },
    {
        "attributes": {
            "whether": "rainy",
            "dayOfTheWeek": "friday"
        },
        "simulation_id": 16,
        "round_id": 2,
        "created_at": "2026-07-28T19:42:34.010709Z",
        "metrics": null,
        "finished_at": null
    },
    {
        "attributes": {
            "whether": "rainy",
            "dayOfTheWeek": "moonday"
        },
        "simulation_id": 16,
        "round_id": 3,
        "created_at": "2026-07-28T19:44:29.225665Z",
        "metrics": null,
        "finished_at": null
    }
```
</details>
<details>
 <summary>patch: Atualizar</summary>

```
  {

    "attributes": {
        "whether": "rainy",
        "dayOfTheWeek": "moonday"
    }

}
```
</details>
</details>
<details>
<summary>3. Agents:</summary>

* URL: http//:localhost:8000/agents

<details>
<summary>post: enviar / criar</summary>


```
[
{ 
        "attributes": {
            "occupation": "studant",
            "gender": "male",
            "age": 24
        },

        "state": [
            
        ],
        
        "agent_id": 1
}

{ 
        "attributes": {
            "occupation": "worker",
            "gender": "female",
            "age": 30
        },

        "state": [
            
        ],
        
        "agent_id": 2
}

{ 
        "attributes": {
            "occupation": "retired",
            "gender": "male",
            "age": 70
        },

        "state": [
            
        ],
        
        "agent_id": 3
}        

]
```
</details>
<details>
 <summary>get: pegar dados</summary>


```
[
  {
        "attributes": {
            "age": 24,
            "gender": "male",
            "occupation": "studant"
        },
        "state": [],
        "simulation_id": 1,
        "agent_id": 1,
        "created_at": "2026-07-28T18:21:50.534674Z"
    } 

{ 
        "attributes": {
            "occupation": "worker",
            "gender": "female",
            "age": 30
        },

        "state": [
            
        ],
        
        "agent_id": 2
}

{ 
        "attributes": {
            "occupation": "retired",
            "gender": "male",
            "age": 70
        },

        "state": [
            
        ],
        
        "agent_id": 3
}    
]
```
</details>
<details>
<summary>patch: Atualizar:</summary>

‘’’
 
‘’’
</details>
</details>
<details>
<summary>4. Decision:</summary>

* URL: http//:localhost:8000/decisions/reasoning

<details>
<summary>post: enviar / criar</summary>


```
  {
    "type": "traffic_choice",
    "framework": "agno",

    "config": { // configurações da llm
        
        "llm_api": "gemini",
        "llm_model": "gemini-3.5-flash-lite",
        "temperature": 1,
        "enable_agentic_memory": false,
        "seed": 1
    },
    
    "context": [ // = parametros
        { 
            "agent_id": 28,
            "congestion_level": "low",
            "fatigue_level": "low",
            "occupation": "studant",
            "age": 24,
            "gender": "male"
        }
    ]
}
```
</details>
</details>

### Como testar sem simulação:
… Descrever o postman

### Possíveis erros:
<details>
<summary> </summary>
   
* Má formatação do Json<br>
* Dados obrigatórios faltando, como o id da simulação, round ou agente<br>
* Na etapa de decisão, faltar a chava da api ou algum atributo de configuração estar com o nome ou valor errado<br>

</details>


