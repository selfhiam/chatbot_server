import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset
from transformers.optimization import AdamW, get_cosine_schedule_with_warmup
from transformers import PreTrainedTokenizerFast, GPT2LMHeadModel
import re
import zipfile
import os

parents = 0

Q_TKN = "<usr>"
A_TKN = "<sys>"
L_TKN = "<label>"
BOS = '</s>'
EOS = '</s>'
MASK = '<unused0>'
SENT = '<unused1>'
PAD = '<pad>'

koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
            bos_token=BOS, eos_token=EOS, unk_token='<unk>',
            pad_token=PAD, mask_token=MASK)
model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
# 저장된 모델 상태를 불러오기
checkpoint = torch.load('./chatjjock.pth', map_location=torch.device('cpu'))

model.load_state_dict(checkpoint)

class ChatbotDataset(Dataset):
    def __init__(self, chats, max_len=50):  # 데이터셋의 전처리를 해주는 부분
        self._data = chats
        self.max_len = max_len
        self.q_token = Q_TKN
        self.a_token = A_TKN
        self.l_token = L_TKN
        self.sent_token = SENT
        self.eos = EOS
        self.mask = MASK
        self.tokenizer = koGPT2_TOKENIZER

    def __len__(self):  # chatbotdata 의 길이를 리턴한다.
        return len(self._data)

    def __getitem__(self, idx):  # 로드한 챗봇 데이터를 차례차례 DataLoader로 넘겨주는 메서드
        turn = self._data.iloc[idx]
        l = str(turn["1"])

        q = turn["Q"]  # 질문을 가져온다.
        q = re.sub(r"([?.!,~])", r" ", q)  # 구둣점들을 제거한다.
        q = re.sub(r'([ㄱ-ㅎㅏ-ㅣ])\1+', r'\1', q) # 자음이나 모음만 연속되는 것 한개만 남기고 삭제

        a = turn["A"]  # 답변을 가져온다.
        a = re.sub(r"([?.!,])", r" ", a)  # 구둣점들을 제거한다.
        a = re.sub(r'([ㄱ-ㅎㅏ-ㅣ])\1+', r'\1', a) # 자음이나 모음만 연속되는 것 한개만 남기고 삭제

        l_toked = self.tokenizer.tokenize(self.l_token + l + self.sent_token)
        l_len = len(l_toked)

        q_toked = self.tokenizer.tokenize(self.q_token + q + self.sent_token)
        q_len = len(q_toked)

        t_toked = (l_toked + q_toked)
        t_len = len(t_toked)

        a_toked = self.tokenizer.tokenize(self.a_token + a + self.eos)
        a_len = len(a_toked)


        #질문의 길이가 최대길이보다 크면
        if t_len > self.max_len:
            a_len = self.max_len - t_len        #답변의 길이를 최대길이 - 질문길이
            if a_len <= 0:       #질문의 길이가 너무 길어 질문만으로 최대 길이를 초과 한다면
                t_toked = t_toked[-(int(self.max_len / 2)) :]   #질문길이를 최대길이의 반으로
                t_len = len(t_toked)
                a_len = self.max_len - t_len              #답변의 길이를 최대길이 - 질문길이
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)

        #질문의 길이 + 답변의 길이가 최대길이보다 크면
        if t_len + a_len > self.max_len:
            a_len = self.max_len - t_len        #답변의 길이를 최대길이 - 질문길이
            if a_len <= 0:       #질문의 길이가 너무 길어 질문만으로 최대 길이를 초과 한다면
                t_toked = t_toked[-(int(self.max_len / 2)) :]   #질문길이를 최대길이의 반으로
                t_len = len(t_toked)
                a_len = self.max_len - t_len              #답변의 길이를 최대길이 - 질문길이
            a_toked = a_toked[:a_len]
            a_len = len(a_toked)


        # 답변 labels = [mask, mask, ...., mask, ..., <bos>,..답변.. <eos>, <pad>....]
        labels = [self.mask,] * t_len + a_toked[1:]

        # mask = 질문길이 0 + 답변길이 1 + 나머지 0
        mask = [0] * t_len + [1] * a_len + [0] * (self.max_len - t_len - a_len)
        # 답변 labels을 index 로 만든다.
        labels_ids = self.tokenizer.convert_tokens_to_ids(labels)
        # 최대길이만큼 PADDING
        while len(labels_ids) < self.max_len:
            labels_ids += [self.tokenizer.pad_token_id]

        # 질문 + 답변을 index 로 만든다.
        token_ids = self.tokenizer.convert_tokens_to_ids(l_toked + q_toked + a_toked)
        # 최대길이만큼 PADDING
        while len(token_ids) < self.max_len:
            token_ids += [self.tokenizer.pad_token_id]

        #질문+답변, 마스크, 답변
        return (token_ids, np.array(mask), labels_ids)

def Parents(parents):
    global parent
    parent = parents

ans = '저한테 말씀을 해주세요.'

def getAnswer(question):
    pattern = r"^[ㄱ-ㅎㅏ-ㅣ가-힣]*$"
    p = re.compile(pattern)
    with torch.no_grad():
        t = question.strip()
        
        # elif not (p.match(question)):
        #     return ans
        l = t[0]
        q = t[1:]
        q = re.sub(r"([?.!,~])", r" ", q)  # 구둣점들을 제거한다.
        q = re.sub(r'([ㄱ-ㅎㅏ-ㅣ])\1+', r'\1', q) # 자음이나 모음만 연속되는 것 한개만 남기고 삭제
        q = q.strip()
        if len(q) < 1:
            return ans
        a = ""
        while 1:
            input_ids = torch.LongTensor(koGPT2_TOKENIZER.encode(L_TKN + l + SENT + Q_TKN + q + SENT + 'sent' + A_TKN + a)).unsqueeze(dim=0)
            pred = model(input_ids)
            pred = pred.logits
            gen = koGPT2_TOKENIZER.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().cpu().numpy().tolist())[-1]
            if gen == EOS:
                break
            a += gen.replace("▁", " ")
        a = a.strip()
        if parent == 1:
            a = a.replace('엄빠', '엄마')
        elif parent == 2:
            a = a.replace('엄빠', '아빠')
        if l == "9" or l == "5":
          count = a.split()
          if len(count) == 1:
            a += '....'
          a = re.sub(r"\s{2,}", "....", a)
        if l == "4" or l == "8" or l == '3':
          count = a.split()
          if len(count) == 1:
            a += '!'
          a = re.sub(r"\s{2,}", "!", a)
        a = re.sub(r'([ㄱ-ㅎㅏ-ㅣ])', r'\1\1', a)
        return a
    