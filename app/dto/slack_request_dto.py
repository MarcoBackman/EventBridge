from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from app.enums.slack_message_type import SlackMsgType

class SlackPostRequest(BaseModel):
    channel: str = Field(
        ...,
        description="The ID of the channel, private group, or DM to send the message to (e.g., 'C123ABC456').",
        examples=["C123ABC456", "D123ABC456"]
    )

    header: Optional[str] = Field(
        None,
        max_length=150, # Slack headers in blocks have a max length
        description="Optional header text for the message. Will be formatted.",
        examples=["Important Update!", "Daily Report"]
    )

    content: str = Field(
        ...,
        description="The main text content of the message. Supports Slack's mrkdwn formatting.",
        examples=["Hello, *world*!", "This is a new line.\n- Item 1\n- Item 2"]
    )

    messageType: Optional[SlackMsgType] = Field(
        True, # Default to True, meaning mrkdwn is enabled for 'content'
        alias="mrkdwn", # Use an alias to map to Slack's 'mrkdwn' parameter if needed in the API call
        description="Whether to parse Slack's mrkdwn formatting in the 'content' field. Defaults to True.",
    )

    blocks: Optional[List[dict]] = Field(
        None,
        description="A list of Slack Block Kit blocks to compose the message. Overrides 'content' for rich layout.",
        examples=[
            [
                {"type": "section", "text": {"type": "mrkdwn", "text": "This is a *section* block."}},
                {"type": "divider"}
            ]
        ]
    )

    # For replying in a thread
    thread_ts: Optional[str] = Field(
        None,
        description="The timestamp of the parent message to reply in a thread (e.g., '1678886400.000000').",
        examples=["1678886400.000000"]
    )

    # Whether to broadcast the reply to the channel
    reply_broadcast: Optional[bool] = Field(
        False,
        description="Set to true to indicate the reply should be shown in the channel, not just in the thread.",
    )

    # Optional custom sender information
    username: Optional[str] = Field(
        None,
        max_length=80, # Common max length for usernames
        description="Optional custom username for the message sender (e.g., 'MyApp Bot').",
        examples=["Notification Bot"]
    )

    message_type: SlackMsgType = Field(
        SlackMsgType.INFO,
        description="The type of message to send. Defaults to TEXT, which uses mrkdwn formatting.",
        examples=[SlackMsgType.INFO, SlackMsgType.WARNING, SlackMsgType.CRITICAL]
    )