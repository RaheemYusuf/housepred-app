"""
This module defines the database models using duckdb.

It includes model classes for different types of real estate,
specifically rental apartments. The module uses a function to
map Python classes to database tables. The structure and fileds
of the RentApartments class are configured to match the corresponding
database for rental apartments.
"""

from dataclasses import dataclass, fields


@dataclass
class PropertyData:
    """
    Python model class for rental apartments.

    Attributes:
        address (str): The address of the apartment, primary key.
        area (float): The area of the apartment in square meters.
        constraction_year (int): The year the apartment was constructed.
        rooms (int): The number of rooms in the apartment.
        bedrooms (int): The number of bedrooms in the apartment.
        balcony (str): Information about the balcony.
        storage (str): Information about storage space.
        parking (str): Information about parking availability.
        furnished (str): Indicates if the apartment is furnished.
        garage (str): Information about the garage.
        garden (str): Information about the garden.
        energy (str): Energy efficiency rating.
        facilities (str): Other facilities available.
        zip (str): ZIP code of the apartment's location.
        neighborhood (str): Neighorhood where the apartment is located.
        rent (int): Monthly rent price.
    """

    address: str
    area: float
    constraction_year: int
    rooms: int
    bedrooms: int
    balcony: str
    storage: str
    parking: str
    furnished: str
    garage: str
    garden: str
    energy: str
    facilities: str
    zip: str
    neighborhood: str
    rent: int



# A reusable helper to translate Python types to DuckDB SQL types
def get_duckdb_schema(model_class) -> dict:
    type_map = {
        int: "BIGINT", float: "DOUBLE", bool: "BOOLEAN", str: "VARCHAR"
    }
    return {
        field.name: type_map.get(field.type, "VARCHAR")
        for field in fields(model_class)
    }
