from langchain_core.tools import tool
from pydantic import BaseModel, Field


# 1. Define custom input schema to use validation and get full control
class DiscountInput(BaseModel):
    price: float = Field(description="Original product price", gt=0)

    discount: float = Field(
        description="Discount percentage between 0 and 100", ge=0, le=100
    )


# 2. Create tool using custom schema (pydantic schema)
# here we validate the input to our tool so that to get the desired  arguments
@tool(args_schema=DiscountInput)
def calculate_discount(price: float, discount: float) -> float:
    """Calculate the final price after applying a discount."""

    final_price = price - (price * discount / 100)

    return round(final_price, 2)


# 3. Inspect schema
# print(calculate_discount.args)


# 4. Execute tool
result = calculate_discount.invoke({"price": 2000, "discount": 15})

print("Final Price:", result)
