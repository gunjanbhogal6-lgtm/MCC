"""
LLM client for n8n webhook integration
"""

import json
import time
import urllib3
from typing import Any, Dict, List, Optional, Union

import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class LLMClient:
    """Client for interacting with n8n webhook LLM endpoint"""
    
    def __init__(
        self,
        endpoint: str,
        timeout: int = 120,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        batch_size: int = 30
    ):
        self.endpoint = endpoint
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.batch_size = batch_size
        self.headers = {"Content-Type": "application/json"}
    
    def _make_request(
        self,
        message: str,
        system_prompt: str,
        attempt: int = 0
    ) -> Optional[Dict]:
        """Make a single request to the LLM endpoint"""
        payload = {
            "message": message,
            "systemPrompt": system_prompt
        }
        
        try:
            response = requests.post(
                self.endpoint,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
                verify=False
            )
            
            if response.status_code >= 400:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "response": None
                }
            
            data = response.json()
            
            output_text = None
            if isinstance(data, list) and len(data) > 0:
                if isinstance(data[0], dict) and "output" in data[0]:
                    output_text = data[0]["output"]
            elif isinstance(data, dict) and "output" in data:
                output_text = data["output"]
            
            return {
                "success": True,
                "error": None,
                "response": output_text
            }
            
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timeout",
                "response": None
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "response": None
            }
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "Invalid JSON response",
                "response": None
            }
    
    def generate(
        self,
        message: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """
        Generate content using the LLM.
        Returns dict with 'success', 'response', 'error' keys.
        """
        last_error: Optional[str] = None
        
        for attempt in range(self.max_retries):
            result = self._make_request(message, system_prompt, attempt)
            
            if result is not None and result.get("success"):
                return result
            
            if result is not None:
                last_error = result.get("error")
            
            if attempt < self.max_retries - 1:
                delay = self.retry_delay * (attempt + 1)
                time.sleep(delay)
        
        return {
            "success": False,
            "error": f"Failed after {self.max_retries} retries: {last_error}",
            "response": None
        }
    
    def generate_batch(
        self,
        messages: List[str],
        system_prompt: str,
        combine: bool = True
    ) -> Dict[str, Any]:
        """
        Generate content for multiple messages in batches.
        If combine=True, combines all messages into a single request.
        """
        if combine:
            combined_message = "\n\n---\n\n".join(messages)
            return self.generate(combined_message, system_prompt)
        
        results: List[str] = []
        errors: List[Dict[str, Any]] = []
        
        for i, message in enumerate(messages):
            result = self.generate(message, system_prompt)
            
            if result["success"] and result["response"]:
                results.append(result["response"])
            else:
                errors.append({
                    "index": i,
                    "error": result.get("error", "Unknown error")
                })
        
        return {
            "success": len(errors) == 0,
            "responses": results,
            "errors": errors if errors else None
        }
    
    def generate_from_csv_batch(
        self,
        csv_text: str,
        system_prompt: str
    ) -> Dict[str, Any]:
        """
        Generate content from CSV text batch.
        """
        message = f"{system_prompt}\n\nCSV Data:\n{csv_text}"
        return self.generate(csv_text, system_prompt)
