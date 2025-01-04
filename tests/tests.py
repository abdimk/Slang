import asyncio
import unittest
from slang.api import ChatLlama
from slang.api import Llama_Models

LamaModel = Llama_Models.Meta_Llama_3_2_3B_Instruct.value

async def main()->str:
    async with ChatLlama("Give me a list of SiFi Movies",LamaModel) as lma:
        response = await lma.get_response()
        return  response
    
class TestStringReturn(unittest.TestCase):
    def test_return_type(self):
        result = asyncio.run(main())
        self.assertIsInstance(result,str, "Function should return a string")


if __name__ == '__main__':
    unittest.main()


