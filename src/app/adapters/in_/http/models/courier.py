from pydantic import BaseModel, Field

from src.app.adapters.in_.http.models.location import LocationDTO


class CourierDTO(BaseModel):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    Courier - a model defined in OpenAPI

        id: The id of this Courier.
        name: The name of this Courier.
        location: The location of this Courier.
    """

    id: str = Field(alias="id")
    name: str = Field(alias="name")
    location: LocationDTO = Field(alias="location")
