from fastapi import APIRouter, status, HTTPException, Depends
from app.services.slack_service import SlackService
from app.dto.slack_request_dto import SlackPostRequest
import logging

logger = logging.getLogger(__name__)
slack_router = APIRouter(prefix="/slack", tags=["Slack"])

def get_slack_service() -> SlackService:
    return SlackService()

@slack_router.post("/post-formatted-message", status_code=status.HTTP_200_OK)
async def post_slack_formatted_message(
    slack_data: SlackPostRequest,
    service: SlackService = Depends(get_slack_service)
):
    logger.info(f"Received request to post formatted Slack message to channel: {slack_data.channel}")

    slack_response = await service.post_formatted_message(slack_data)

    if slack_response.get("ok"):
        return {"message": "Formatted Slack message sent successfully!", "slack_response": slack_response}
    else:
        error_detail = slack_response.get('error', 'Failed to send formatted Slack message.')
        logger.error(f"Failed to send formatted Slack message: {error_detail}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to send Slack message: {error_detail}"
        )   

@slack_router.post("/test-message", status_code=status.HTTP_200_OK)
async def send_slack_message(
    slack_data: SlackPostRequest
): 
    success = await get_slack_service().post_formatted_message(
        slack_data
    )
    return {"message" : success}

@slack_router.get("/get-test", status_code=status.HTTP_200_OK)
async def get_slack_channels(channel_id:str):
    success = await get_slack_service().get_conversations_info(channel_id)
    return {"message" : success}
    