from typing import Any, Dict, List, Optional, Union
from app.core.config import settings
from app.enums.slack_message_type import SlackMsgType
from slack_sdk import WebClient
from app.dto.slack_request_dto import SlackPostRequest
import logging

logger = logging.getLogger(__name__)

class SlackService:

    EMOJI_MAP = {
        SlackMsgType.CRITICAL: ":rotating_light:",
        SlackMsgType.INFO: ":information_source:",
        SlackMsgType.WARNING: ":warning:",
    }


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
        
    @staticmethod
    def form_header_message(header: str,  emoji: Optional[str] = None) -> Dict[str, Any]:
        if not header:
            return {}
        
        if emoji:
            formatted_text = f"{emoji} {header}"

        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*{formatted_text}*",
            }
        }

    @staticmethod
    def form_main_content_message(content: str) -> Dict[str, Any]:
        if not content:
            return {}
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": content,
            }
        }


    # This should set channel, thread_ts, reply_broadcast, username, icon_url, icon_emoji
    @staticmethod
    def set_message_parameters(
        channel: str,
        thread_ts: Optional[str] = None,
        reply_broadcast: Optional[bool] = False,
        username: Optional[str] = None,
        icon_url: Optional[str] = None,
        icon_emoji: Optional[str] = None
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {
            "channel": channel,
            "link_names": True,
        }
        if thread_ts:
            params["thread_ts"] = thread_ts
            params["reply_broadcast"] = reply_broadcast
        if username:
            params["username"] = username
        if icon_url:
            params["icon_url"] = icon_url
        elif icon_emoji:
            params["icon_emoji"] = icon_emoji
        return params

    def post_formatted_message(self, slack_data: SlackPostRequest) -> Dict[str, Any]:
            try:
                # This part is unchanged
                optional_params = {
                    "thread_ts": slack_data.thread_ts,
                    "reply_broadcast": slack_data.reply_broadcast,
                    "username": slack_data.username,
                }
                filtered_params = {k: v for k, v in optional_params.items() if v is not None}
                payload: Dict[str, Any] = self.set_message_parameters(
                    channel=slack_data.channel, **filtered_params
                )

                if slack_data.blocks:
                    payload["blocks"] = slack_data.blocks
                    payload["text"] = slack_data.content or "Message with custom blocks."
                else:
                    emoji_icon = self.EMOJI_MAP.get(slack_data.message_type)
                    generated_blocks = []
                    
                    if slack_data.header:
                        generated_blocks.append(self.form_header_message(slack_data.header, emoji_icon))
                    generated_blocks.append(self.form_main_content_message(slack_data.content))
                    
                    payload["blocks"] = generated_blocks
                    payload["text"] = slack_data.content

                result = self.slack_client.chat_postMessage(**payload)
                return result
            except Exception as e:
                logger.error(f"An unexpected error occurred: {e}", exc_info=True)
                return {"ok": False, "error": str(e)}


        