import argparse
from PyKomoran import *
from HW2_util import NLP_util

class HW2(NLP_util):
        
    def tokenize(self, data):
        komoran = Komoran("EXP")
        text = [data[n]['form'] for n in range(len(data))]
        tokens = []
        for t in text :
            token = komoran.get_list(t)
            token = [str(x) for x in token]
            tokens.append(token)
        return (text, tokens)
   
    def make_word2idx(self, data):
        origin, tokens = data[0], data[1]
        w2i = []
        for token in tokens :
            word2idx = sorted(set(token))[::-1]
            word2idx += ['<UNK']
            word2idx += ['<PAD>']

            word2idx = word2idx[::-1]
            word2idx = {word : idx for idx, word in enumerate(word2idx)}
            w2i.append(word2idx)

        return w2i

    def convert_tokens_to_idx(self, data):
        origin, tokens = data[0], data[1]
        word2idx = self.make_word2idx(data)
        idx_list = []
        for i in range(len(tokens)) :
            idx = [word2idx[i][tokens[i][t]] for t in range(len(tokens[i]))]
            idx_list.append(idx)

        return (origin, tokens, idx_list)

    def result(self, data, num) :
        token_list = []
        idx_list = []
        target_text, target_pos, target_idx = data[0][num], data[1][num], data[2][num]
        for i, v in enumerate(zip(target_pos, target_idx)) :
            if v[0].split('/')[1] in ['NNP', 'NNG', 'VV'] :
                token_list.append(v[0])
                idx_list.append(v[1])
            else :
                pass
        return (target_text, token_list, idx_list)

    def save_result(self, std_num, std_name, data, num):
        with open("./" + str(std_num) + "_" + str(std_name)+"_hw2.txt", mode='w', encoding="UTF-8", errors="ignore") as out:
            out.write("Text Num : {0}\n".format(num)) 
            out.write("Original Text : {0}\n".format(data[0]))
            out.write("Tokenized Text : {0}\n".format(data[1]))
            out.write("idx : {0}\n".format(data[2]))
            out.close()
        
if __name__ == "__main__":
    # 학번과 이름 외, 다른 코드는 수정하지 마시길 바랍니다
    parser = argparse.ArgumentParser()
    parser.add_argument("--print_examples", type=int, default=1)
    args = parser.parse_args()

    util = HW2()

    # 01. 데이터 불러오기
    data = util.load_data(path = "./NLP_train_6000.json")

    # 02. 데이터 형태소 분석
    tokenized_data = util.tokenize(data = data)

    # 03. word2idx 생성
    util.make_word2idx(data=tokenized_data)

    # 04. Convert token to idx
    converted_data = util.convert_tokens_to_idx(data=tokenized_data)

    # 05. 명사와 동사(Tag : NNP, NNG, VV) 토큰과 idx만 추출
    selected_data = util.result(data=converted_data, num=args.print_examples)

    # 06. 결과 저장(.txt)
    util.save_result(std_num='학번', std_name="이름", data=selected_data, num=args.print_examples)