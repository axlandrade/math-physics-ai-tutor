# app/subjects.py

def detect_subject(user_message: str) -> str:
    """
    Heurística simples para detectar se a pergunta é sobre Matemática,
    Física ou genérica. Pode ser refinada depois.
    """
    text = user_message.lower()

    physics_keywords = [
        "velocidade", "aceleração", "força", "trabalho", "energia",
        "cinemática", "dinâmica", "campo elétrico", "campo magnético",
        "corrente", "circuito", "lente", "óptica", "onda", "movimento",
        "queda livre", "newton", "lei de newton", "impulso", "momento"
    ]

    math_keywords = [
        "função", "derivada", "integral", "limite", "matriz",
        "determinante", "equação", "inequação", "log", "logaritmo",
        "progressão", "probabilidade", "estatística", "seno",
        "cosseno", "tangente", "trigonometria", "polinômio",
        "série", "somatório", "produto escalar", "vetor"
    ]

    if any(k in text for k in physics_keywords):
        return "physics"
    if any(k in text for k in math_keywords):
        return "math"
    return "generic"


def build_subject_instruction(subject: str) -> str:
    """
    Instrução extra para o modelo, dependendo da área.
    """
    if subject == "physics":
        return (
            "O assunto identificado é FÍSICA. "
            "Dê atenção especial às unidades, dimensões físicas e "
            "interpretação conceitual dos resultados.\n"
        )
    elif subject == "math":
        return (
            "O assunto identificado é MATEMÁTICA. "
            "Dê atenção especial às propriedades algébricas, gráficos e "
            "interpretação geométrica quando fizer sentido.\n"
        )
    else:
        return (
            "O assunto não foi claramente identificado como Matemática ou Física. "
            "Tente, se possível, relacionar a questão com conceitos dessas áreas.\n"
        )
