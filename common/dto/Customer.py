import pandera as pa
from pandera.typing import Series

from pydantic import BaseModel, Field, field_validator
from typing import List, Literal, Optional


class CustomerDTO(BaseModel):
    customerID: str = Field(..., alias="customerID")
    gender: Literal["Male", "Female"]
    SeniorCitizen: Literal[0, 1]
    Partner: Literal["Yes", "No"]
    Dependents: Literal["Yes", "No"]
    tenure: int
    PhoneService: Literal["Yes", "No"]
    MultipleLines: Literal["Yes", "No", "No phone service"]
    InternetService: Literal["DSL", "Fiber optic", "No"]
    OnlineSecurity: Literal["Yes", "No", "No internet service"]
    OnlineBackup: Literal["Yes", "No", "No internet service"]
    DeviceProtection: Literal["Yes", "No", "No internet service"]
    TechSupport: Literal["Yes", "No", "No internet service"]
    StreamingTV: Literal["Yes", "No", "No internet service"]
    StreamingMovies: Literal["Yes", "No", "No internet service"]
    Contract: Literal["Month-to-month", "One year", "Two year"]
    PaperlessBilling: Literal["Yes", "No"]
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: Optional[float]

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