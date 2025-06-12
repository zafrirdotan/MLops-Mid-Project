import math
import pandera as pa
from pandera.typing import Series

from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional


class CustomerDTO(BaseModel):
    customerID: Optional[str] = Field(None, alias="customerID")
    gender: Optional[Literal["Male", "Female"]] = None
    SeniorCitizen: Optional[Literal[0, 1]] = None
    Partner: Optional[Literal["Yes", "No"]] = None
    Dependents: Optional[Literal["Yes", "No"]] = None
    tenure: Optional[int] = None
    PhoneService: Optional[Literal["Yes", "No"]] = None
    MultipleLines: Optional[Literal["Yes", "No", "No phone service"]] = None
    InternetService: Optional[Literal["DSL", "Fiber optic", "No"]] = None
    OnlineSecurity: Optional[Literal["Yes", "No", "No internet service"]] = None
    OnlineBackup: Optional[Literal["Yes", "No", "No internet service"]] = None
    DeviceProtection: Optional[Literal["Yes", "No", "No internet service"]] = None
    TechSupport: Optional[Literal["Yes", "No", "No internet service"]] = None
    StreamingTV: Optional[Literal["Yes", "No", "No internet service"]] = None
    StreamingMovies: Optional[Literal["Yes", "No", "No internet service"]] = None
    Contract: Optional[Literal["Month-to-month", "One year", "Two year"]] = None
    PaperlessBilling: Optional[Literal["Yes", "No"]] = None
    PaymentMethod: Optional[str] = None
    MonthlyCharges: Optional[float] = None
    TotalCharges: Optional[float] = None



    @field_validator("*", mode="before")
    @classmethod
    def replace_nan_with_none(cls, v):
        if isinstance(v, float) and math.isnan(v):
            return None
        return v
    
    @field_validator("TotalCharges", mode="before")
    @classmethod
    def parse_total_charges(cls, v):
        # Replace spaces or 'nan' with '2279', then try to convert to float
        if v is None:
            return 2279.0
        if isinstance(v, str):
            v = v.replace(' ', '2279')
            if v == 'nan':
                return 2279.0
        try:
            return float(v)
        except (TypeError, ValueError):
            return 2279.0


class CustomerListDTO(BaseModel):
    customers: List[CustomerDTO]


# Create a pandera schema from your Pydantic model
class CustomerSchema(pa.DataFrameModel):
    customerID: Series[str]
    gender: Series[str]
    SeniorCitizen: Series[int]
    Partner: Series[str]
    Dependents: Series[str]
    tenure: Series[int]
    PhoneService: Series[str]
    MultipleLines: Series[str]
    InternetService: Series[str]
    OnlineSecurity: Series[str]
    OnlineBackup: Series[str]
    DeviceProtection: Series[str]
    TechSupport: Series[str]
    StreamingTV: Series[str]
    StreamingMovies: Series[str]
    Contract: Series[str]
    PaperlessBilling: Series[str]
    PaymentMethod: Series[str]
    MonthlyCharges: Series[float]
    TotalCharges: Series[float]