from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class PizzaInOrder:
    class OrderState(Enum):
        INCOMING_ORDER = 0
        DOUGH_CHEF = 1
        TOPPING_CHEF = 2
        OVEN = 3
        WAITER = 4
        COMPLETED = 5

    toppings: list[str]
    id: Optional[str] = None
    start_time_total: Optional[float] = None
    end_time_total: Optional[float] = None
    start_time_dough: Optional[float] = None
    end_time_dough: Optional[float] = None
    start_time_toppings: Optional[float] = None
    end_time_toppings: Optional[float] = None
    start_time_oven: Optional[float] = None
    end_time_oven: Optional[float] = None
    start_time_serve: Optional[float] = None
    end_time_serve: Optional[float] = None
    state: OrderState = OrderState(0)

    def move_to_next_step(self):
        self.state = PizzaInOrder.OrderState(self.state.value + 1)

    def assign_timestamp(self, start_time_snapshot, end_time_snapshot):
        start_time_snapshot = start_time_snapshot.timestamp
        end_time_snapshot = end_time_snapshot.timestamp
        if self.state == PizzaInOrder.OrderState.DOUGH_CHEF:
            self.start_time_dough = start_time_snapshot
            self.end_time_dough = end_time_snapshot
        elif self.state == PizzaInOrder.OrderState.TOPPING_CHEF:
            self.start_time_toppings = start_time_snapshot
            self.end_time_toppings = end_time_snapshot
        elif self.state == PizzaInOrder.OrderState.OVEN:
            self.start_time_oven = start_time_snapshot
            self.end_time_oven = end_time_snapshot
        elif self.state == PizzaInOrder.OrderState.WAITER:
            self.start_time_serve = start_time_snapshot
            self.end_time_serve = end_time_snapshot
        elif self.state == PizzaInOrder.OrderState.COMPLETED:
            self.start_time_total = start_time_snapshot
            self.end_time_total = end_time_snapshot
        # if self.state == Order.OrderState.INCOMING_ORDER:
        #     self.start_time_total = start_time_snapshot


@dataclass
class Orders:
    id: str
    pizzas_in_order: list[PizzaInOrder]
    start_preparation_time: Optional[float] = None
    end_preparation_time: Optional[float] = None
