"""
AI-powered model suggestion service for vendors.

This module provides functionality to suggest building models for a vendor
based on their website and company information using AI.
"""

import anthropic
import os
from typing import List, Dict
import json


class ModelSuggestionService:
    """Service for generating AI-powered model suggestions for vendors."""
    
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
    
    def suggest_models(self, vendor_name: str, website_url: str) -> List[Dict]:
        """
        Generate model suggestions for a vendor based on their name and website.
        
        Args:
            vendor_name: Name of the vendor/company
            website_url: URL of the vendor's website
            
        Returns:
            List of suggested models with details
        """
        prompt = f"""You are an expert in sustainable and regenerative building technologies. 
        
A building systems vendor named "{vendor_name}" with website {website_url} needs to have their product models catalogued.

Based on the vendor name and typical products from companies in this space, suggest 3-5 specific building models/products they likely offer.

For each model, provide:
1. model_name: Specific product name (e.g., "24ft Geodesic Dome", "Modular Studio Unit")
2. description: 2-3 sentence description of the model
3. price_range: Estimated price range (e.g., "$50k-$100k", "$200k-$500k")
4. specifications: Key technical specs as a JSON object (e.g., {{"size": "24ft diameter", "capacity": "4-6 people", "materials": "sustainable timber"}})

Return ONLY a valid JSON array of models, no other text. Format:
[
  {{
    "model_name": "...",
    "description": "...",
    "price_range": "...",
    "specifications": {{...}}
  }}
]"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract JSON from response
            response_text = message.content[0].text.strip()
            
            # Remove markdown code fences if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])
            
            models = json.loads(response_text)
            return models
            
        except Exception as e:
            print(f"Error generating model suggestions: {e}")
            return []
    
    def suggest_models_from_context(self, vendor_name: str, website_url: str, additional_context: str = "") -> List[Dict]:
        """
        Generate model suggestions with additional context.
        
        Args:
            vendor_name: Name of the vendor/company
            website_url: URL of the vendor's website
            additional_context: Additional information about the vendor
            
        Returns:
            List of suggested models with details
        """
        prompt = f"""You are an expert in sustainable and regenerative building technologies. 
        
A building systems vendor named "{vendor_name}" with website {website_url} needs to have their product models catalogued.

Additional context: {additional_context}

Based on this information, suggest 3-5 specific building models/products they offer.

For each model, provide:
1. model_name: Specific product name
2. description: 2-3 sentence description
3. price_range: Estimated price range
4. specifications: Key technical specs as JSON object

Return ONLY a valid JSON array of models, no other text. Format:
[
  {{
    "model_name": "...",
    "description": "...",
    "price_range": "...",
    "specifications": {{...}}
  }}
]"""

        try:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = message.content[0].text.strip()
            
            # Remove markdown code fences if present
            if response_text.startswith("```"):
                lines = response_text.split("\n")
                response_text = "\n".join(lines[1:-1])
            
            models = json.loads(response_text)
            return models
            
        except Exception as e:
            print(f"Error generating model suggestions: {e}")
            return []
