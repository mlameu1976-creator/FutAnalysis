import os
import pytest

# ⚠️ Marcação para rodar só quando você quiser
pytestmark = pytest.mark.integration


def test_real_team_summary(client):
    """
    Teste REAL usando API-Football.
    Usa um time conhecido (ex: Manchester United = 33).
    """

    response = client.get(
        "/analysis/team/33/summary?limit=5"
    )

    assert response.status_code == 200

    data = response.json()

    assert "team_id" in data
    assert "summary" in data

    summary = data["summary"]

    assert summary["played"] > 0
    assert "wins" in summary
    assert "draws" in summary
    assert "losses" in summary


def test_real_advanced_prediction(client):
    """
    Teste REAL da predição avançada.
    """

    response = client.get(
        "/analysis/team/33/advanced-prediction?limit=5&is_home=true"
    )

    assert response.status_code == 200

    prediction = response.json()["prediction"]

    assert 0 <= prediction["win"] <= 100
    assert 0 <= prediction["draw"] <= 100
    assert 0 <= prediction["loss"] <= 100
    assert 0 <= prediction["confidence"] <= 100
