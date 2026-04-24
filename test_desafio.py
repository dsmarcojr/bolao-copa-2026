import unittest
from desafio import ehEmailValido, ehCPFValido, ehSenhaForte, calcular_pontos

class TestDesafioTDD(unittest.TestCase):
    # Caso 1: Email válido
    def test_email_valido(self):
        self.assertTrue(ehEmailValido("contato@giuliamarco.com.br"))

    # Caso 2: Email inválido (formato incorreto ou sem extensão)
    def test_email_invalido(self):
        self.assertFalse(ehEmailValido("contatogiuliamarco.com.br"))
        self.assertFalse(ehEmailValido("user@dominio"))

    # Caso 3: CPF válido (Algoritmo oficial)
    def test_cpf_valido(self):
        self.assertTrue(ehCPFValido("12345678909"))

    # Caso 4: CPF inválido (Números repetidos)
    def test_cpf_repetido(self):
        self.assertFalse(ehCPFValido("00000000000"))

    # Caso 5: Senha forte (8+ chars, Maiúscula, Minúscula, Número e Símbolo)
    def test_senha_forte(self):
        self.assertTrue(ehSenhaForte("Brasil@2026"))

    def test_senha_sem_minuscula(self):
        self.assertFalse(ehSenhaForte("BRASIL@2026"))

class TestBolaoXP(unittest.TestCase):

    def test_placar_exato(self):
        self.assertEqual(calcular_pontos((2, 1), (2, 1)), 25)

    def test_vencedor_correto_placar_errado(self):
        self.assertEqual(calcular_pontos((2, 1), (3, 0)), 10)

    def test_empate_correto_placar_errado(self):
        self.assertEqual(calcular_pontos((1, 1), (0, 0)), 10)

    def test_erro_total(self):
        self.assertEqual(calcular_pontos((2, 1), (0, 2)), 0)

if __name__ == '__main__':
    unittest.main()
