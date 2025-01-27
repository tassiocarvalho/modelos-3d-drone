import FreeCAD as App
import Part
import math

# Criar um novo documento
doc = App.newDocument("AnelComFuros")

# Definir dimensões
diametro_externo = 5  # Diâmetro externo em cm
diametro_interno = 3.7  # Diâmetro interno em cm
altura = 0.2  # Altura do anel em cm
diametro_furo = 0.4  # Diâmetro dos furos em cm
distancia_entre_furos = 3.77  # Distância entre os centros dos furos em cm

# Calcular o raio do círculo onde os furos serão posicionados
raio_posicao_furos = distancia_entre_furos / math.sqrt(3)  # Raio em cm

# Converter para raio
raio_externo = diametro_externo / 2
raio_interno = diametro_interno / 2
raio_furo = diametro_furo / 2

# Criar o cilindro externo (anel)
cilindro_externo = Part.makeCylinder(raio_externo * 10, altura * 10)

# Criar o cilindro interno (para o furo central do anel)
cilindro_interno = Part.makeCylinder(raio_interno * 10, altura * 10)

# Subtrair o cilindro interno do externo para formar o anel
anel = cilindro_externo.cut(cilindro_interno)

# Criar os três furos
furos = []
for i in range(3):  # 3 furos, cada um a 120 graus
    # Calcular a posição do furo
    angulo = math.radians(i * 120)  # Converter ângulo para radianos
    x = raio_posicao_furos * 10 * math.cos(angulo)  # Converter para mm
    y = raio_posicao_furos * 10 * math.sin(angulo)  # Converter para mm
    # Criar o cilindro do furo na posição calculada
    furo = Part.makeCylinder(raio_furo * 10, altura * 10, App.Vector(x, y, 0))
    furos.append(furo)

# Subtrair os furos do anel
for furo in furos:
    anel = anel.cut(furo)

# Adicionar a peça ao documento
Part.show(anel)

# Recalcular o documento para exibir o resultado
doc.recompute()

print("Anel com furos posicionados a 3,77 cm de distância criado com sucesso!")
