from pathlib import Path
from tkinter.filedialog import askopenfilename
from pandas import ExcelFile, read_excel, DataFrame, Series
from pandas.errors import InvalidColumnName

from ..constants import (ENGINE, OFF, CABECALHO_DIDAXIS, CABECALHO_PERGUNTA, CABECALHO_ALTERNATIVAS, CORRETA, V,
                         EXTENSIONS, FILETYPES)


__all__ = ['get_desktop_path', 'abrir']


def get_desktop_path() -> Path:
    """
    Retorna o caminho do diretório de desktop do usuário.

    Returns the user's desktop directory path.
    """
    return Path.home() / "Desktop"


def _open_excel(path: Path) -> DataFrame | Exception | InvalidColumnName:
    """
    Abre um arquivo Excel e retorna um DataFrame ou uma exceção em caso de erro.

    Opens an Excel file and returns a DataFrame or an exception in case of an error.

    :param path: O caminho para o arquivo Excel.
    :return: Um DataFrame ou uma excessão.
    """
    try:
        with ExcelFile(path, engine=ENGINE) as xls:
            df = read_excel(xls, dtype='string', keep_default_na=OFF)
    except Exception as err:
        return Exception(err)

    if not _verify_columns(df.columns):
        raise InvalidColumnName(f'O arquivo Excel não tem as colunas necessárias: {CABECALHO_DIDAXIS}')
    return df


def _split_questions(df: DataFrame) -> list[DataFrame]:
    """
    Divide o DataFrame em uma lista_serial de DataFrames, agrupados por 'PERGUNTA'.

    Splits the DataFrame into a list of DataFrames, grouped by 'PERGUNTA'.

    :param df: O DataFrame a ser dividido.
    :return: Uma lista_serial de DataFrames.
    """
    grup = df.groupby('PERGUNTA')
    return [grupo for _, grupo in grup]


def _split_question_parameters(question: DataFrame) -> dict:
    """
    Extrai os parâmetros da questão.

    Extracts the parameters of the question.

    :param question: O DataFrame de uma questão.
    :return: Um dicionário com os parâmetros da questão.
    """
    return question[CABECALHO_PERGUNTA].iloc[0].to_dict()


def _normalize_keys(to_normalize: dict) -> dict:
    """
    Normaliza as chaves do dicionário para letras minúsculas.

    Normalizes dictionary keys to lowercase.

    :param to_normalize: Um dicionário a ser normalizado.
    :return: Um dicionário com chaves em letras minúsculas.
    """
    return {key.lower(): value for key, value in to_normalize.items()}


def _normalize_choices(choices: list) -> list[tuple[str, bool]]:
    """
    Normaliza as escolhas das questões.

    Normalizes question choices.

    :param choices: Uma lista_serial de escolhas de questão.
    :return: Uma lista_serial de tuplas (alternativa: str, correto: bool).
    """
    return [(alternativa, _verifies_correct(correta)) for alternativa, correta in choices]


def _split_question_choices(question: DataFrame) -> dict[str, list[tuple[str, bool]]]:
    """
    Divide as alternativas da questão.

    Divide the alternatives of the question.

    :param question: O DataFrame de uma questão.
    :return: Um dicionário com as alternativas da questão em formato de lista_serial de tuplas com uma string e um booleano.
    """
    choices = question[CABECALHO_ALTERNATIVAS].values.tolist()
    normalized_choices = _normalize_choices(choices)
    return dict(alternativas=normalized_choices)


def _serialize_questions(question_list: list[DataFrame]) -> list[dict]:
    """
    Serializa as questões em uma lista_serial de dicionários.

    Serializes the questions into a list of dictionaries.

    :param question_list: Uma lista_serial de DataFrames de questões.
    :return: Uma lista_serial de dicionários serializados.
    """
    serials = []
    for question in question_list:
        serial_dict = _split_question_parameters(question)
        alternativas = _split_question_choices(question)
        serial_dict.update(alternativas)
        serial_dict = _normalize_keys(serial_dict)
        serials.append(serial_dict)
    return serials


def _verifies_correct(correct: str) -> bool:
    """Verifica se a resposta é 'CORRETA' ou 'V'.

    Verify if the string is 'CORRETA' or 'V'."""
    return correct in [CORRETA, V]


def _verify_columns(columns: Series) -> bool:
    """
    Verifica se o DataFrame tem as mesmas colunas do CABECALHO_DIDAXIS.
    Retorna True se as colunas coincidirem, False caso contrário.

    Checks if the DataFrame has the same columns as CABECALHO_DIDAXIS.
    Returns True if the columns match, False otherwise.
    """
    colunas_do_dataframe = columns.to_list()
    colunas_do_dataframe.sort()
    columns = CABECALHO_DIDAXIS.copy()
    columns.sort()
    return colunas_do_dataframe == columns


def abrir() -> list[dict] | FileNotFoundError | None:
    """
    Função principal para abrir e serializar questões de um arquivo Excel.

    Main function to open and serialize questions from an Excel file.

    :return: Uma lista_serial de questões serializadas ou uma exceção.
    """
    path = askopenfilename(defaultextension=EXTENSIONS, filetypes=FILETYPES, initialdir=get_desktop_path())

    if not path:
        raise FileNotFoundError('Não foi possível encontrar o arquivo.')

    path = Path(path).resolve()
    try:
        data_frame = _open_excel(path)
    except InvalidColumnName as err:
        raise InvalidColumnName(err)

    question_list = _split_questions(data_frame)
    serialized_questions = _serialize_questions(question_list)
    return serialized_questions
