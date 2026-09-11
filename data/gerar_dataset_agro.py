import csv
import random
from datetime import date

random.seed(42)

OUT_DIR = r"C:\Users\fonta\Desktop\portfolio_powerbi\agro_analytics"

# Fictional dataset — no real Timac Agro customer/farmer data. City names are
# real Brazilian agro hubs used only for geographic plausibility of the map.
STATE_INFO = {
    "MT": {"lat": (-7.5, -17.0), "lon": (-50.5, -60.5), "cidades": ["Sorriso", "Sinop", "Lucas do Rio Verde", "Campo Novo do Parecis"],
           "culturas": ["Soja", "Milho", "Algodão"]},
    "GO": {"lat": (-12.5, -18.8), "lon": (-46.5, -52.8), "cidades": ["Rio Verde", "Jataí", "Cristalina", "Montividiu"],
           "culturas": ["Soja", "Milho"]},
    "PR": {"lat": (-22.7, -26.3), "lon": (-48.3, -54.2), "cidades": ["Cascavel", "Toledo", "Ponta Grossa", "Guarapuava"],
           "culturas": ["Soja", "Milho", "Trigo"]},
    "RS": {"lat": (-27.3, -33.2), "lon": (-49.8, -57.2), "cidades": ["Passo Fundo", "Cruz Alta", "Não-Me-Toque", "Santa Rosa"],
           "culturas": ["Soja", "Trigo", "Milho"]},
    "SP": {"lat": (-20.3, -24.8), "lon": (-44.8, -52.8), "cidades": ["Ribeirão Preto", "São Carlos", "Araraquara", "Franca"],
           "culturas": ["Cana-de-açúcar", "Café", "Milho"]},
    "MG": {"lat": (-14.8, -22.2), "lon": (-40.0, -50.8), "cidades": ["Patrocínio", "Araguari", "Patos de Minas", "Varginha"],
           "culturas": ["Café", "Milho", "Soja"]},
    "BA": {"lat": (-9.0, -18.2), "lon": (-38.0, -46.2), "cidades": ["Luís Eduardo Magalhães", "Barreiras", "São Desidério"],
           "culturas": ["Algodão", "Soja", "Cana-de-açúcar"]},
    "MS": {"lat": (-17.8, -23.8), "lon": (-51.5, -57.8), "cidades": ["Maracaju", "Dourados", "Chapadão do Sul"],
           "culturas": ["Soja", "Milho", "Cana-de-açúcar"]},
    "TO": {"lat": (-5.8, -13.2), "lon": (-46.3, -50.2), "cidades": ["Pedro Afonso", "Formoso do Araguaia", "Gurupi"],
           "culturas": ["Soja", "Milho"]},
}

AREA_RANGE = {
    "Soja": (60, 850), "Milho": (50, 700), "Algodão": (100, 900),
    "Café": (8, 65), "Cana-de-açúcar": (150, 1600), "Trigo": (50, 400),
}

FERT_POR_CULTURA = {
    "Soja": ["NPK", "Cloreto de Potássio", "Superfosfato Simples"],
    "Milho": ["Ureia", "NPK", "Cloreto de Potássio"],
    "Algodão": ["NPK", "Ureia", "Cloreto de Potássio"],
    "Café": ["NPK", "Ureia", "Superfosfato Simples"],
    "Cana-de-açúcar": ["Ureia", "NPK", "Superfosfato Simples"],
    "Trigo": ["NPK", "Superfosfato Simples", "Ureia"],
}

TAXA_HA_TON = {  # toneladas de fertilizante por hectare/ano, aproximado por cultura
    "Soja": 0.28, "Milho": 0.35, "Algodão": 0.32,
    "Café": 0.55, "Cana-de-açúcar": 0.40, "Trigo": 0.22,
}

CUSTO_TON_BRL = {
    "NPK": 3200, "Ureia": 2800, "Cloreto de Potássio": 3600, "Superfosfato Simples": 2100,
}

# meses de safra com maior aplicação (pico) por cultura — simula sazonalidade
PICO_MES = {
    "Soja": [9, 10, 11], "Milho": [1, 2, 9], "Algodão": [10, 11, 12],
    "Café": [9, 10, 2], "Cana-de-açúcar": [3, 4, 9], "Trigo": [5, 6],
}

