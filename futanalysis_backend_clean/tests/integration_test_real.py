import requests

BASE_URL = "http://127.0.0.1:8000"

def test_team_summary():
    print("🔍 Testando summary com dados reais...")
    r = requests.get(f"{BASE_URL}/analysis/team/33/summary?limit=5")
    r.raise_for_status()
    data = r.json()
    print("✅ Summary OK")
    print(data)

def test_advanced_prediction():
    print("\n🔍 Testando advanced prediction com dados reais...")
    r = requests.get(
        f"{BASE_URL}/analysis/team/33/advanced-prediction?limit=5&is_home=true"
    )
    r.raise_for_status()
    data = r.json()
    print("✅ Advanced Prediction OK")
    print(data)

if __name__ == "__main__":
    print("🚀 Iniciando testes de integração REAL\n")
    test_team_summary()
    test_advanced_prediction()
    print("\n🎉 Todos os testes passaram com dados reais")
