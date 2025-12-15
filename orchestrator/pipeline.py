# orchestrator/pipeline.py
"""
TRUE Multi-Agent Orchestration System using LangGraph.
5 specialized agents + proper state machine.
GUARANTEES 15+ questions and 3 complete pages.
"""

import json
import re
from pathlib import Path
from typing_extensions import TypedDict

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage

from agents.parser_agent import ProductParserAgent
from agents.content_logic import ContentLogicBlocks

load_dotenv()


# ---------------------------------------------------------------------
# State Schema
# ---------------------------------------------------------------------
class AgentState(TypedDict, total=False):
    """State for multi-agent workflow.
    
    Using total=False makes all fields optional, which is required
    for LangGraph 0.2.58 when starting with empty state.
    """
    product_json: str
    questions: list
    faq_json: dict
    product_page_json: dict
    comparison_page_json: dict


# ---------------------------------------------------------------------
# Shared LLM with increased timeout
# ---------------------------------------------------------------------
try:
    llm = ChatOllama(
        model="llama3.1",
        temperature=0.7,
        streaming=False,
        timeout=120,  # Increased timeout for first request
        num_ctx=4096,  # Explicit context window
    )
    print("[INFO] ✓ Ollama LLM initialized successfully")
except Exception as e:
    print(f"[WARNING] Ollama initialization failed: {e}")
    print("[INFO] System will use deterministic fallback")
    llm = None


# ---------------------------------------------------------------------
# AGENT 1: Product Parser
# ---------------------------------------------------------------------
def product_parser_agent(state: AgentState) -> dict:
    """Parse product from input file."""
    print("[AGENT 1] Product Parser - Running...")
    
    parser = ProductParserAgent()
    product = parser.run()
    
    print(f"[AGENT 1] ✓ Parsed: {product.name}")
    return {"product_json": json.dumps(product.__dict__, ensure_ascii=False)}


# ---------------------------------------------------------------------
# AGENT 2: Question Generator (GUARANTEES 15+ questions)
# ---------------------------------------------------------------------
def question_generation_agent(state: AgentState) -> dict:
    """Generate exactly 15+ categorized questions."""
    print("[AGENT 2] Question Generator - Running...")
    
    product = json.loads(state["product_json"])
    
    # If LLM not available, use fallback immediately
    if llm is None:
        print("[AGENT 2] Using guaranteed fallback (LLM not configured)")
        questions = _generate_guaranteed_15_questions(product)
        return {"questions": questions}
    
    # Try LLM with improved prompt
    prompt = f"""You are a JSON generator. Generate EXACTLY 15 questions about this product.

Product Information:
- Name: {product['name']}
- Price: ₹{product['price']}
- Skin Types: {', '.join(product['skin_type'])}
- Ingredients: {', '.join(product['key_ingredients'])}

Generate 3 questions for EACH category (total 15):
- informational (3 questions)
- usage (3 questions)
- safety (3 questions)
- purchase (3 questions)
- comparison (3 questions)

CRITICAL: Return ONLY valid JSON array. No explanation, no markdown, no code fences.
Format:
[
  {{"category": "informational", "question": "What is this product?"}},
  {{"category": "usage", "question": "How do I apply it?"}},
  ... (15 total)
]

JSON array:"""

    try:
        print("[AGENT 2] Attempting LLM generation...")
        response = llm.invoke([HumanMessage(content=prompt)])
        content = response.content.strip()
        
        # Aggressive JSON extraction
        content = _extract_json_from_llm_response(content)
        
        questions = json.loads(content)
        
        # Validate we got enough questions
        if not isinstance(questions, list) or len(questions) < 15:
            raise ValueError(f"Got {len(questions) if isinstance(questions, list) else 0} questions, need 15+")
        
        print(f"[AGENT 2] ✓ Generated {len(questions)} questions via LLM")
        return {"questions": questions}
        
    except Exception as e:
        print(f"[AGENT 2] ⚠️ LLM failed ({type(e).__name__}: {str(e)[:100]})")
        print("[AGENT 2] Using guaranteed fallback")
        questions = _generate_guaranteed_15_questions(product)
        return {"questions": questions}


def _extract_json_from_llm_response(content: str) -> str:
    """Extract JSON from LLM response, handling markdown and extra text."""
    # Remove markdown code fences
    content = re.sub(r'```json\s*', '', content)
    content = re.sub(r'```\s*', '', content)
    
    # Find JSON array boundaries
    start = content.find('[')
    end = content.rfind(']')
    
    if start != -1 and end != -1 and end > start:
        content = content[start:end+1]
    
    return content.strip()


