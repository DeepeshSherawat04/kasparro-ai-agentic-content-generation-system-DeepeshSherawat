# agents/content_logic.py
"""
Reusable content logic blocks for template-based generation.
These functions transform product data into structured content.
"""

from typing import Dict, Any, List


class ContentLogicBlocks:
    """Reusable content generation logic blocks."""
    
    @staticmethod
    def generate_product_headline(product: Dict[str, Any]) -> str:
        """Generate attention-grabbing headline."""
        name = product.get('name', 'Product')
        benefit = product.get('benefits', [''])[0] if product.get('benefits') else 'Premium skincare'
        return f"{name} – Your Solution for {benefit}"
    
    @staticmethod
    def generate_product_tagline(product: Dict[str, Any]) -> str:
        """Generate short tagline."""
        concentration = product.get('concentration', '')
        benefit = product.get('benefits', ['beautiful skin'])[0]
        return f"{concentration} formula for {benefit.lower()}"
    
    @staticmethod
    def generate_key_features(product: Dict[str, Any]) -> List[str]:
        """Extract and format key features."""
        features = []
        
        if product.get('concentration'):
            features.append(f"Potent {product['concentration']} formula")
        
        if product.get('key_ingredients'):
            features.append(f"Enriched with {', '.join(product['key_ingredients'])}")
        
        if product.get('skin_type'):
            features.append(f"Perfect for {', '.join(product['skin_type'])} skin")
        
        if product.get('benefits'):
            for benefit in product['benefits']:
                features.append(f"Helps with {benefit.lower()}")
        
        return features
    
    @staticmethod
    def generate_ingredients_section(product: Dict[str, Any]) -> Dict[str, str]:
        """Format ingredients with descriptions (ONLY from product data)."""
        ingredients = {}
        for ing in product.get('key_ingredients', []):
            # Only use info that can be inferred from product data
            ingredients[ing] = f"Active ingredient in {product.get('name', 'this product')}"
        return ingredients
    
    @staticmethod
    def generate_usage_instructions(product: Dict[str, Any]) -> Dict[str, Any]:
        """Structure usage instructions."""
        return {
            "application": product.get('how_to_use', 'Apply as directed'),
            "timing": "As indicated in product instructions"
        }
    
    @staticmethod
    def generate_safety_info(product: Dict[str, Any]) -> Dict[str, Any]:
        """Format safety information."""
        return {
            "suitable_for": product.get('skin_type', []),
            "warnings": [product.get('side_effects', 'Consult dermatologist if irritation occurs')]
        }
    
    @staticmethod
    def generate_price_section(product: Dict[str, Any]) -> Dict[str, Any]:
        """Format pricing information."""
        price = product.get('price', 0)
        return {
            "price": f"₹{price}",
            "currency": "INR"
        }
    
    @staticmethod
    def generate_comparison_points(product_a: Dict[str, Any], product_b: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate structured comparison points."""
        comparison = []
        
        # Price comparison
        comparison.append({
            "aspect": "Price",
            "product_a": f"₹{product_a.get('price', 0)}",
            "product_b": f"₹{product_b.get('price', 0)}",
            "winner": "product_a" if product_a.get('price', 999999) < product_b.get('price', 999999) else "product_b"
        })
        
        # Concentration comparison
        comparison.append({
            "aspect": "Concentration",
            "product_a": product_a.get('concentration', 'N/A'),
            "product_b": product_b.get('concentration', 'N/A'),
            "winner": "equal"
        })
        
        # Ingredients comparison
        comparison.append({
            "aspect": "Key Ingredients",
            "product_a": ', '.join(product_a.get('key_ingredients', [])),
            "product_b": ', '.join(product_b.get('key_ingredients', [])),
            "winner": "equal"
        })
        
        # Skin type compatibility
        comparison.append({
            "aspect": "Skin Type Compatibility",
            "product_a": ', '.join(product_a.get('skin_type', [])),
            "product_b": ', '.join(product_b.get('skin_type', [])),
            "winner": "product_a" if len(product_a.get('skin_type', [])) >= len(product_b.get('skin_type', [])) else "product_b"
        })
        
        return comparison