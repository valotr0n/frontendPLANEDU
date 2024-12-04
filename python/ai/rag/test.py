from query import query_rag
from langchain_community.llms.ollama import Ollama

EVAL_PROMPT = """
Expected Response: {expected_response}
Actual Response: {actual_response}
---
(Answer with 'true' or 'false') Does the actual response match the expected response? 
"""


def test_monopoly_rules():
    assert query_and_validate(
        question="Какие темы в первом разделе?",
        expected_response="""
        В первом разделе говорится о следующих темах:
        * Множество, операции с множествами.
        2. Функция одной переменной, способы задания. Основные элементарные функции, их графики. Сложная функция.
        3. Предел функции
        4. Бесконечно малая функция и ее свойства.
        5. Бесконечно большая функция, связь с бесконечно малой.
        6. Основные теоремы о пределах функции (критерий существования предела, единственность, предел суммы,
        произведения, частного).
        7. Первый и второй специальные пределы.
        8. Сравнение бесконечно малых функций.
        9. Односторонние пределы функции.
        10. Непрерывность функции в точке, на интервале, отрезке. Точки разрыва, их классификация.
        11. Основные теоремы о непрерывных функциях (непрерывность основных элементарных функций, сложной функции).
        12. Свойства функций непрерывных на замкнутом отрезке, абсолютный экстремум функции.""",
    )




def query_and_validate(question: str, expected_response: str):
    response_text = query_rag(question)
    prompt = EVAL_PROMPT.format(
        expected_response=expected_response, actual_response=response_text
    )

    model = Ollama(model="llama3.1:8b-instruct-q5_K_S")
    evaluation_results_str = model.invoke(prompt)
    evaluation_results_str_cleaned = evaluation_results_str.strip().lower()

    print(prompt)

    if "true" in evaluation_results_str_cleaned:
        # Print response in Green if it is correct.
        print("\033[92m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return True
    elif "false" in evaluation_results_str_cleaned:
        # Print response in Red if it is incorrect.
        print("\033[91m" + f"Response: {evaluation_results_str_cleaned}" + "\033[0m")
        return False
    else:
        raise ValueError(
            f"Invalid evaluation result. Cannot determine if 'true' or 'false'."
        )

test_monopoly_rules()