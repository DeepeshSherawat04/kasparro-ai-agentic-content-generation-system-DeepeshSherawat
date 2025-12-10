"""
Data classes that describe the structure of the FAQ page.
Sections contain items, and each item is just a question + answer pair.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class FAQItem:
    question: str
    answer: str


@dataclass
class FAQSection:
    category_name: str
    items: List[FAQItem]


@dataclass
class FAQPageTemplate:
    title: str
    sections: List[FAQSection]
