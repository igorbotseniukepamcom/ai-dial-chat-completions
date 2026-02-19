from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        #TODO:
        # Documentation: https://pypi.org/project/aidial-client/ (here you can find how to create and use these clients)
        # 1. Create Dial client
        # 2. Create AsyncDial client
        

        self._client = Dial(
            base_url=DIAL_ENDPOINT,
            api_key=self._api_key
        )

        self._async_dial_client = AsyncDial(
            api_key=self._api_key, 
            base_url=DIAL_ENDPOINT
        )

    def get_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with client
        #    Hint: to unpack messages you can use the `to_dict()` method from Message object
        # 2. Get content from response, print it and return message with assistant role and content
        # 3. If choices are not present then raise Exception("No choices in response found")
        vdeployment_name=self._deployment_name
        vmessages=[msg.to_dict() for msg in messages]
        vstream=False

        completion = self._client.chat.completions.create(
            deployment_name=vdeployment_name,
            stream=vstream,
            messages=vmessages
        )

        if(completion.choices[0].message==''):
            raise Exception("No choices in response found")
        else:
            print(completion.choices[0].message.content)
            return Message(Role.AI,completion.choices[0].message.content)

    async def stream_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with async client
        #    Hint: don't forget to add `stream=True` in call.
        # 2. Create array with `contents` name (here we will collect all content chunks)
        # 3. Make async loop from `chunks` (from 1st step)
        # 4. Print content chunk and collect it contents array
        # 5. Print empty row `print()` (it will represent the end of streaming and in console we will print input from a new line)
        # 6. Return Message with assistant role and message collected content
        vdeployment_name=self._deployment_name
        vmessages=[msg.to_dict() for msg in messages]
        vstream=True

        chunks = await self._async_dial_client.chat.completions.create(
            deployment_name=vdeployment_name,
            stream=vstream,
            messages=vmessages
        )
        contents = []

        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    print(delta.content, end='')
                    contents.append(delta.content)

        print()
        return Message(Role.AI, ''.join(contents))