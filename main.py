import calendar
import logging
import random
import time

import requests

import settings

logger = logging.getLogger("run")
error_logger = logging.getLogger("errors")
global start_time
config = settings.Config().load()

# times_to_run = random.randint(300, 500)
times_to_run = 500
BASE_URL = "https://www.duolingo.com/"
COOKIE = (
    "lang=en; duocsexp0=web_delight_use_fetch_v3~experiment~; lu=https://www.duolingo.com/; "
    "initial_referrer=$direct; lr=; lp=splash; G_ENABLED_IDPS=google; "
    "csrf_token=IjdkOTBlYzY2ZmM5MjQwNjc4YWVkYTgyNjNiNDRhOTdkIg==; logged_out_uuid=509830122; logged_in=true; "
    "OptanonAlertBoxClosed=2022-12-03T17:23:05.663Z; wuuid=6a1cd314-6f7c-4679-8f2b-f08befba9892; "
    "jwt_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjYzMDcyMDAwMDAsImlhdCI6MCwic3ViIjo1MDk4MzAxMjJ9"
    ".JX4b7xHKnNoqZiQK0YrVZYVOt98TVh2WCCEZTngdgeY; tsl=1673266436916; "
    "OptanonConsent=isGpcEnabled=0&datestamp=Mon+Jan+09+2023+12%3A13%3A58+GMT%2B0000+("
    "Greenwich+Mean+Time)&version=6.16.0&isIABGlobal=false&consentId=a5c719ad-f12c-464c-9b78-d91a7112a6bf"
    "&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&hosts"
    "=H3%3A1%2CH14%3A1%2CH11%3A1%2CH1%3A1%2CH15%3A1%2CH6%3A1%2CH22%3A1%2CH2%3A1%2CH7%3A1%2CH16%3A1%2CH9%3A1"
    "%2CH18%3A1%2CH10%3A1%2CH12%3A1%2CH13%3A1&geolocation=GB%3BENG&AwaitingReconsent=false; "
    "AWSALB=i4ODpXdyoq5thBDs/nC3gg27SDdOwkfP9OpmDIMH2oxQ687vCoq4Raotx4V2IWqM4Lm0JAhZ"
    "+glGVkfO09Hgdzb0UiLcx1K40x32KlIVAl+M3u6HFBNw1S4I7Ej9; "
    "AWSALBCORS=i4ODpXdyoq5thBDs/nC3gg27SDdOwkfP9OpmDIMH2oxQ687vCoq4Raotx4V2IWqM4Lm0JAhZ"
    "+glGVkfO09Hgdzb0UiLcx1K40x32KlIVAl+M3u6HFBNw1S4I7Ej9"
)
headers = {
    "Content-Type": "application/json;charset=UTF-8",
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9"
    ".eyJleHAiOjYzMDcyMDAwMDAsImlhdCI6MCwic3ViIjo1MDk4MzAxMjJ9"
    ".JX4b7xHKnNoqZiQK0YrVZYVOt98TVh2WCCEZTngdgeY",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
    "Safari/537.36",
    "Cookie": COOKIE,
}


def get_new_lesson():
    global start_time
    payload = """{"challengeTypes":["assist","characterIntro","characterMatch","characterPuzzle","characterSelect",
    "characterTrace","completeReverseTranslation","definition","dialogue","form","freeResponse","gapFill","judge",
    "listen","listenComplete","listenMatch","match","name","listenComprehension","listenIsolation","listenTap",
    "partialListen","partialReverseTranslate","readComprehension","select","selectPronunciation",
    "selectTranscription","syllableTap","syllableListenTap","tapCloze","tapClozeTable","tapComplete",
    "tapCompleteTable","tapDescribe","translate","typeCloze","typeClozeTable","typeCompleteTable"],
    "fromLanguage":"en","isFinalLevel":false,"isV2":true,"juicy":true,"learningLanguage":"id","levelSessionIndex":4,
    "levelIndex":0,"skillIds":["9bed47bf0a11ae48fc67c116d2a9e28e"],"type":"LEXEME_SKILL_LEVEL_PRACTICE"}"""
    response = requests.post(
        f"{BASE_URL}2017-06-30/sessions", data=payload, headers=headers
    )
    logger.debug(response.content)
    if response.status_code != 200:
        error_logger.error(str(response.status_code) + " - " + str(response.content))
        # raise AssertionError(response.status_code)
    json_response = response.json()
    lesson_id = json_response["id"]
    logger.info(f"Starting lesson with ID: {lesson_id}")
    start_time = calendar.timegm(time.gmtime()) + offset
    logger.info(f"Start Time: {start_time}")
    return lesson_id


