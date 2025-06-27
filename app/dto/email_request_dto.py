from pydantic import BaseModel, EmailStr, Field, BeforeValidator
from typing import List, Optional, Union, Annotated

def ensure_list_of_emails(v: Union[str, List[EmailStr]]) -> List[EmailStr]:
    """Ensures a single email string is converted to a list."""
    if isinstance(v, str):
        return [v]
    return v

# Create an Annotated type for convenience
ListOfEmails = Annotated[List[EmailStr], BeforeValidator(ensure_list_of_emails)]

class EmailSendRequest(BaseModel):
    to_recipients: ListOfEmails = Field(
        min_items=1,
        description="이메일을 받을 한 명 이상의 수신자 이메일 주소 목록"
    )

    subject: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="이메일의 제목."
    )

    body: str = Field(
        ...,
        min_length=1,
        description="이메일 본문 내용 (HTML or Text)"
    )

    cc_recipients: Optional[ListOfEmails] = Field(
        None,
        description="이메일 참조(CC) 목록"
    )

    bcc_recipients: Optional[ListOfEmails] = Field(
        None,
        description="이메일의 숨은 참조 (BCC) 목록"
    )

    is_html: bool = Field(
        False,
        description="이메일 본문 HTML 형식 여부 (기본값: False)"
    )

    class Config: # Note: In Pydantic v2, this is now `model_config`
        json_schema_extra = { # Also `schema_extra` is now `json_schema_extra`
            "example": {
                "to_recipients": ["john.doe@example.com"],
                "subject": "안녕하세요! Pydantic 이메일 예시입니다.",
                "body": "이것은 Pydantic을 사용하여 생성된 이메일 본문입니다. <br> <b>좋은 하루 되세요!</b>",
                "cc_recipients": ["jane.doe@example.com"],
                "bcc_recipients": ["secret.user@example.com"],
                "is_html": True
            }
        }

# Example Usage to test:
print(EmailSendRequest(to_recipients="test@example.com", subject="Test", body="Hi"))
# Expected output: to_recipients=['test@example.com']

print(EmailSendRequest(to_recipients=["test1@example.com", "test2@example.com"], subject="Test2", body="Hello"))
# Expected output: to_recipients=['test1@example.com', 'test2@example.com']