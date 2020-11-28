===========
ADSO Server
===========
.. role:: js(code)
   :language: javascript


Requirements 
--------------
Docker Engine and Docker Compose (https://docs.docker.com/compose/install/)

How to start server
--------------------
Run `docker-compose up` in root folder of project.

The API and Websocket server will listen on same address *SERVER_IP:8000*, here *SERVER_IP* is the IP address of the server, for local test it should be *127.0.0.1*

How to use adso-server
-----------------------

REST Api schema : 
*************************
There is only one API at URI `http://SERVER_IP:8000/api-token-auth/`, this API is used to obtain the access token to connect with Websocket server. Client need to send POST request with username and password, default is **admin** and **admin**

See *openapi-schema.yml* file for the complete schema.

Websocket communication : 
*************************

Websocket server is available at `ws://SERVER_IP:8000/ws/notification`

List of message accepted by server :

* **Authentication message**

  * **Format** : :js:`{action: "Authentication", payload: { token : string, modelID: string }}`
  
  * **Usage** : this message need to be sent by client after connecting to server in order to get the structure (inputs/outputs) of current simulation model. Here `token` is the access token obtained by `api-token-auth` API, `modelID` is the id of simulation model, for this demo it is `ProjectileMotion`.

  * **Example** : :js:`{action: "Authentication", payload: { token : "48f21793804566e518af0fdda0f65febc1b62427", modelID: "ProjectileMotion" }}`


* **Request run message**

  * Format : :js:`{action: "request_run", payload: { [input_id: string] : {value: number, dtype: string} }}`
  
  * Usage : this message is used to request the execution of simulation model with new input values. The `input_id` can be obtained from the response of server after authenticating with **authentication message** by prefixing *"lab."* to the name of inputs

  * **Example** : 
  
    .. code-block:: javascript

      {"action": "request_run",
        "payload": {
          "lab.angle": {
            "value": 32,
            "dtype": "float"
          },
          "lab.k": {
            "value": 0.46,
            "dtype": "float"
          },
          "lab.mass": {
            "value": 6.2,
            "dtype": "float"
          }
        }
      }

List of message sent from server to client :

* **Model components message**

  * **Format** : :js:`{action: "MODEL_COMPONENT", payload: { input : Array<{[key:string]: any}>, output: Array<{[key:string]: any}> }}`
  
  * **Usage** : this message normally is sent right after the authentication request from client, it contains the information about the structure of simulation model, this data helps the client to build the interface corresponding to the simulation model.

  * **Example** : 
  
    .. code-block:: javascript

      {
        "action": "MODEL_COMPONENT",
        "payload": {
          "input": [
            {
              "name": "mass",
              "desc": "Mass of projectile",
              "parent": "lab",
              "unit": "kg",
              "dtype": "float",
              "value_range": [0, 10],
              "value": 1.5
            },
            {
              "name": "k",
              "desc": "Friction coefficient",
              "parent": "lab",
              "unit": null,
              "dtype": "float",
              "value_range": [0, 1],
              "value": 0
            },
            {
              "name": "angle",
              "desc": "Launch angle",
              "parent": "lab",
              "unit": "degree",
              "dtype": "float",
              "value_range": [0, 90],
              "value": 50
            },
            {
              "name": "speed",
              "desc": "Launch speed",
              "parent": "lab",
              "unit": "m/s",
              "dtype": "float",
              "value_range": [0, 20],
              "value": 12.5
            },
            {
              "name": "position",
              "desc": "Initial position",
              "parent": "lab",
              "unit": null,
              "dtype": "ndarray",
              "value_range": [null, null],
              "value": [0, 0, 0]
            }
          ],
          "output": [
            {
              "name": "coordinate",
              "desc": "Coordinate of projectile",
              "parent": "lab",
              "unit": null,
              "dtype": "Any",
              "value_range": [null, null],
              "value": 0
            },
            {
              "name": "spd",
              "desc": "Speed of projectile",
              "parent": "lab",
              "unit": null,
              "dtype": "Any",
              "value_range": [null, null],
              "value": 0
            },
            {
              "name": "acc",
              "desc": "Acceleration of projectile",
              "parent": "lab",
              "unit": null,
              "dtype": "Any",
              "value_range": [null, null],
              "value": 0
            },
            {
              "name": "time",
              "desc": "Total time",
              "parent": "lab",
              "unit": null,
              "dtype": "Any",
              "value_range": [null, null],
              "value": 0
            }
          ]
        }
      }


* **Computed result message**

  * Format : :js:`{action: "computed_output", payload: { [output_name: string] : {value: any, dtype: string, desc: string} }}`
  
  * Usage : this message contains the result of simulation initiated by **request run message**, it is used to update the graphs of client.

  * **Example** : 
    
    .. code-block:: JavaScript
      
      {
        "action": "computed_output",
        "payload": {
          "coordinate": {
            "value": [
              [0, 0],
              [0.055102682404810956, 0.03394159872669933],
              [0.11016449733667975, 0.06687738814590993]
            ],
            "dtype": "ndarray",
            "desc": "Coordinate of projectile"
          },
          "spd": {
            "value": [
              [5.512312625016769, 3.4444752175158317],
              [5.508224361483508, 3.3438569698683693],
              [5.50413913005308, 3.243313346782429]
            ],
            "dtype": "ndarray",
            "desc": "Speed of projectile"
          },
          "acc": {
            "value": [
              [-0.40897803346898604, -10.065557838718917],
              [-0.4086747106907119, -10.05809261389346],
              [-0.40837161287490586, -10.050632925729019]
            ],
            "dtype": "ndarray",
            "desc": "Acceleration of projectile"
          },
          "time": {
            "value": 0.7000000000000004,
            "dtype": "float",
            "desc": "Total time"
          }
        }
      }

* **Server log message**

  * Format : :js:`{action: "server_log", payload: string}`
  
  * Usage : this message contains log of server, it is used to show in log dialog of client.

  * **Example** : 
    
    .. code-block:: JavaScript
      
      {
        action: "server_log",
        payload: "Job bcb3bf03-9bc3-47e7-94a0-c166eecdc30b computed"
      }



Development
----------------

* Trung Le <trung.le@cast2cloud.com>

Contributors
------------

None yet. Why not be the first?


