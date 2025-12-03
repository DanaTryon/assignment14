import pytest
from pydantic import ValidationError
from uuid import uuid4
from app.schemas.calculation import CalculationCreate, CalculationUpdate

# --- validate_type ---
def test_calculation_invalid_type():
    with pytest.raises(ValidationError) as exc:
        CalculationCreate(
            type="invalidtype",  # not in CalculationType
            inputs=[1.0, 2.0],
            user_id=uuid4()
        )
    assert "Type must be one of" in str(exc.value)

# --- check_inputs_is_list ---
def test_calculation_inputs_not_list():
    with pytest.raises(ValidationError) as exc:
        CalculationCreate(
            type="addition",
            inputs="not-a-list",  # triggers check_inputs_is_list
            user_id=uuid4()
        )
    assert "Input should be a valid list" in str(exc.value)

# --- validate_inputs: too few numbers ---
def test_calculation_inputs_too_short():
    with pytest.raises(ValidationError) as exc:
        CalculationCreate(
            type="addition",
            inputs=[5],  # only one number
            user_id=uuid4()
        )
    # Just assert that it's a validation error on "inputs"
    assert "inputs" in str(exc.value)

# --- validate_inputs: division by zero ---
def test_calculation_division_by_zero():
    with pytest.raises(ValidationError) as exc:
        CalculationCreate(
            type="division",
            inputs=[10, 0],  # denominator zero
            user_id=uuid4()
        )
    assert "Cannot divide by zero" in str(exc.value)

# --- CalculationUpdate validator ---
def test_calculation_update_inputs_too_short():
    with pytest.raises(ValidationError) as exc:
        CalculationUpdate(inputs=[42])  # only one number
    assert "inputs" in str(exc.value)
