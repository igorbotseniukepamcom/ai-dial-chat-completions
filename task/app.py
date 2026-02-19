import asyncio

from task.clients.client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    #TODO:
    # 1.1. Create DialClient
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    # 1.2. Create CustomDialClient
    # 2. Create Conversation object
    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    # 4. Use infinite cycle (while True) and get yser message from console
    # 5. If user message is `exit` then stop the loop
    # 6. Add user message to conversation history (role 'user')
    # 7. If `stream` param is true -> call DialClient#stream_completion()
    #    else -> call DialClient#get_completion()
    # 8. Add generated message to history
    # 9. Test it with DialClient and CustomDialClient
    # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response
    print('Start a new chat conversation:')
    # Model to use 
    model='gpt-4o'

    dc=DialClient(model)

    conv_chat=Conversation()
    #check for system prompt
    print("Input system prompt")
    prompt=input("Enter prompt>").strip()
    # Default system role and prompt 
    if prompt:
        init_message=Message(
            Role.SYSTEM,
            prompt
        )
    else:
        init_message=Message(
            Role.SYSTEM,
            DEFAULT_SYSTEM_PROMPT
        )

    conv_chat.add_message(init_message)

    print("Type your question or 'exit' to quit.")
    while(True):

        uq=input('Enter question > ').strip()

        if(uq.lower()=='exit'):
            print("Exiting the chat. Goodbye!")
            break

        if(uq.lower()=='show'):
            print(conv_chat.get_messages())
            continue  

        query_message=Message(
            Role.USER,
            content=uq
        )

        conv_chat.add_message(query_message)

        print('AI:')
        if stream:
            resp_message= await dc.stream_completion(conv_chat.get_messages())
        else:
            resp_message=dc.get_completion(conv_chat.get_messages())

        conv_chat.add_message(resp_message)
        

print("Please check mode ( sync or async) in start() function and set stream param accordingly.")

s=input("Do you want to enable streaming mode? (yes/no) > ").strip().lower()
stream_mode = True if s == 'yes' else False

asyncio.run(
    start(stream_mode)
)