def _generate_guaranteed_15_questions(product: dict) -> list:
    """Fallback that GUARANTEES exactly 15 questions."""
    name = product['name']
    
    return [
        # Informational (3)
        {"category": "informational", "question": f"What is {name}?"},
        {"category": "informational", "question": f"What are the main benefits of {name}?"},
        {"category": "informational", "question": f"What ingredients are in {name}?"},
        
        # Usage (3)
        {"category": "usage", "question": f"How do I apply {name}?"},
        {"category": "usage", "question": f"When should I use {name}?"},
        {"category": "usage", "question": f"Can I use {name} with other products?"},
        
        # Safety (3)
        {"category": "safety", "question": f"Is {name} safe for sensitive skin?"},
        {"category": "safety", "question": f"Are there any side effects of {name}?"},
        {"category": "safety", "question": f"What precautions should I take with {name}?"},
        
        # Purchase (3)
        {"category": "purchase", "question": f"How much does {name} cost?"},
        {"category": "purchase", "question": f"Where can I buy {name}?"},
        {"category": "purchase", "question": f"Does {name} have a return policy?"},
        
        # Comparison (3)
        {"category": "comparison", "question": f"How does {name} compare to other vitamin C serums?"},
        {"category": "comparison", "question": f"Why should I choose {name} over alternatives?"},
        {"category": "comparison", "question": f"What makes {name} unique?"},
    ]


