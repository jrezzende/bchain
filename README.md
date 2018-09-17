# bchain
A very basic implementation of a blockchain - builted for educational purposes -.

Usages:

To interact with your blockchain, first you need to run the server.
On command prompt, enter your project's current folder and type:
$ python runserver.py

 * Serving Flask app "blockchain_api" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 
 With your server up and running, to mine a block you need to make a GET request to http://localhost:<port>/mine.
 
 To create a new transaction and append it to the next block to be forged, make a POST request to 
 http://localhost:<port>/transactions/new - with the body of the post containing a JSON like the example below:
  
  {
    "sender": "m4ee26xbc15148ee92c6cd394edd974a",
    "recipient": "someones-address",
    "amount": 3
  }
  
  After creating new transactions and mining a new block, you can evaluate the current state of your entire chain by making a
  GET request to http://localhost:<port>/chain.
  
  To add new network neighbouring nodes to your list of nodes your can simply run the server on another port 
  (runserver.py will look for an available port automatically) and make a POST request to http://localhost:<port>/nodes/register -
  with the body of the request containing a json like the example below:
  
  {
    "nodes": ["http://127.0.0.1:<port>"]
  }
  
  After that, you can mine new blocks on your added node and verify its authoritativeness by making a GET request to
  http://localhost:<port>/nodes/resolve which will resolve the current state of the chain by replacing it if a valid chain is found,
  whose length is greaters than ours.
  
  
