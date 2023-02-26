from dataclasses import dataclass, asdict

@dataclass
class ProductItem():
    """
    Product in daily deals.
    """
    name: str
    price: float
    emission: float

