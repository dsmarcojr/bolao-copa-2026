import re

def ehEmailValido(email):
    # Regex rigorosa: exige @, domínio e extensão (ex: .com, .com.br)
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(padrao, email))

def _calcular_digito_cpf(cpf_parcial, peso_inicial):
    soma = sum(int(cpf_parcial[i]) * (peso_inicial - i) for i in range(len(cpf_parcial)))
    return (soma * 10 % 11) % 10

def ehCPFValido(cpf):
    cpf = re.sub(r'\D', '', str(cpf))
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    digito_1 = _calcular_digito_cpf(cpf[:9], 10)
    digito_2 = _calcular_digito_cpf(cpf[:10], 11)
    
    return int(cpf[9]) == digito_1 and int(cpf[10]) == digito_2

def ehSenhaForte(senha):
    if len(senha) < 8: return False
    tem_maiuscula = any(c.isupper() for c in senha)
    tem_minuscula = any(c.islower() for c in senha)
    tem_numero = any(c.isdigit() for c in senha)
    tem_simbolo = any(not c.isalnum() for c in senha)
    return tem_maiuscula and tem_minuscula and tem_numero and tem_simbolo

def calcular_pontos(gols_real, gols_palpite):
    """
    Calcula pontos do bolão:
    - 25 pts: Placar Exato
    - 10 pts: Acertou vencedor/empate mas errou placar
    - 0 pts: Errou tudo
    """
    if gols_real == gols_palpite:
        return 25
    
    # Verifica tendência (Vitória Casa, Empate, Vitória Fora)
    tendencia_real = (gols_real[0] > gols_real[1]) - (gols_real[0] < gols_real[1])
    tendencia_palpite = (gols_palpite[0] > gols_palpite[1]) - (gols_palpite[0] < gols_palpite[1])
    
    if tendencia_real == tendencia_palpite:
        return 10
        
    return 0
