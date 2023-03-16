from dataclasses import dataclass, asdict

@dataclass
class ProductItem():
    """
    Product in daily deals.
    """
    name: str
    price: float
    category: str
    weight: str
    emission: float
    compensation_price: float

