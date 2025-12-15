# agents/langchain_tools.py
"""
Properly defined LangChain tools using @tool decorator.
Required for create_agent compatibility.
"""
import json
from pathlib import Path
from langchain_core.tools import tool


@tool
def read_product_data() -> dict:
    """Read the product input data from the JSON file.
    
    Returns:
        dict: Product information including name, ingredients, price, etc.
    """
    file_path = Path("data/product_input.json")
    if not file_path.exists():
        raise FileNotFoundError(f"Product data not found at {file_path}")
    
    return json.loads(file_path.read_text(encoding="utf-8"))


@tool
def get_product_price(product_name: str) -> str:
    """Get the price of a product.
    
    Args:
        product_name: Name of the product
        
    Returns:
        str: Price information
    """
    data = read_product_data.invoke({})
    return f"₹{data.get('price', 'N/A')}"


@tool
def get_product_ingredients(product_name: str) -> list:
    """Get the key ingredients of a product.
    
    Args:
        product_name: Name of the product
        
    Returns:
        list: List of key ingredients
    """
    data = read_product_data.invoke({})
    return data.get('key_ingredients', [])


@tool
def get_usage_instructions(product_name: str) -> str:
    """Get how to use the product.
    
    Args:
        product_name: Name of the product
        
    Returns:
        str: Usage instructions
    """
    data = read_product_data.invoke({})
    return data.get('how_to_use', 'No instructions available')


@tool
def get_safety_information(product_name: str) -> str:
    """Get safety and side effect information.
    
    Args:
        product_name: Name of the product
        
    Returns:
        str: Safety information and potential side effects
    """
    data = read_product_data.invoke({})
    return data.get('side_effects', 'No safety information available')


# Export all tools
TOOLS = [
    read_product_data,
    get_product_price,
    get_product_ingredients,
    get_usage_instructions,
    get_safety_information,
]