NOMES = ["João", "Maria", "Carlos", "Ana", "Pedro", "Luiza", "Marcos", "Fernanda", "Rafael", "Camila",
         "Eduardo", "Patrícia", "Rodrigo", "Juliana", "Gustavo", "Beatriz", "Fábio", "Renata", "André", "Larissa",
         "Bruno", "Aline", "Diego", "Vanessa", "Thiago", "Priscila", "Leonardo", "Débora", "Vinícius", "Simone"]
SOBRENOMES = ["Silva", "Souza", "Oliveira", "Pereira", "Costa", "Almeida", "Ferreira", "Rodrigues", "Martins",
              "Barbosa", "Ribeiro", "Carvalho", "Gomes", "Lima", "Araújo", "Machado", "Teixeira", "Nogueira"]

estados = list(STATE_INFO.keys())

agricultores = []
talhoes = []
agricultor_id = 1
talhao_id = 1

for estado in estados:
    info = STATE_INFO[estado]
    n_agricultores = random.randint(7, 10)
    for _ in range(n_agricultores):
        nome = f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"
        cidade = random.choice(info["cidades"])
        lat_c = random.uniform(*info["lat"])
        lon_c = random.uniform(*info["lon"])
        cliente_desde = date(random.randint(2015, 2023), random.randint(1, 12), 1)
        agricultores.append({
            "AgricultorID": agricultor_id, "Nome": nome, "Estado": estado, "Municipio": cidade,
            "Latitude": round(lat_c, 5), "Longitude": round(lon_c, 5),
            "ClienteDesde": cliente_desde.isoformat(),
        })

        n_talhoes = random.randint(1, 3)
        for _ in range(n_talhoes):
            cultura = random.choice(info["culturas"])
            area = round(random.uniform(*AREA_RANGE[cultura]), 1)
            # talhão perto da sede do agricultor (jitter pequeno)
            t_lat = lat_c + random.uniform(-0.35, 0.35)
            t_lon = lon_c + random.uniform(-0.35, 0.35)
            safra_ano = random.choice([2023, 2024, 2025])
            talhoes.append({
                "TalhaoID": talhao_id, "AgricultorID": agricultor_id,
                "NomeTalhao": f"Talhão {talhao_id:03d}", "Cultura": cultura,
                "AreaHectares": area, "Latitude": round(t_lat, 5), "Longitude": round(t_lon, 5),
                "Safra": f"{safra_ano}/{safra_ano+1}",
            })
            talhao_id += 1
        agricultor_id += 1

# --- Consumo de fertilizantes mensal (2022-01 a 2025-12), sazonal por cultura ---
consumo = []
for t in talhoes:
    cultura = t["Cultura"]
    area = t["AreaHectares"]
    taxa_anual = TAXA_HA_TON[cultura] * area
    picos = set(PICO_MES[cultura])
    tipos = FERT_POR_CULTURA[cultura]

    for ano in range(2022, 2026):
        for mes in range(1, 13):
            if date(ano, mes, 1) > date(2025, 12, 1):
                continue
            is_pico = mes in picos
            # fora de pico, aplica menos frequentemente
            if not is_pico and random.random() < 0.55:
                continue
            fator_mes = random.uniform(0.55, 0.85) if is_pico else random.uniform(0.08, 0.22)
            tendencia = 1 + (ano - 2022) * 0.025  # leve crescimento ano a ano
            ruido = random.uniform(0.9, 1.12)
            toneladas = round(taxa_anual * fator_mes * tendencia * ruido / 3, 3)
            if toneladas <= 0:
                continue
            tipo = random.choice(tipos)
            custo = round(toneladas * CUSTO_TON_BRL[tipo] * random.uniform(0.96, 1.05), 2)
            consumo.append({
                "Data": date(ano, mes, 1).isoformat(), "TalhaoID": t["TalhaoID"],
                "TipoFertilizante": tipo, "Toneladas": toneladas, "CustoBRL": custo,
            })

with open(f"{OUT_DIR}\\agricultores.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(agricultores[0].keys()))
    w.writeheader()
    w.writerows(agricultores)

with open(f"{OUT_DIR}\\talhoes.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(talhoes[0].keys()))
    w.writeheader()
    w.writerows(talhoes)

with open(f"{OUT_DIR}\\fertilizantes_consumo.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(consumo[0].keys()))
    w.writeheader()
    w.writerows(consumo)

print(f"Agricultores: {len(agricultores)}")
print(f"Talhoes: {len(talhoes)}")
print(f"Consumo: {len(consumo)}")
print(f"Total hectares: {sum(t['AreaHectares'] for t in talhoes):,.0f}")
