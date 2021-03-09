import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from typing import List, Tuple

class DFWrapper:
    def __init__(self, df: pd.DataFrame, target: str, tfidf=False, fasttext=False) -> None:
        """
        Принимает датафрейм, где все колонки содержат или числа, или строки,
        таргет, который будет использован для классификации
        """
        self.df = df.drop(target, axis=1)
        self.target = df[target]
        if not tfidf and not fasttext:
            self.vectorizer = CountVectorizer
        elif tfidf:
            self.vectorizer = TfidfVectorizer
        elif fasttext:
            self.vectorizer = "fasttext"
        self.__modify_df()

    @property
    def features(self) -> pd.DataFrame:
        """
        Возвращает подготовленный к классификации датафрейм,
        где строковые колонки или закодированы one-hot, или векторизованы
        """
        return self.df

    def fit(self, model):
        """
        Обучение модели
        """
        m = model()
        m.fit(self.df, self.target)
        return m

    def __select_columns(self) -> Tuple[List[str], List[str]]:
        """
        По количеству уникальных значений в колонке
        функция отбирает какие колонки закодировать one-hot,
        а какие нужно векторизовать.
        Возвращает 2 списка названий колонок: для one-hot и для векторизации
        """
        one_hot_columns = []
        vect_columns = []
        unique_value_threshold = self.df.shape[0] * 0.01

        for column in self.df.columns:
            if type(self.df[column][0]) is str:
                if self.df[column].unique().shape[0] < unique_value_threshold:
                    one_hot_columns.append(column)
                else:
                    vect_columns.append(column)
        return one_hot_columns, vect_columns

    def __apply_one_hot(self, one_hot_columns: List[str]) -> pd.DataFrame:
        """
        Принимает список названий колонок и применяет к ним one-hot кодирование.
        Возвращает датафрейм
        """
        encoder = OneHotEncoder(sparse=False)
        values = encoder.fit_transform(self.df[one_hot_columns])
        return pd.DataFrame(values, columns=encoder.get_feature_names())

    def __apply_vectorizer(self, vect_columns: List[str]) -> pd.DataFrame:
        """
        Принимает список названий колонок и применяет к ним векторизацию.
        Возвращает датафрейм
        """
        concatenated_columns = self.df[vect_columns[0]]
        for column in vect_columns[1:]:
            concatenated_columns = concatenated_columns + " " + self.df[column]

        vect = self.vectorizer()
        values = vect.fit_transform(concatenated_columns).toarray()
        return pd.DataFrame(values, columns=vect.get_feature_names())

    def __make_embeddings(self, string: str) -> np.array:
        """
        Принимает строку и возвращает усредненный вектор эмбеддинга фасттекста
        """
        res = []
        # конечно нужно бы токенизировать по-хорошему
        for word in string.split():
            try:
                res.append(fast_text_model.word_vec(word))
            except AttributeError:
                continue
        return np.array(res).mean(axis=0)

    def __apply_fasttext(self, vect_columns: List[str]) -> None:
        """
        Принимает список названий колонок и переводит их в эмбеддинги фасттекста.
        """
        for column in vect_columns:
            self.df[column] = self.df[column].apply(self.__make_embeddings)

    def __modify_df(self) -> None:
      """
      Применяет к исходному датафрейму one-hot кодирование и векторизацию.
      """
      one_hot_columns, vect_columns = self.__select_columns()
      one_hot_df = self.__apply_one_hot(one_hot_columns)
      if self.vectorizer != "fasttext":
          vectorized_df = self.__apply_vectorizer(vect_columns)
          self.df = pd.concat((self.df, one_hot_df, vectorized_df), axis=1)
          self.df.drop(one_hot_columns + vect_columns, axis=1, inplace=True)
      else:
          self.__apply_fasttext(vect_columns)
          self.df = pd.concat((self.df, one_hot_df), axis=1)
          self.df.drop(one_hot_columns, axis=1, inplace=True)