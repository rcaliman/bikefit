# -*- coding: utf-8 -*-
class Bikefit():
    def __init__(self,cavalo,esterno,braco):
        """Recebe as tres variaveis do formulario"""
        self.cavalo = cavalo
        self.esterno = esterno
        self.braco = braco

    def quadro_speed(self):
        """Calcula o tamanho do quadro para Speed"""
        return round((self.cavalo * 0.67),1)

    def quadro_mtb(self):
        """Calcula o tamanho do quadro para MTB"""    
        return round(((self.cavalo * 0.67 - 10) * 0.393700787),1)

    def altura_selim(self):
        """Calcula a altura do selim"""
        return round((self.cavalo * 0.883),1)

    def top_tube_efetivo(self):
        """Calcula o top tube efetivo"""
        return round((((self.esterno - self.cavalo + self.braco)/2)+4),1)
