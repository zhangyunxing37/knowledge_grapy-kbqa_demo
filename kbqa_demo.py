# coding: utf-8
import sys
sys.path.append(r"C:\Users\z50004593\Desktop\model\python_py")
from entity_find import EntityExtractor
from intent_find import Question_intent
from sql_create import Aearch_answer
import warnings
warnings.filterwarnings('ignore')

class KBQA:
    def __init__(self):
        self.extractor = EntityExtractor()
        self.intent = Question_intent()
        self.sql = Aearch_answer()

    def qa_main(self, input_str):
        answer = "对不起，您的问题我不知道，我今后会努力改进的。"
        entities = self.extractor.entity_reg(input_str)
        # print(entities)
        if not entities:
            return answer
        intent=self.intent.query_intent(input_str)
        #print(intent)
        if not str(intent):
            return answer
        sqls = self.sql.transfor_to_sql(entities, intent)
        final_answer = self.sql.answer(sqls)
        # print(final_answer)
        if not final_answer:
            return answer
        else:
            return '\n'.join(final_answer)


handler = KBQA()
while True:
    question = input("用户：")
    if not question:
        break
    qqa = handler.qa_main(question)
    print("小刘：", qqa)
    print("*"*50, '\n')


