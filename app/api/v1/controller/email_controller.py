from fastapi import FastAPI, APIRouter, HTTPException, status
from app.dto.email import EmailRequest, EmailBatchRequest, EmailSendRequest
#from app.services.email_service import email_service

router = APIRouter(prefix="/emails", tags=["Emails"])

@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def send_email(
    email_data: EmailRequest,
    # current_user: Any = Depends(get_current_active_user) # Example: requires authentication
):
    # """
    # Endpoint to send a single email.
    # """
    # success = await email_service.send_single_email(
    #     recipient_email=email_data.recipient_email,
    #     subject=email_data.subject,
    #     body=email_data.body
    # )
    # if not success:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to send email")
    # return {"message": "Email sending initiated successfully"}
    pass

@router.post("/batch", status_code=status.HTTP_202_ACCEPTED)
async def send_batch_emails(
    batch_data: EmailBatchRequest, # Assuming you have a Pydantic model for a list of EmailRequest
    # current_user: Any = Depends(get_current_active_user)
):
    """
    Endpoint to send multiple emails in a batch.
    """
    pass
    # results = await email_service.send_batch_emails(batch_data.emails)
    # if all(results):
    #     return {"message": "All emails initiated successfully"}
    # elif any(results):
    #     return {"message": "Some emails failed to send", "results": results}
    # else:
    #    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="All emails failed to send")
    
@router.post("/send-mail", status_code=status.HTTP_200_OK)
async def postEmail(request: EmailSendRequest):
    pass
    # try :
    #     logger.info(f"이메일 전송 요청 수신:")
    #     logger.debug(f"  To: {request.to_recipients}")
    #     logger.debug(f"  Subject: {request.subject}")
    #     logger.debug(f"  Body (HTML: {request.is_html}): {request.body[:50]}...") # 본문 일부만 출력
    #     if request.cc_recipients:
    #         logger.debug(f"  CC: {request.cc_recipients}")
    #     if request.bcc_recipients:
    #         logger.debug(f"  BCC: {request.bcc_recipients}")

    #     #이메일 전송
    #     result = await email_service.send_single_email()

    #     await logger.info("이메일 전송 성공.")
    #     return {"message": "이메일이 성공적으로 전송되었습니다.", "request_id": "some_unique_id_123"}
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         detail=f"이메일 전송 실패했습니다: {e}"
    #     )