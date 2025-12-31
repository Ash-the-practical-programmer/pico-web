import re
from typing import Dict, Any, List, Optional

class InstructionParser:
    """
    Parse natural language instructions into processing operations
    
    Uses pattern matching and keyword extraction (can be enhanced with LLM)
    """
    
    OPERATION_PATTERNS = {
        # Augmentation
        "augment": {
            "keywords": ["augment", "variations", "transform", "modify", "generate variations"],
            "operations": ["rotation", "flip", "brightness", "contrast", "crop", "blur"]
        },
        
        # Pairing
        "pair": {
            "keywords": ["pair", "pairs", "similar", "different", "match", "compare"],
            "operations": ["similarity_pairs", "difference_pairs", "temporal_pairs"]
        },
        
        # Filtering
        "filter": {
            "keywords": ["filter", "remove", "keep only", "exclude", "quality"],
            "operations": ["blur_filter", "size_filter", "quality_filter", "duplicate_filter"]
        },
        
        # Generation
        "generate": {
            "keywords": ["generate", "create", "synthetic", "puzzle", "pattern"],
            "operations": ["synthetic_generation", "puzzle_generation", "pattern_generation"]
        },
        
        # Expansion
        "expand": {
            "keywords": ["expand", "multiply", "10x", "increase", "scale up"],
            "operations": ["dataset_expansion"]
        }
    }
    
    def parse(self, instructions: str, output_count: Optional[int] = None) -> Dict[str, Any]:
        """
        Parse natural language instructions
        
        Returns:
            {
                "intent": "augment",  # Primary intent
                "operations": [...],   # List of operations to perform
                "parameters": {...},   # Extracted parameters
                "estimated_output_count": 10000
            }
        """
        
        instructions_lower = instructions.lower()
        
        # Detect primary intent
        intent = self._detect_intent(instructions_lower)
        
        # Extract operations
        operations = self._extract_operations(instructions_lower, intent)
        
        # Extract parameters
        parameters = self._extract_parameters(instructions_lower)
        
        # Estimate output count
        estimated_count = output_count or self._estimate_output_count(
            instructions_lower, 
            parameters
        )
        
        return {
            "intent": intent,
            "operations": operations,
            "parameters": parameters,
            "estimated_output_count": estimated_count
        }
    
    def _detect_intent(self, text: str) -> str:
        """Detect primary processing intent"""
        
        scores = {}
        for intent, config in self.OPERATION_PATTERNS.items():
            score = sum(1 for keyword in config["keywords"] if keyword in text)
            scores[intent] = score
        
        # Return intent with highest score
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "augment"
    
    def _extract_operations(self, text: str, intent: str) -> List[str]:
        """Extract specific operations mentioned in instructions"""
        
        operations = []
        
        # Augmentation operations
        if "rotat" in text:
            operations.append("rotation")
        if "flip" in text or "mirror" in text:
            operations.append("flip")
        if "bright" in text:
            operations.append("brightness")
        if "contrast" in text:
            operations.append("contrast")
        if "crop" in text:
            operations.append("crop")
        if "color" in text or "hue" in text:
            operations.append("color_jitter")
        
        # Filtering operations
        if "blur" in text and "filter" in text:
            operations.append("blur_filter")
        if "quality" in text:
            operations.append("quality_filter")
        
        # Pairing operations
        if "similar" in text:
            operations.append("similarity_pairs")
        if "different" in text or "spot-the-difference" in text:
            operations.append("difference_pairs")
        
        # Default operations based on intent
        if not operations:
            operations = self.OPERATION_PATTERNS[intent]["operations"][:3]
        
        return operations
    
    def _extract_parameters(self, text: str) -> Dict[str, Any]:
        """Extract numeric parameters from instructions"""
        
        params = {}
        
        # Extract rotation range
        rotation_match = re.search(r'rotat.*?(-?\d+).*?(-?\d+)', text)
        if rotation_match:
            params["rotation_range"] = [int(rotation_match.group(1)), int(rotation_match.group(2))]
        else:
            params["rotation_range"] = [-30, 30]  # Default
        
        # Extract brightness range
        if "brightness" in text:
            params["brightness_range"] = [0.7, 1.3]  # Default
        
        # Extract difficulty (for puzzles)
        if "easy" in text:
            params["difficulty"] = "easy"
        elif "hard" in text:
            params["difficulty"] = "hard"
        else:
            params["difficulty"] = "medium"
        
        # Extract expansion factor
        expansion_match = re.search(r'(\d+)x', text)
        if expansion_match:
            params["expansion_factor"] = int(expansion_match.group(1))
        
        return params
    
    def _estimate_output_count(self, text: str, parameters: Dict) -> int:
        """Estimate desired output count from instructions"""
        
        # Look for explicit numbers
        count_match = re.search(r'(\d{1,3}(?:,\d{3})*|\d+)\s*(?:samples?|images?|variations?|outputs?)', text)
        if count_match:
            count_str = count_match.group(1).replace(',', '')
            return int(count_str)
        
        # Look for expansion factor
        if "expansion_factor" in parameters:
            return 1000 * parameters["expansion_factor"]  # Assume 1k input
        
        # Look for keywords
        if "10x" in text or "ten times" in text:
            return 10000
        if "100x" in text:
            return 100000
        
        # Default
        return 10000