def complete_lesson(lesson_id):
    global start_time
    end_time = calendar.timegm(time.gmtime()) + offset
    logger.info(f"End Time: {end_time}")

    payload = (
        '{"id":"'
        + lesson_id
        + '","learningLanguage":"id","fromLanguage":"en","type":"LEXEME_SKILL_LEVEL_PRACTICE","challenges":[{'
        '"prompt":"apple","choices":[{'
        '"image":"https://d2pur3iezf4d1j.cloudfront.net/images/645fa42dcea02c7e2970a1285e321562",'
        '"phrase":"Susu","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/645fa42dcea02c7e2970a1285e321562",'
        '"tts":"https://d1vq87e9lcf771.cloudfront.net/eka/cbbb794000c03229cae129d964b86542","hint":"Milk"},'
        '{"image":"https://d2pur3iezf4d1j.cloudfront.net/images/cd1ecb710774af3d4904673137972ef3",'
        '"phrase":"apel","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/cd1ecb710774af3d4904673137972ef3",'
        '"tts":"https://d1vq87e9lcf771.cloudfront.net/eka/21557015e016652a58c101c99e7ca890","hint":"apple"},'
        '{"image":"https://d2pur3iezf4d1j.cloudfront.net/images/0131443731d05ac52199b3317eda2aab",'
        '"phrase":"jeruk","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/0131443731d05ac52199b3317eda2aab'
        '","tts":"https://d1vq87e9lcf771.cloudfront.net/eka/f1c58d6163764eafd35b7d49540e0726",'
        '"hint":"orange"}],"correctIndex":1,"type":"select","id":"65ed27a806064725b8acc1955d2d09a0",'
        '"challengeResponseTrackingProperties":{"level_session_index":4,"birdbrain_target":0.95,'
        '"birdbrain_source":"birdbrain_v2","generation_timestamp":1668024818326,"is_v2":true,'
        '"birdbrain_probability":0.97698724,"content_length":4},"metadata":{"challenge_construction_insights":{'
        '"birdbrain_probability":0.97698724,"birdbrain_target":0.95,"birdbrain_source":"birdbrain_v2",'
        '"content_length":4},"highlight":[],"hint":"apple","phrase":"apel",'
        '"solution_key":"ffd1c18dff303827bb5da81fcddc35c7","source_language":"id",'
        '"specific_type":"name_example","language":"id","lexeme_ids_to_update":['
        '"ffd1c18dff303827bb5da81fcddc35c7"],"type":"select","lexemes_to_update":['
        '"ffd1c18dff303827bb5da81fcddc35c7"],"generic_lexeme_map":{},"num_comments":0,"learning_language":"id",'
        '"from_language":"en"},"newWords":[],"progressUpdates":[],"challengeGeneratorIdentifier":{'
        '"specificType":"name_example","generatorId":"ffd1c18dff303827bb5da81fcddc35c7"},"timeTaken":934354,'
        '"correct":true,"guess":"1"},{"choices":["Ia kamu.","Hitam itu kuat.","Dia kuat."],"correctIndices":['
        '2],"prompt":"She is strong.","sourceLanguage":"en","targetLanguage":"id",'
        '"solutionTts":"https://d1vq87e9lcf771.cloudfront.net/ade/b15d20c1baa00a619afa1cf8bb039a7f",'
        '"type":"judge","id":"ff025eee8d4b40f7ad6b23136830f27a","challengeResponseTrackingProperties":{'
        '"best_solution":"Dia kuat.","level_session_index":4,"birdbrain_target":0.95,'
        '"birdbrain_source":"birdbrain_v2","generation_timestamp":1668024818326,"is_v2":true,'
        '"birdbrain_probability":0.949394,"content_length":9},"metadata":{"challenge_construction_insights":{'
        '"birdbrain_probability":0.949394,"birdbrain_target":0.95,"birdbrain_source":"birdbrain_v2",'
        '"content_length":9,"best_solution":"Dia kuat."},"sentences":[{"sentence":"Ia kamu.","correct":false},'
        '{"sentence":"Hitam itu kuat.","correct":false},{"sentence":"Dia kuat.","correct":true}],'
        '"solution_key":"1d06dd491c510f8f44922f42c3660377","source_language":"en","target_language":"id",'
        '"text":"She is strong.","highlight":[],"type":"judge","specific_type":"target_learning_judge",'
        '"lexeme_ids_to_update":["1d081cc665403ad7dc506f9996b64d6d","bb08fee5dcef31845e9aa77fbc71734a"],'
        '"lexemes_to_update":["1d081cc665403ad7dc506f9996b64d6d","bb08fee5dcef31845e9aa77fbc71734a"],'
        '"generic_lexeme_map":{},"learning_language":"id","from_language":"en","options":[{"sentence":"Ia '
        'kamu.","correct":false},{"sentence":"Hitam itu kuat.","correct":false},{"sentence":"Dia kuat.",'
        '"correct":true}]},"newWords":[],"progressUpdates":[],'
        '"sentenceDiscussionId":"1d06dd491c510f8f44922f42c3660377","challengeGeneratorIdentifier":{'
        '"specificType":"target_learning_judge","generatorId":"a6b81b74d830353d36d3dece76b20f23"},'
        '"timeTaken":1985,"correct":true,"guess":2},{"prompt":"water","choices":[{'
        '"image":"https://d2pur3iezf4d1j.cloudfront.net/images/7afea32bcf0e8c6f9d446ad4aad416be",'
        '"phrase":"air","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/7afea32bcf0e8c6f9d446ad4aad416be",'
        '"tts":"https://d1vq87e9lcf771.cloudfront.net/ade/b2e60ea638c37930fdd5e236ac3ace22","hint":"water"},'
        '{"image":"https://d2pur3iezf4d1j.cloudfront.net/images/645fa42dcea02c7e2970a1285e321562",'
        '"phrase":"Susu","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/645fa42dcea02c7e2970a1285e321562",'
        '"tts":"https://d1vq87e9lcf771.cloudfront.net/eka/cbbb794000c03229cae129d964b86542","hint":"Milk"},'
        '{"image":"https://d2pur3iezf4d1j.cloudfront.net/images/0131443731d05ac52199b3317eda2aab",'
        '"phrase":"jeruk","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/0131443731d05ac52199b3317eda2aab'
        '","tts":"https://d1vq87e9lcf771.cloudfront.net/eka/f1c58d6163764eafd35b7d49540e0726",'
        '"hint":"orange"}],"correctIndex":0,"type":"select","id":"beb353fe16444ab2ad2a5534e00f3a77",'
        '"challengeResponseTrackingProperties":{"level_session_index":4,"birdbrain_target":0.95,'
        '"birdbrain_source":"birdbrain_v2","generation_timestamp":1668024818326,"is_v2":true,'
        '"birdbrain_probability":0.9608965,"content_length":3},"metadata":{"challenge_construction_insights":{'
        '"birdbrain_probability":0.9608965,"birdbrain_target":0.95,"birdbrain_source":"birdbrain_v2",'
        '"content_length":3},"highlight":[],"hint":"water","phrase":"air",'
        '"solution_key":"9f724dd75011977323c2f2d12a3d74a5","source_language":"id",'
        '"specific_type":"name_example","language":"id","lexeme_ids_to_update":['
        '"9f724dd75011977323c2f2d12a3d74a5"],"type":"select","lexemes_to_update":['
        '"9f724dd75011977323c2f2d12a3d74a5"],"generic_lexeme_map":{},"num_comments":0,"learning_language":"id",'
        '"from_language":"en"},"newWords":[],"progressUpdates":[],"challengeGeneratorIdentifier":{'
        '"specificType":"name_example","generatorId":"9f724dd75011977323c2f2d12a3d74a5"},"timeTaken":870,'
        '"correct":true,"guess":"0"},{"choices":["Kamu punya kucing.","Kamu punya dia-kucing.","Anda memelihara '
        'apel-kucing."],"correctIndices":[0],"prompt":"You have cats.","sourceLanguage":"en",'
        '"targetLanguage":"id",'
        '"solutionTts":"https://d1vq87e9lcf771.cloudfront.net/ade/e1869b2cd29eb1a47eb95d765149557f",'
        '"type":"judge","id":"65129e7283c04346b17d6d53f2439ab3","challengeResponseTrackingProperties":{'
        '"best_solution":"Kamu punya kucing.","level_session_index":4,"birdbrain_target":0.95,'
        '"birdbrain_source":"birdbrain_v2","generation_timestamp":1668024818326,"is_v2":true,'
        '"birdbrain_probability":0.9477119,"content_length":18},"metadata":{"challenge_construction_insights":{'
        '"birdbrain_probability":0.9477119,"birdbrain_target":0.95,"birdbrain_source":"birdbrain_v2",'
        '"content_length":18,"best_solution":"Kamu punya kucing."},"sentences":[{"sentence":"Kamu punya '
        'kucing.","correct":true},{"sentence":"Kamu punya dia-kucing.","correct":false},{"sentence":"Anda '
        'memelihara apel-kucing.","correct":false}],"solution_key":"83e92fc961d5ed6fda818dfaf8b198aa",'
        '"source_language":"en","target_language":"id","text":"You have cats.","highlight":[],"type":"judge",'
        '"specific_type":"target_learning_judge","lexeme_ids_to_update":["8732721164c1b018aeefdddf53a79498",'
        '"2163279839037ce9c20ad5eeafb358f3","e0153bafefabee09d4eca6e5da227e43"],"lexemes_to_update":['
        '"8732721164c1b018aeefdddf53a79498","2163279839037ce9c20ad5eeafb358f3",'
        '"e0153bafefabee09d4eca6e5da227e43"],"generic_lexeme_map":{},"learning_language":"id",'
        '"from_language":"en","options":[{"sentence":"Kamu punya kucing.","correct":true},{"sentence":"Kamu '
        'punya dia-kucing.","correct":false},{"sentence":"Anda memelihara apel-kucing.","correct":false}]},'
        '"newWords":[],"progressUpdates":[],"sentenceDiscussionId":"83e92fc961d5ed6fda818dfaf8b198aa",'
        '"challengeGeneratorIdentifier":{"specificType":"target_learning_judge",'
        '"generatorId":"27d9b5e59466ea4f1efe4efbf5f952e0"},"timeTaken":511,"correct":true,"guess":0},'
        '{"prompt":"black","choices":[{'
        '"image":"https://d2pur3iezf4d1j.cloudfront.net/images/0131443731d05ac52199b3317eda2aab",'
        '"phrase":"jeruk","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/0131443731d05ac52199b3317eda2aab'
        '","tts":"https://d1vq87e9lcf771.cloudfront.net/ade/e583242232aafa91bb712ae4fe6bd361","hint":"orange"},'
        '{"image":"https://d2pur3iezf4d1j.cloudfront.net/images/8a0bf2fda530b50c833af5ce0c4ab30f",'
        '"phrase":"hitam","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/8a0bf2fda530b50c833af5ce0c4ab30f'
        '","tts":"https://d1vq87e9lcf771.cloudfront.net/eka/5b2f1b23a324c0a7ffaa1fcb8bbbee1c","hint":"black"},'
        '{"image":"https://d2pur3iezf4d1j.cloudfront.net/images/9aa862ebf2f8636383e54ce23d340db9",'
        '"phrase":"kucing","svg":"https://d2pur3iezf4d1j.cloudfront.net/images/9aa862ebf2f8636383e54ce23d340db9'
        '","tts":"https://d1vq87e9lcf771.cloudfront.net/eka/eab8f9526fab5b3c70dfb7172f4c4cec","hint":"cat"}],'
        '"correctIndex":1,"type":"select","id":"28b9d6cf22e64d96bed8c746df024c29",'
        '"challengeResponseTrackingProperties":{"level_session_index":4,"birdbrain_target":0.95,'
        '"birdbrain_source":"birdbrain_v2","generation_timestamp":1668024818326,"is_v2":true,'
        '"birdbrain_probability":0.94840115,"content_length":5},"metadata":{"challenge_construction_insights":{'
        '"birdbrain_probability":0.94840115,"birdbrain_target":0.95,"birdbrain_source":"birdbrain_v2",'
        '"content_length":5},"highlight":[],"hint":"black","phrase":"hitam",'
        '"solution_key":"e8dcf52d441912d0f1f6a4b154f27934","source_language":"id",'
        '"specific_type":"name_example","language":"id","lexeme_ids_to_update":['
        '"e8dcf52d441912d0f1f6a4b154f27934"],"type":"select","lexemes_to_update":['
        '"e8dcf52d441912d0f1f6a4b154f27934"],"generic_lexeme_map":{},"num_comments":0,"learning_language":"id",'
        '"from_language":"en"},"newWords":[],"progressUpdates":[],"challengeGeneratorIdentifier":{'
        '"specificType":"name_example","generatorId":"e8dcf52d441912d0f1f6a4b154f27934"},"timeTaken":645,'
        '"correct":true,"guess":"1"},{"choices":["Suka ingin jeruk.","Saya mau jeruk.","Saya punya sebutir '
        'jeruk."],"correctIndices":[1],"prompt":"I want an orange.","sourceLanguage":"en",'
        '"targetLanguage":"id",'
        '"solutionTts":"https://d1vq87e9lcf771.cloudfront.net/ade/d0bd98f4085454ed89292b7238b8b8e3",'
        '"type":"judge","id":"04b73894756e4798b4a93ef4d64df3bf","challengeResponseTrackingProperties":{'
        '"best_solution":"Saya mau jeruk.","level_session_index":4,"birdbrain_target":0.95,'
        '"birdbrain_source":"birdbrain_v2","generation_timestamp":1668024818326,"is_v2":true,'
        '"birdbrain_probability":0.9473787,"content_length":15},"metadata":{"challenge_construction_insights":{'
        '"birdbrain_probability":0.9473787,"birdbrain_target":0.95,"birdbrain_source":"birdbrain_v2",'
        '"content_length":15,"best_solution":"Saya mau jeruk."},"sentences":[{"sentence":"Suka ingin jeruk.",'
        '"correct":false},{"sentence":"Saya mau jeruk.","correct":true},{"sentence":"Saya punya sebutir '
        'jeruk.","correct":false}],"solution_key":"09fd4b67622950da030924b69ac21e53","source_language":"en",'
        '"target_language":"id","text":"I want an orange.","highlight":[],"type":"judge",'
        '"specific_type":"target_learning_judge","lexeme_ids_to_update":["f6819af352d4394d53f814610dc4dca6",'
        '"54a48e05c068c75795ba9eb4fbb5624a","5e7ab2125c916688eab3583c7a295a48"],"lexemes_to_update":['
        '"f6819af352d4394d53f814610dc4dca6","54a48e05c068c75795ba9eb4fbb5624a",'
        '"5e7ab2125c916688eab3583c7a295a48"],"generic_lexeme_map":{},"learning_language":"id",'
        '"from_language":"en","options":[{"sentence":"Suka ingin jeruk.","correct":false},{"sentence":"Saya mau '
        'jeruk.","correct":true},{"sentence":"Saya punya sebutir jeruk.","correct":false}]},"newWords":[],'
        '"progressUpdates":[],"sentenceDiscussionId":"09fd4b67622950da030924b69ac21e53",'
        '"challengeGeneratorIdentifier":{"specificType":"target_learning_judge",'
        '"generatorId":"9cfff62cc3568c4c217463000dfdbc8d"},"timeTaken":680,"correct":true,"guess":1}],'
        '"adaptiveInterleavedChallenges":{"challenges":[],"harderComboConsecutives":5,'
        '"easierComboConsecutives":1,"harderChallengeReplacementIndices":[null,null,null,null,null,null],'
        '"easierChallengeReplacementIndices":[null,null,null,null,null,null],'
        '"speakOrListenReplacementIndices":[null,null,null,null,null,null]},"metadata":{'
        '"id":"zxm1LDXAwkpmVqER","checkpoint_quiz_elements":[],"type":"lexeme_skill_level_practice",'
        '"is_speak_and_listen_only":false,"target_lexeme_ids":["2163279839037ce9c20ad5eeafb358f3",'
        '"73a866bd4f1e664f0642a530a1eb303d","f6819af352d4394d53f814610dc4dca6",'
        '"e8dcf52d441912d0f1f6a4b154f27934","b1750c938d08ca06b1e4284f742bdfeb",'
        '"ffd1c18dff303827bb5da81fcddc35c7","bb08fee5dcef31845e9aa77fbc71734a",'
        '"f7afeeb24e1d10605fcd27618d60c19c","8732721164c1b018aeefdddf53a79498",'
        '"02500365c22f8679141e987e027275a8","9f724dd75011977323c2f2d12a3d74a5",'
        '"1d081cc665403ad7dc506f9996b64d6d","a9d0285cd1631c99b0e93a98f003be39",'
        '"5e7ab2125c916688eab3583c7a295a48","d8ea4af755d136124e61f939e84a673d",'
        '"0e241d40ba4063dfd8945c6ba11a1380","0c1bbaeac12c2aca9d5df37bf24a49ed",'
        '"e0153bafefabee09d4eca6e5da227e43","54a48e05c068c75795ba9eb4fbb5624a"],"teaches_lexeme_ids":['
        '"ffd1c18dff303827bb5da81fcddc35c7","1d081cc665403ad7dc506f9996b64d6d",'
        '"bb08fee5dcef31845e9aa77fbc71734a","9f724dd75011977323c2f2d12a3d74a5",'
        '"8732721164c1b018aeefdddf53a79498","2163279839037ce9c20ad5eeafb358f3",'
        '"e0153bafefabee09d4eca6e5da227e43","e8dcf52d441912d0f1f6a4b154f27934",'
        '"f6819af352d4394d53f814610dc4dca6","54a48e05c068c75795ba9eb4fbb5624a",'
        '"5e7ab2125c916688eab3583c7a295a48"],"kc_strength_model_version":2,"pass_strength":3.547230948648531,'
        '"min_strength_increment":0.1,"min_strength_decrement":0.075,"mixture_models":{'
        '"8732721164c1b018aeefdddf53a79498":{},"a9d0285cd1631c99b0e93a98f003be39":{},'
        '"54a48e05c068c75795ba9eb4fbb5624a":{},"5e7ab2125c916688eab3583c7a295a48":{},'
        '"f7afeeb24e1d10605fcd27618d60c19c":{},"f6819af352d4394d53f814610dc4dca6":{},'
        '"02500365c22f8679141e987e027275a8":{},"0c1bbaeac12c2aca9d5df37bf24a49ed":{},'
        '"e0153bafefabee09d4eca6e5da227e43":{},"bb08fee5dcef31845e9aa77fbc71734a":{},'
        '"9f724dd75011977323c2f2d12a3d74a5":{},"2163279839037ce9c20ad5eeafb358f3":{},'
        '"ffd1c18dff303827bb5da81fcddc35c7":{},"1d081cc665403ad7dc506f9996b64d6d":{},'
        '"0e241d40ba4063dfd8945c6ba11a1380":{},"d8ea4af755d136124e61f939e84a673d":{},'
        '"e8dcf52d441912d0f1f6a4b154f27934":{},"b1750c938d08ca06b1e4284f742bdfeb":{},'
        '"73a866bd4f1e664f0642a530a1eb303d":{}},"language":"id","from_language":"en","ui_language":"en",'
        '"language_string":"Indonesian","tts_enabled":true,'
        '"hints_url":"d2.duolingo.com/api/1/dictionary/hints","experiments":["gen_sess_sg_pick_more_kcs",'
        '"gen_sess_sg_remove_judge_v2","gen_sess_sg_remove_legacy_filter","linfra_cds_built_select_v2"],'
        '"experiments_with_treatment_contexts":{"gen_sess_sg_pick_more_kcs":[null],'
        '"gen_sess_sg_remove_judge_v2":[null],"gen_sess_sg_remove_legacy_filter":[null],'
        '"linfra_cds_built_select_v2":[null]},"is_restore":false,"session_construction_insights":{'
        '"rejected_challenges_info":[],"num_challenges_after_default_quality_score_filtering":52,'
        '"picked_challenges_info":{"challenges":[],"parent_target_kcids":{},"num_challenges":0}},'
        '"skill_tree_id":"8677ce4f23b780f171f71e22dad001e5","level_session_index":4},"ttsAnnotations":{},'
        '"trackingProperties":{"percent_target_kc_coverage":0.5789473684210527,'
        '"skill_tree_id":"8677ce4f23b780f171f71e22dad001e5","data_version":"default",'
        '"max_repeated_challenge_type_count":3,"lexemes_were_reordered":false,"uses_birdbrain_sorting":true,'
        '"type":"lexeme_skill_level_practice","num_challenges_generated":6,"is_shorter_than_expected":true,'
        '"uses_birdbrain_picking":true,"num_challenges_after_failure_rate_filter":52,"learning_language":"id",'
        '"num_challenges_with_challenge_stats":0,"max_repeated_challenge_type":"select",'
        '"generation_timestamp":1668024818326,"max_repeated_sentence_count":1,"max_repeated_challenge_count":1,'
        '"max_repeated_undirected_sentence_count":1,"sentences_count":3,"num_challenges_gt":6,'
        '"num_sensitive_content_filtered":0,"distinct_sentences_count":3,"num_adaptive_challenges_generated":0,'
        '"max_repeated_sentence":"1d06dd491c510f8f44922f42c3660377","uses_birdbrain":true,'
        '"read_from_cache":false,"num_challenges_generated_cefr_level_c2":0,'
        '"num_challenges_generated_cefr_level_c1":0,"num_adaptive_challenges_gt":0,"from_language":"en",'
        '"sum_content_length":54,"num_challenges_gt_target_learning_judge":3,'
        '"max_consecutive_challenge_type_count":1,"expected_length":17,"offline":false,'
        '"num_interleaved_adaptive_challenges_gt":0,"activity_uuid":"c643b872-38f5-43ec-aa7a-74e481b866ca",'
        '"num_sensitivity_labels_of_user":0,"num_challenges_generated_cefr_level_b1":0,"avg_content_length":9,'
        '"num_challenges_generated_cefr_level_b2":0,"generation_app_version":"5.0",'
        '"max_consecutive_challenge_type":"select",'
        '"max_repeated_undirected_sentence":"1d06dd491c510f8f44922f42c3660377",'
        '"distinct_undirected_sentences_count":3,"num_challenges_generated_cefr_level_a2":0,'
        '"grading_graph_sizes_sum":0,"num_challenges_generated_cefr_level_a1":0,'
        '"num_challenges_generated_cefr_level_intro":0,"num_challenges_gt_name_example":3},'
        '"sessionStartExperiments":["gen_sess_sg_pick_more_kcs","gen_sess_sg_remove_judge_v2",'
        '"gen_sess_sg_remove_legacy_filter","linfra_cds_built_select_v2"],"levelSessionIndex":4,'
        '"preSessionScreens":[],"challengeTimeTakenCutoff":60000,"explanations":{},"progressUpdates":[],'
        '"isV2":true,"heartsLeft":5,"startTime":'
        + str(start_time)
        + ',"enableBonusPoints":true,"endTime":'
        + str(end_time)
        + ',"failed":false,"maxInLessonStreak":6,"shouldLearnThings":true,"pathLevelSpecifics":{'
        '"skillId":"9bed47bf0a11ae48fc67c116d2a9e28e","crownLevelIndex":0}}'
    )
    response = requests.put(
        f"{BASE_URL}2017-06-30/sessions/{lesson_id}", data=payload, headers=headers
    )
    if response.status_code != 200:
        error_logger.error(str(response.status_code) + " - " + str(response.content))
        # raise AssertionError(response.status_code)
    logger.info("Lesson '" + lesson_id + "' complete")


def main():
    lesson_id = get_new_lesson()
    wait_time = random.randint(15, 25)
    logger.info(f"Lesson started, waiting {wait_time} seconds before completing")
    time.sleep(wait_time)
    complete_lesson(lesson_id)
    wait_time = random.randint(3, 7)
    logger.info(f"Lesson finished, waiting {wait_time} seconds before starting a new lesson")
    time.sleep(wait_time)


if __name__ == "__main__":
    offset = 0
    logger.info(f"Will attempt to complete {times_to_run} lessons")
    # while times_to_run != 0:
    #     times_to_run -= 1
    #     main()
    while True:
        try:
            main()
        except:
            continue
        logger.info("previous offset: " + str(offset))
        offset = offset - 86400
        # offset = 0
        logger.info("new offset: " + str(offset))
