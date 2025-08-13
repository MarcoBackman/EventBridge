from fastapi import APIRouter, status, HTTPException, Depends, BackgroundTasks
from app.services.slack_service import SlackService
from app.dto.slack_request_dto import SlackPostRequest
import logging

logger = logging.getLogger(__name__)
slack_router = APIRouter(prefix="/slack", tags=["Slack"])

def get_slack_service() -> SlackService:
    return SlackService()

def post_slack_message_in_background(service: SlackService, 
                                     slack_data: SlackPostRequest):
    try:
        slack_response = service.post_formatted_message(slack_data)
        if not slack_response:
            logger.error(f"Failed to send formatted slack message from background task: {slack_response}")
    except Exception as e:
        logger.error(f"Error occured during the background task: {e}")


@slack_router.post("/post-formatted-message", status_code=status.HTTP_200_OK)
async def post_slack_formatted_message(
    slack_data: SlackPostRequest,
    background_tasks: BackgroundTasks,
    service: SlackService = Depends(get_slack_service) #Depds injection
):
    logger.info(f"Received request to post formatted Slack message to channel: {slack_data.channel}")
    background_tasks.add_task(post_slack_message_in_background, service, slack_data)
    #Alternatively you can use "from fastapi.concurrency import run_in_threadpool" if you have fixed with async and sync blocking code internally

    return {"message": "Slack message is being processed in the background."}


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
    