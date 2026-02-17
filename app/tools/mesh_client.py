"""Mesh Client for Consumer Risk Model Integration.

This module provides client functionality to interact with the consumer-risk-model-mesh
for quantitative risk calculations (PD/LGD/EAD).
"""

import httpx
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class ExposureData(BaseModel):
    """Exposure data for risk calculations."""
    
    loan_amount: float = Field(..., description="Loan amount in dollars")
    ltv: float = Field(..., description="Loan-to-value ratio")
    fico_score: int = Field(..., description="FICO credit score")
    dti: float = Field(..., description="Debt-to-income ratio")
    property_type: str = Field(..., description="Property type")
    occupancy: str = Field(..., description="Occupancy status")
    loan_purpose: str = Field(..., description="Loan purpose")


class RiskMetrics(BaseModel):
    """Risk metrics output from mesh."""
    
    pd: float = Field(..., description="Probability of Default")
    lgd: float = Field(..., description="Loss Given Default")
    ead: float = Field(..., description="Exposure at Default")
    expected_loss: float = Field(..., description="Expected Loss")
    rwa: float = Field(..., description="Risk-Weighted Assets")


class MeshClient:
    """Client for interacting with consumer-risk-model-mesh API."""
    
    def __init__(
        self,
        base_url: str = "http://localhost:5000",
        api_version: str = "v1",
        timeout: int = 30,
        api_token: Optional[str] = None
    ):
        """Initialize mesh client.
        
        Args:
            base_url: Base URL of the mesh API
            api_version: API version to use
            timeout: Request timeout in seconds
            api_token: Optional authentication token
        """
        self.base_url = base_url.rstrip("/")
        self.api_version = api_version
        self.timeout = timeout
        self.api_token = api_token
        
        self.headers = {}
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"
    
    async def calculate_risk_metrics(
        self,
        exposure_data: ExposureData
    ) -> RiskMetrics:
        """Calculate PD/LGD/EAD for a given exposure.
        
        Args:
            exposure_data: Loan exposure data
            
        Returns:
            Risk metrics including PD, LGD, EAD, and RWA
        """
        url = f"{self.base_url}/api/{self.api_version}/calculate"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    json=exposure_data.model_dump(),
                    headers=self.headers
                )
                response.raise_for_status()
                
                data = response.json()
                return RiskMetrics(**data)
                
            except httpx.HTTPError as e:
                logger.error(f"Mesh API request failed: {e}")
                raise
    
    async def get_model_performance(
        self,
        model_id: str
    ) -> Dict[str, Any]:
        """Get performance metrics for a model.
        
        Args:
            model_id: ID of the model
            
        Returns:
            Model performance metrics
        """
        url = f"{self.base_url}/api/{self.api_version}/models/{model_id}/performance"
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Failed to get model performance: {e}")
                raise
    
    async def run_stress_test(
        self,
        scenario_name: str,
        exposures: List[ExposureData]
    ) -> Dict[str, Any]:
        """Run stress testing scenario.
        
        Args:
            scenario_name: Name of stress scenario
            exposures: List of exposures to stress test
            
        Returns:
            Stress test results
        """
        url = f"{self.base_url}/api/{self.api_version}/stress-test"
        
        payload = {
            "scenario": scenario_name,
            "exposures": [exp.model_dump() for exp in exposures]
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Stress test failed: {e}")
                raise
    
    def health_check(self) -> bool:
        """Check if mesh API is healthy.
        
        Returns:
            True if API is responding, False otherwise
        """
        url = f"{self.base_url}/health"
        
        try:
            response = httpx.get(url, timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Health check failed: {e}")
            return False