# ---------------------------------------------------------------------
# AGENT 3: FAQ Generator
# ---------------------------------------------------------------------
def faq_page_agent(state: AgentState) -> dict:
    """Generate FAQ page with answers."""
    print("[AGENT 3] FAQ Generator - Running...")
    
    product = json.loads(state["product_json"])
    questions = state["questions"]
    
    # Group by category
    categories = {}
    for q in questions:
        cat = q["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(q["question"])
    
    # Answer using ONLY product data
    faq_sections = []
    for category, qs in categories.items():
        items = []
        for question in qs:
            answer = _answer_from_product_data(question, product)
            items.append({"question": question, "answer": answer})
        
        faq_sections.append({"category": category, "items": items})
    
    faq_json = {
        "title": f"Frequently Asked Questions - {product['name']}",
        "product": product['name'],
        "total_questions": len(questions),
        "sections": faq_sections
    }
    
    print(f"[AGENT 3] ✓ Generated FAQ with {len(questions)} Q&As")
    return {"faq_json": faq_json}


def _answer_from_product_data(question: str, product: dict) -> str:
    """Answer using ONLY product data (no external knowledge)."""
    q_lower = question.lower()
    
    if "cost" in q_lower or "price" in q_lower or "much" in q_lower:
        return f"The product is priced at ₹{product['price']}."
    
    if "ingredient" in q_lower:
        return f"The key ingredients are: {', '.join(product['key_ingredients'])}."
    
    if "how" in q_lower and ("use" in q_lower or "apply" in q_lower):
        return product['how_to_use']
    
    if "when" in q_lower:
        return product['how_to_use']
    
    if "safe" in q_lower or "side effect" in q_lower or "precaution" in q_lower:
        return product['side_effects']
    
    if "benefit" in q_lower:
        return f"The main benefits include: {', '.join(product['benefits'])}."
    
    if "what is" in q_lower:
        return f"{product['name']} is a {product['concentration']} serum for {', '.join(product['skin_type'])} skin."
    
    if "skin type" in q_lower or "sensitive" in q_lower:
        return f"This product is suitable for {', '.join(product['skin_type'])} skin types."
    
    if "compare" in q_lower or "why choose" in q_lower or "unique" in q_lower:
        return f"{product['name']} offers {product['concentration']} with {', '.join(product['key_ingredients'])} at ₹{product['price']}."
    
    if "where" in q_lower and "buy" in q_lower:
        return "Available at select retailers."
    
    if "return" in q_lower or "refund" in q_lower:
        return "Please check with the retailer for return policy details."
    
    if "daily" in q_lower or "often" in q_lower:
        return product['how_to_use']
    
    return f"This information can be found in the product details for {product['name']}."


# ---------------------------------------------------------------------
# AGENT 4: Product Page Generator
# ---------------------------------------------------------------------
def product_page_agent(state: AgentState) -> dict:
    """Generate complete product description page."""
    print("[AGENT 4] Product Page Generator - Running...")
    
    product = json.loads(state["product_json"])
    logic = ContentLogicBlocks()
    
    product_page = {
        "page_type": "product_description",
        "product_name": product['name'],
        "headline": logic.generate_product_headline(product),
        "tagline": logic.generate_product_tagline(product),
        "hero_section": {
            "main_benefit": product['benefits'][0],
            "concentration": product['concentration'],
            "price": logic.generate_price_section(product)
        },
        "key_features": logic.generate_key_features(product),
        "ingredients": {
            "title": "Key Ingredients",
            "items": logic.generate_ingredients_section(product)
        },
        "how_to_use": logic.generate_usage_instructions(product),
        "safety_information": logic.generate_safety_info(product),
        "who_is_it_for": {
            "skin_types": product['skin_type'],
            "concerns": product['benefits']
        }
    }
    
    print("[AGENT 4] ✓ Generated product page")
    return {"product_page_json": product_page}


# ---------------------------------------------------------------------
# AGENT 5: Comparison Page Generator
# ---------------------------------------------------------------------
def comparison_page_agent(state: AgentState) -> dict:
    """Generate comparison page with fictional Product B."""
    print("[AGENT 5] Comparison Page Generator - Running...")
    
    product_a = json.loads(state["product_json"])
    
    # Load fictional Product B
    product_b_file = Path("data/product_b.json")
    if not product_b_file.exists():
        raise FileNotFoundError(
            f"Product B file not found: {product_b_file}\n"
            f"Please ensure data/product_b.json exists."
        )
    
    product_b = json.loads(product_b_file.read_text(encoding="utf-8"))
    
    logic = ContentLogicBlocks()
    
    comparison_page = {
        "page_type": "product_comparison",
        "title": f"{product_a['name']} vs {product_b['name']}",
        "subtitle": "Comprehensive comparison to help you choose",
        "products": {
            "product_a": {
                "name": product_a['name'],
                "summary": logic.generate_product_tagline(product_a),
                "price": f"₹{product_a['price']}"
            },
            "product_b": {
                "name": product_b['name'],
                "summary": logic.generate_product_tagline(product_b),
                "price": f"₹{product_b['price']}"
            }
        },
        "comparison_table": logic.generate_comparison_points(product_a, product_b),
        "recommendation": {
            "best_for_budget": product_a['name'] if product_a['price'] < product_b['price'] else product_b['name'],
            "best_for_oily_skin": product_a['name'],
            "best_for_dry_skin": product_b['name']
        }
    }
    
    print("[AGENT 5] ✓ Generated comparison page")
    return {"comparison_page_json": comparison_page}


# ---------------------------------------------------------------------
# Output Writer
# ---------------------------------------------------------------------
def write_outputs(state: AgentState) -> dict:
    """Write all JSON outputs to files."""
    print("[OUTPUT] Writing files...")
    
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Write FAQ
    (output_dir / "faq.json").write_text(
        json.dumps(state["faq_json"], indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    # Write Product Page
    (output_dir / "product_page.json").write_text(
        json.dumps(state["product_page_json"], indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    # Write Comparison Page
    (output_dir / "comparison_page.json").write_text(
        json.dumps(state["comparison_page_json"], indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    
    print("[OUTPUT] ✓ Successfully wrote:")
    print("  → output/faq.json")
    print("  → output/product_page.json")
    print("  → output/comparison_page.json")
    
    return {}


# ---------------------------------------------------------------------
# Workflow Builder Function
# ---------------------------------------------------------------------
def create_workflow():
    """Create and compile the LangGraph workflow.
    
    Returns:
        Compiled LangGraph application
    """
    workflow = StateGraph(AgentState)
    
    # Add all agent nodes
    workflow.add_node("agent_1_parser", product_parser_agent)
    workflow.add_node("agent_2_questions", question_generation_agent)
    workflow.add_node("agent_3_faq", faq_page_agent)
    workflow.add_node("agent_4_product", product_page_agent)
    workflow.add_node("agent_5_comparison", comparison_page_agent)
    workflow.add_node("write_outputs", write_outputs)
    
    # Define linear workflow edges
    workflow.add_edge(START, "agent_1_parser")
    workflow.add_edge("agent_1_parser", "agent_2_questions")
    workflow.add_edge("agent_2_questions", "agent_3_faq")
    workflow.add_edge("agent_3_faq", "agent_4_product")
    workflow.add_edge("agent_4_product", "agent_5_comparison")
    workflow.add_edge("agent_5_comparison", "write_outputs")
    workflow.add_edge("write_outputs", END)
    
    return workflow.compile()


# ---------------------------------------------------------------------
# Orchestrator Entry Point
# ---------------------------------------------------------------------
class PipelineOrchestrator:
    """Multi-agent content generation orchestrator."""
    
    def __init__(self):
        """Initialize the orchestrator with compiled workflow."""
        self.app = create_workflow()
    
    def run(self):
        """Execute the complete multi-agent workflow.
        
        Returns:
            dict: Final state containing all generated content
        """
        print("=" * 70)
        print("🚀 MULTI-AGENT CONTENT GENERATION SYSTEM")
        print("=" * 70)
        
        try:
            result = self.app.invoke({}, config={"recursion_limit": 50})
            
            print("=" * 70)
            print("✅ PIPELINE COMPLETED SUCCESSFULLY")
            print("=" * 70)
            
            if "questions" in result:
                print(f"📊 Total Questions Generated: {len(result['questions'])} (Required: ≥15)")
            
            return result
            
        except Exception as e:
            print("=" * 70)
            print("❌ PIPELINE FAILED")
            print("=" * 70)
            print(f"Error: {e}")
            raise