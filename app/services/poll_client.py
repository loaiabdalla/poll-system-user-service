"""HTTP Client for inter-service communication with Poll Service."""
import logging
from typing import Optional
import httpx
from app.core.config import settings

logger = logging.getLogger(__name__)


class PollClient:
    """Handles external HTTP calls to the Poll Service."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or settings.POLL_SERVICE_URL).rstrip("/")

    async def delete_user_answers(self, user_id: int) -> bool:
        """
        Request Poll Service to delete all answers submitted by user_id.
        Returns True if successful or no answers existed, False if call failed.
        """
        url = f"{self.base_url}/answers/user/{user_id}"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.delete(url)
                if response.status_code in (200, 204, 404):
                    logger.info(f"Successfully signaled Poll Service to delete answers for user {user_id}")
                    return True
                logger.warning(
                    f"Poll Service returned {response.status_code} when deleting answers for user {user_id}: {response.text}"
                )
                return False
        except httpx.RequestError as exc:
            logger.error(f"Failed to communicate with Poll Service at {url}: {exc}")
            # In microservices, we log the failure so we don't completely lock out user deletion if Poll Service is offline
            return False
