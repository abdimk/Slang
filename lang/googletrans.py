import requests
import urllib.parse


#not complited use it on your own risk 



class GoogleTrans:
    def __init__(self,text):
        self.text_to_translate = text
        self.encoded_text = urllib.parse.quote(self.text_to_translate)
        self.url = f"https://translate.googleapis.com/translate_a/single?client=gtx&dj=1&dt=t&dt=at&dt=bd&dt=ex&dt=md&dt=rw&dt=ss&dt=rm&sl=en&tl=am&tk=776969.883488&q={self.encoded_text}"
        self.response = requests.get(self.url)
        self.json_response = self.response.json()
    
    def extract(self,json_response:str) -> None:
        # Extracting elements using variables
        sentences = json_response.get('sentences', [{}])
        translation = sentences[0].get('trans', '')
        original_text = sentences[0].get('orig', '')
        backend = sentences[0].get('backend', '')
        model_specification = sentences[0].get('model_specification', [{}])
        translation_engine_debug_info = sentences[0].get('translation_engine_debug_info', [{}])
        src_language = json_response.get('src', '')
        alternative_translations = json_response.get('alternative_translations', [{}])
        confidence = json_response.get('confidence', '')
        spell = json_response.get('spell', {})
        ld_result = json_response.get('ld_result', {})

        model_performace = {
            "sentences":sentences,
            "translation":translation,
            "original_text":original_text,
            "backend":backend,
            "model_specification":model_specification,
            "translation_engine_debug_info":translation_engine_debug_info,
            "src_language":src_language,
            "alternative_translations":alternative_translations,
            "confidence":confidence,
            "spell":spell,
            "ld_result":ld_result
        }
        # Extracting and printing alternative translations if available
        print("Alternative Translations:")
        for i, alternative in enumerate(alternative_translations):
            src_phrase = alternative.get('src_phrase', '')
            alternatives = alternative.get('alternative', [])
            print(f"  Source Phrase [{i}]: {src_phrase}")
            for j, alt in enumerate(alternatives):
                word_postproc = alt.get('word_postproc', '')
                score = alt.get('score', '')
                has_preceding_space = alt.get('has_preceding_space', '')
                attach_to_next_token = alt.get('attach_to_next_token', '')
                backends = alt.get('backends', [])
                print(f"    Alternative [{j}]:")
                print(f"      Word Postproc: {word_postproc}")
                print(f"      Score: {score}")
                print(f"      Has Preceding Space: {has_preceding_space}")
                print(f"      Attach to Next Token: {attach_to_next_token}")
                print(f"      Backends: {backends}")

            # LD Result details
            srclangs = ld_result.get('srclangs', [])
            srclangs_confidences = ld_result.get('srclangs_confidences', [])
            extended_srclangs = ld_result.get('extended_srclangs', [])

            print("LD Result:")
            print(f"  Source Languages: {srclangs}")
            print(f"  Source Languages Confidences: {srclangs_confidences}")
            print(f"  Extended Source Languages: {extended_srclangs}")

# G1 = GoogleTrans("i have a dog!")
# G1.extract(G1.json_response)