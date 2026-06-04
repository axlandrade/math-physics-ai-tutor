from subjects import build_subject_instruction, detect_subject


def test_detect_subject_physics() -> None:
    assert detect_subject("Como calcular a velocidade em queda livre?") == "physics"


def test_detect_subject_math() -> None:
    assert detect_subject("Resolva esta integral definida.") == "math"


def test_detect_subject_generic() -> None:
    assert detect_subject("Como organizar uma rotina de estudos?") == "generic"


def test_build_subject_instruction_fallback() -> None:
    instruction = build_subject_instruction("unknown")

    assert "não foi claramente identificado" in instruction
