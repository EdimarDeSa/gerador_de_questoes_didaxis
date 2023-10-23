from pathlib import Path
from pandas import ExcelFile, read_excel, DataFrame, Series
from pandas.errors import InvalidColumnName

from BackEndFunctions.Constants import ENGINE, CABECALHO_DIDAXIS, CABECALHO_PERGUNTA, CABECALHO_ALTERNATIVAS, CORRETA, V


class AbrirArquivo:
    def _open_excel(self, path: Path) -> DataFrame | Exception | InvalidColumnName:
        """
        Abre um arquivo Excel e retorna um DataFrame ou uma exceção em caso de erro.

        Opens an Excel file and returns a DataFrame or an exception in case of an error.

        :param path: O caminho para o arquivo Excel.
        :return: Um DataFrame ou uma excessão.
        """
        try:
            with ExcelFile(path, engine=ENGINE) as xls:
                df = read_excel(xls, dtype='string', keep_default_na=False)
        except Exception as err:
            return Exception(err)

        return df

    @staticmethod
    def _split_questions(df: DataFrame) -> list[DataFrame]:
        """
        Divide o DataFrame em uma lista_serial de DataFrames, agrupados por 'PERGUNTA'.

        Splits the DataFrame into a list of DataFrames, grouped by 'PERGUNTA'.

        :param df: O DataFrame a ser dividido.
        :return: Uma lista_serial de DataFrames.
        """

        grup = df.groupby('PERGUNTA')
        return [grupo for _, grupo in grup]

    @staticmethod
    def _split_question_parameters(question: DataFrame) -> dict:
        """
        Extrai os parâmetros da questão.

        Extracts the parameters of the question.

        :param question: O DataFrame de uma questão.
        :return: Um dicionário com os parâmetros da questão.
        """
        return question[CABECALHO_PERGUNTA].iloc[0].to_dict()

    @staticmethod
    def _normalize_keys(to_normalize: dict) -> dict:
        """
        Normaliza as chaves do dicionário para letras minúsculas.

        Normalizes dictionary keys to lowercase.

        :param to_normalize: Um dicionário a ser normalizado.
        :return: Um dicionário com chaves em letras minúsculas.
        """
        return {key.lower(): value for key, value in to_normalize.items()}
    
    def _normalize_choices(self, choices: list) -> list[tuple[str, bool]]:
        """
        Normaliza as escolhas das questões.

        Normalizes question choices.

        :param choices: Uma lista_serial de escolhas de questão.
        :return: Uma lista_serial de tuplas (alternativa: str, correto: bool).
        """

        return [(alternativa, self._verifies_correct(correta)) for alternativa, correta in choices]

    def _split_question_choices(self, question: DataFrame) -> list[tuple[str, bool]]:
        """
        Divide as alternativas da questão.

        Divide the alternatives of the question.

        :param question: O DataFrame de uma questão.
        :return: Um dicionário com as alternativas da questão em formato de lista_serial de tuplas com uma string e um booleano.
        """

        choices = question[CABECALHO_ALTERNATIVAS].values.tolist()

        return self._normalize_choices(choices)

    def _serialize_questions(self, question_list: list[DataFrame]) -> list[dict]:
        """
        Serializa as questões em uma lista_serial de dicionários.

        Serializes the questions into a list of dictionaries.

        :param question_list: Uma lista_serial de DataFrames de questões.
        :return: Uma lista_serial de dicionários serializados.
        """

        serials = []
        for question in question_list:
            serial_dict = self._split_question_parameters(question)
            alternativas = self._split_question_choices(question)

            serial_dict['alternativas'] = alternativas
            normalized_serial_dict = self._normalize_keys(serial_dict)

            serials.append(normalized_serial_dict)

        return serials

    @staticmethod
    def _verifies_correct(correct: str) -> bool:
        """Verifica se a resposta é 'CORRETA' ou 'V'.

        Verify if the string is 'CORRETA' or 'V'."""
        return correct in [CORRETA, V]

    @staticmethod
    def _verify_columns(columns: list) -> None:
        """
        Verifica se o DataFrame tem as mesmas colunas do CABECALHO_DIDAXIS.
        Retorna True se as colunas coincidirem, False caso contrário.

        Checks if the DataFrame has the same columns as CABECALHO_DIDAXIS.
        Returns True if the columns match, False otherwise.
        """

        if columns != CABECALHO_DIDAXIS:
            raise InvalidColumnName(f'O arquivo não contem as colunas necessárias:\n'
                                    f'{CABECALHO_DIDAXIS}')

    def open(self, path: str):
        """
        Função principal para abrir e serializar questões de um arquivo Excel.

        Application function to open and serialize questions from an Excel file.

        :return: Uma lista_serial de questões serializadas ou uma exceção.
        """

        if not path:
            raise FileNotFoundError('Não foi possível encontrar o arquivo.')

        abs_path = Path(path).resolve()

        data_frame = self._open_excel(abs_path)

        self._verify_columns(data_frame.columns.to_list())

        question_list = self._split_questions(data_frame)

        return self._serialize_questions(question_list)
