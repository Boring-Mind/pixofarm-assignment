from typing import Union

from pydantic import BaseModel


class CreateCityIn(BaseModel):
    """Contains all input fields for create_city endpoint."""

    name: str
    latitude: float
    longitude: float
    altitude: float
    continent: Union[int, str]
    # ToDo: replace the Union[int, str] with int | str when pydantic will support this
