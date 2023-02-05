import datetime
from dataclasses import dataclass
from datetime import timedelta


@dataclass
class SinglePizzaReport:
    id: str
    total_preparation_time: timedelta


@dataclass
class OrderReport:
    id: str
    saved_at: datetime.datetime
    total_preparation_time: timedelta
    pizzas_in_order: list[SinglePizzaReport]