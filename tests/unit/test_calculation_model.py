import pytest
import uuid
from app.models.calculation import Addition, Subtraction, Multiplication, Division, AbstractCalculation

# --- Addition ---
def test_addition_inputs_not_list():
    calc = Addition(user_id=uuid.uuid4(), inputs="not-a-list")
    with pytest.raises(ValueError) as exc:
        calc.get_result()
    assert "Inputs must be a list" in str(exc.value)

def test_addition_inputs_too_short():
    calc = Addition(user_id=uuid.uuid4(), inputs=[5])
    with pytest.raises(ValueError) as exc:
        calc.get_result()
    assert "at least two numbers" in str(exc.value)

# --- Subtraction ---
def test_subtraction_inputs_not_list():
    calc = Subtraction(user_id=uuid.uuid4(), inputs="not-a-list")
    with pytest.raises(ValueError):
        calc.get_result()

def test_subtraction_inputs_too_short():
    calc = Subtraction(user_id=uuid.uuid4(), inputs=[10])
    with pytest.raises(ValueError):
        calc.get_result()

# --- Multiplication ---
def test_multiplication_inputs_not_list():
    calc = Multiplication(user_id=uuid.uuid4(), inputs="not-a-list")
    with pytest.raises(ValueError):
        calc.get_result()

def test_multiplication_inputs_too_short():
    calc = Multiplication(user_id=uuid.uuid4(), inputs=[2])
    with pytest.raises(ValueError):
        calc.get_result()

# --- Division ---
def test_division_by_zero():
    calc = Division(user_id=uuid.uuid4(), inputs=[10, 0])
    with pytest.raises(ValueError) as exc:
        calc.get_result()
    assert "Cannot divide by zero" in str(exc.value)

# --- AbstractCalculation factory ---
def test_create_invalid_type():
    with pytest.raises(ValueError) as exc:
        AbstractCalculation.create("invalidtype", uuid.uuid4(), [1, 2])
    assert "Unsupported calculation type" in str(exc.value)
