# My Pizza restaurant

* Welcome to my pizza app.
* This app simulating pizza restaurant that has a specific workflow:
    * Fist, the order is receives, the app assign the order id if it doesn't supply.
    * Then the dough chef making the perfect dough for the pizza. (with sugar spice and every day nice)
    * when the dough is ready, toppings chef work had to put toppings on the pizza.
    * After the toppings is sets, its time to cook, the oven run in action.
    * bling, bling! pizza is ready and the waiters need to serve it ASAP.
* each phase takes a different amount of time:
    * dough - 7 seconds
    * toppings - 4 seconds for each topping
    * oven - 10 seconds
    * waiter serves - 5 seconds
* restaurant has a limited resources
    * 2 Dough chefs
    * 3 Toppings chef (that each can place 2 toppings)
    * 1 Oven
    * 2 Waiters
* each pizza order produces reports of its time of preparation.
* each bulk of orders produces report of the total time of the pizzas preparation.
* report is save on database.

## General design

* the app uses `asyncio` python build in module.
* the application uses producer/consumer pattern to process the orders.
* each of the restaurants employee's role has a queue/s, the queue/s is for consuming orders and producing orders to the
  next phase.
* there are certain roles in the system, for example:
    * *bulk_producer* - which produce all of the incoming orders in bulk
    * *dough_chef_consumer* - the fist step, consumes pizza and make its work
    * *dough_chef_producer* - after it done produce the next step (which is topping chef)

## How To Run

### *python main.py* with pre-defined data samples:

* read the following and pass to "execute" section
* make sure to un-comment the two last lines in `main.py` file

```python
    from data_samples import order_doc

restaurant.post_orders(order_doc)
```

* make sure to comment the following line in `main.py` file

```python
  # app.run(host="0.0.0.0", port=5000, debug=True)
```

### Run with API call

* read the following and pass to "execute" section
* make sure to un-comment the two last lines in `main.py` file

```python
# from data_samples import order_doc
# restaurant.post_orders(order_doc)
```

* make sure to comment the following line in `main.py` file

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

* open your favorite HTTP requester like: postman/curl etc...
* make a *POST* request to http://localhost:5000/api/pizza/order
* body should look like:

```json
{
  "orders": [
    {
      "id": 123,
      "toppings": [
        "tuna",
        "olives"
      ]
    },
    {
      "toppings": [
        "tuna",
        "green olives",
        "black olives",
        "extra cheese",
        "mushrooms"
      ]
    },
    {
      "id": 456,
      "toppings": []
    }
  ]
}
```

#### **Notes about the body**

* there is not any validation to requests body, **make sure to send data correctly to avoid 500 error**
* the `id` field is **not required**
* the `toppings` field is **required** but can be empty list.

### execute

* Look for the file `docker-compose.yml` that is located in the root directory of the repository.
* Open the `yaml` file and check if your port is not already allocated to other applications
    * If so, you need to change port or close running apps on this port.
* Run the command `docker-compose up -d` - the app will start run immediately.
* To be able to see the logs run `docker logs pizza_assignment-pizza-app-1`

### Inspect data in MongoDB container

* Connect to docker bash - run `docker exec -it pizza_assignment-mongodb-1 bash`
* Once inside the container, start the MongoDB shell by running the mongo command: `mongosh`
* switch to use `pizza_app` context run `use pizza_app`
* To view the data in a specific collection, you can use the `db.pizza_reports.find().pretty()` command.
* There you go :)

### Terminating

* Run `docker-compose down` in root directory of the repository