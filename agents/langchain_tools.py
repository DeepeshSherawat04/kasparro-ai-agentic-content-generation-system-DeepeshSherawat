"""
Deterministic tools for LangChain 1.1.3 ReAct Agent.
All tools must be simple Python callables that return strings.
"""

import json
from pathlib import Path
from types import SimpleNamespace

# deterministic block builders
from blocks.product_blocks import (
    build_overview_block,
    build_ingredients_block,
    build_safety_block,
    build_pricing_block,
)
from blocks.usage_blocks import build_usage_block
from blocks.benefits_blocks import build_benefits_block
from blocks.comparison_blocks import (
    create_product_b_block,
    compare_ingredients_block,
    build_comparison_summary_block,
)


# ----------------------------------------------------------------------
# READ PRODUCT
# ----------------------------------------------------------------------
def read_product(_: str) -> str:
    """
    Read data/product_input.json and return its contents as JSON string.
    """
    path = Path("data/product_input.json")
    return path.read_text(encoding="utf-8")


# ----------------------------------------------------------------------
# OVERVIEW
# ----------------------------------------------------------------------
def build_overview(product_json: str) -> str:
    """
    Build overview section from deterministic block.
    """
    data = json.loads(product_json)
    ns = SimpleNamespace(**data)
    block = build_overview_block(ns)
    return json.dumps(block, ensure_ascii=False)


# ----------------------------------------------------------------------
# INGREDIENTS
# ----------------------------------------------------------------------
def build_ingredients(product_json: str) -> str:
    """
    Build ingredient section.
    """
    data = json.loads(product_json)
    ns = SimpleNamespace(**data)
    block = build_ingredients_block(ns)
    return json.dumps(block, ensure_ascii=False)


# ----------------------------------------------------------------------
# USAGE
# ----------------------------------------------------------------------
def build_usage(product_json: str) -> str:
    """
    Build usage instructions.
    """
    data = json.loads(product_json)
    ns = SimpleNamespace(**data)
    block = build_usage_block(ns)
    return json.dumps(block, ensure_ascii=False)


# ----------------------------------------------------------------------
# BENEFITS
# ----------------------------------------------------------------------
def build_benefits(product_json: str) -> str:
    """
    Build product benefits section.
    """
    data = json.loads(product_json)
    ns = SimpleNamespace(**data)
    block = build_benefits_block(ns)
    return json.dumps(block, ensure_ascii=False)


# ----------------------------------------------------------------------
# SAFETY
# ----------------------------------------------------------------------
def build_safety(product_json: str) -> str:
    """
    Build safety + precautions section.
    """
    data = json.loads(product_json)
    ns = SimpleNamespace(**data)
    block = build_safety_block(ns)
    return json.dumps(block, ensure_ascii=False)


# ----------------------------------------------------------------------
# PRICING
# ----------------------------------------------------------------------
def build_pricing(product_json: str) -> str:
    """
    Build pricing section.
    """
    data = json.loads(product_json)
    ns = SimpleNamespace(**data)
    block = build_pricing_block(ns)
    return json.dumps(block, ensure_ascii=False)


# ----------------------------------------------------------------------
# PRODUCT COMPARISON
# ----------------------------------------------------------------------
def compare_products(product_json: str) -> str:
    """
    Compare Product A (input) vs generated Product B.
    Returns JSON: {product_b, ingredient_comparison, summary}
    """
    data = json.loads(product_json)
    ns = SimpleNamespace(**data)

    product_b = create_product_b_block()
    ing_cmp = compare_ingredients_block(ns, product_b)
    summary = build_comparison_summary_block(ns, product_b, ing_cmp)

    out = {
        "product_b": product_b.__dict__,
        "ingredient_comparison": ing_cmp,
        "summary": summary,
    }
    return json.dumps(out, ensure_ascii=False)


# ----------------------------------------------------------------------
# EXPORT TOOL LIST
# ----------------------------------------------------------------------
TOOLS = [
    read_product,
    build_overview,
    build_ingredients,
    build_usage,
    build_benefits,
    build_safety,
    build_pricing,
    compare_products,
]
