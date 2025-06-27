from typing import Any, Dict, List, Optional, Union
from app.core.config import settings
from slack_sdk import WebClient
from app.dto.slack_request_dto import SlackPostRequest
import logging

logger = logging.getLogger(__name__)

class SlackService:
    def __init__(self):
        self.slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)

    async def get_conversations_info(self, channel_id: str) -> None:
        try:
            result = await self.slack_client.conversations_info(channel=channel_id)

            if result.get("ok"):
                logger.info(f"Successfully retrieved info for channel ID: {channel_id}")
                return result.get("channel") # Return the 'channel' dictionary from the result
            else:
                error_msg = result.get("error", "Unknown error during conversations_info")
                logger.error(f"Slack API error in get_conversations_info for {channel_id}: {error_msg}")
                return None
        except Exception as e:
            logger.error(f"An unexpected error occurred in get_conversations_info for {channel_id}: {e}", exc_info=True)
            return None


    async def send_message_to_channel(self, channel_id: str, message: str) -> Dict[str, Any]:
        try:
            # Correct parameter: use 'text' for message content
            result = await self.slack_client.chat_postMessage(
                channel=channel_id,
                text=message
            )

            if result.get("ok"):
                logger.info(f"Message successfully sent to channel {channel_id}.")
            else:
                error_msg = result.get("error", "Unknown error from Slack API")
                logger.error(f"Failed to send message to channel {channel_id}: {error_msg}")
            
            return result # Return the full Slack API response

        except Exception as e:
            logger.error(f"An unexpected error occurred while sending Slack message to {channel_id}: {e}", exc_info=True)
            # Return a consistent error format
            return {"ok": False, "error": str(e), "detail": "An exception occurred in the service"}
        
    async def post_formatted_message(self, slack_data: SlackPostRequest) -> Dict[str, Any]:
        try:
            payload: Dict[str, Any] = {
                "channel": slack_data.channel,
                "link_names": True, # Common practice to automatically link @mentions and #channels
            }

            # Handle Threading
            if slack_data.thread_ts:
                payload["thread_ts"] = slack_data.thread_ts
                payload["reply_broadcast"] = slack_data.reply_broadcast

            # Handle Custom Sender Info
            if slack_data.username:
                payload["username"] = slack_data.username
            if slack_data.icon_url:
                payload["icon_url"] = str(slack_data.icon_url) # Pydantic HttpUrl needs to be stringified
            elif slack_data.icon_emoji:
                payload["icon_emoji"] = slack_data.icon_emoji

            # --- Message Content Logic (Blocks vs. Text) ---
            if slack_data.blocks:
                payload["blocks"] = slack_data.blocks
                payload["text"] = slack_data.content
            else:
                generated_blocks: List[Dict[str, Any]] = []
                if slack_data.header:
                    generated_blocks.append(
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": slack_data.header,
                                "emoji": True
                            }
                        }
                    )
                
                # Always add the main content, either in a section block or as simple text
                if generated_blocks:
                    # If there are already blocks (from header), add content as a section block
                    generated_blocks.append(
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn", # Assume mrkdwn is desired in blocks for content
                                "text": slack_data.content
                            }
                        }
                    )
                    payload["blocks"] = generated_blocks
                    payload["text"] = slack_data.content # Fallback text
                else:
                    # No blocks and no header, send as simple text
                    payload["text"] = slack_data.content
                    # Apply mrkdwn setting directly to the top-level 'text' field
                    # Assuming SlackMsgType maps to a boolean
                    # payload["mrkdwn"] = True if slack_data.messageType == SlackMsgType.MARKDOWN_TRUE else False

            # Send the message
            result = self.slack_client.chat_postMessage(**payload)

            if result.get("ok"):
                logger.info(f"Formatted message successfully sent to channel {slack_data.channel}.")
            else:
                error_msg = result.get("error", "Unknown error from Slack API")
                logger.error(f"Failed to send formatted message to channel {slack_data.channel}: {error_msg}")
            
            return result

        except Exception as e:
            logger.error(f"An unexpected error occurred while sending formatted Slack message to {slack_data.channel}: {e}", exc_info=True)
            return {"ok": False, "error": str(e), "detail": "An exception occurred in the service"}


        