# pokeapi
#### A small source of information for Pokemon Moves and Advantages

This small API works using [Flask-Restplus](https://github.com/noirbizarre/flask-restplus) as black-end's framework.
It also depend from the original [PokeApi](https://pokeapi.co), this API is a sort of wrapper around it which has it own capabilities. 

It has two different endpoints:
* /advantages 
  * POST: Expects two move types and base on them determinates 
    1. If the first one can deal *double_damage_to* to the second on
    1. If the first one can take *half_damage_from* the second type
    1. If the first one can take *no_damage_from* the second type
* /moves
  * POST: Check for moves in common shared by a pokemon list
    1. Return the shared moves
    1. Moves can be requested in different language
    
 All the resquests are documented using *Swagger*.
 
 For installing the package, you can use the following commands:
 
 ```
  pip install -qU -r requirements.txt
 ```
 
And then, you just need to start the application. You can take a look on the root ```run.py``` for an basic example

#### Making requests
If you want to request info, you'll need to point to ```{your_host}/api/v1/```, this ```api/v1``` represents the blueprint for the API. 
For instance ```http://127.0.0.1:5000/api/v1/advantages/``` is the valid endpoint for requesting advantages comparations.

Swagger will be available at ```http://127.0.0.1:5000/api/v1/``` and http://127.0.0.1:5000/api/v1/swagger.json is a JSON representation of the API Documentation

#### Cache
Since this API depents so much in requets, it saves the JSON response for move_types and pokemons to help speed up the transactions from second time and ahead
