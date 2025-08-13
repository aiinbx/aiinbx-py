# Threads

Types:

```python
from ai_inbx.types import ThreadRetrieveResponse, ThreadSearchResponse
```

Methods:

- <code title="get /threads/{threadId}">client.threads.<a href="./src/ai_inbx/resources/threads.py">retrieve</a>(thread_id) -> <a href="./src/ai_inbx/types/thread_retrieve_response.py">ThreadRetrieveResponse</a></code>
- <code title="post /threads/search">client.threads.<a href="./src/ai_inbx/resources/threads.py">search</a>(\*\*<a href="src/ai_inbx/types/thread_search_params.py">params</a>) -> <a href="./src/ai_inbx/types/thread_search_response.py">ThreadSearchResponse</a></code>

# Emails

Types:

```python
from ai_inbx.types import EmailRetrieveResponse, EmailReplyResponse, EmailSendResponse
```

Methods:

- <code title="get /emails/{emailId}">client.emails.<a href="./src/ai_inbx/resources/emails.py">retrieve</a>(email_id) -> <a href="./src/ai_inbx/types/email_retrieve_response.py">EmailRetrieveResponse</a></code>
- <code title="post /emails/{emailId}/reply">client.emails.<a href="./src/ai_inbx/resources/emails.py">reply</a>(email_id, \*\*<a href="src/ai_inbx/types/email_reply_params.py">params</a>) -> <a href="./src/ai_inbx/types/email_reply_response.py">EmailReplyResponse</a></code>
- <code title="post /emails/send">client.emails.<a href="./src/ai_inbx/resources/emails.py">send</a>(\*\*<a href="src/ai_inbx/types/email_send_params.py">params</a>) -> <a href="./src/ai_inbx/types/email_send_response.py">EmailSendResponse</a></code>
