import FreeCAD as App
import Part
import math
from FreeCAD import Base

# Criar um novo documento no FreeCAD
doc = App.newDocument("CilindroComParalelepipedoEVariosFurosEAdicional")

# --- PRIMEIRA PEÇA: Cilindro com Paralelepípedo e Múltiplos Furos ---

# Dimensões do cilindro principal
diametro_cilindro = 17  # mm
altura_cilindro = 10 - 1.5  # mm (altura ajustada para manter altura total em 10 mm)
raio_cilindro = diametro_cilindro / 2

# Criar o cilindro principal
cilindro_principal = Part.makeCylinder(raio_cilindro, altura_cilindro)

# Dimensões do paralelepípedo
largura_paralelepipedo = 19  # mm
comprimento_paralelepipedo = 19  # mm
altura_paralelepipedo = 1.5  # mm

# Criar o paralelepípedo
paralelepipedo = Part.makeBox(
    largura_paralelepipedo, comprimento_paralelepipedo, altura_paralelepipedo
)

# Posicionar o paralelepípedo abaixo do cilindro
paralelepipedo.translate(App.Vector(-largura_paralelepipedo / 2, -comprimento_paralelepipedo / 2, -altura_paralelepipedo))

# Unir o cilindro e o paralelepípedo
peca_combinada = cilindro_principal.fuse(paralelepipedo)

# Dimensões do vazio principal
diametro_vazio = 15  # mm
altura_vazio = altura_cilindro - 4  # mm
raio_vazio = diametro_vazio / 2

# Criar o vazio principal
vazio_principal = Part.makeCylinder(raio_vazio, altura_vazio)

# Posicionar o vazio principal
vazio_principal.translate(App.Vector(0, 0, -altura_paralelepipedo))

# Subtrair o vazio principal da peça combinada
peca_combinada = peca_combinada.cut(vazio_principal)

# Dimensões dos furos pequenos
diametro_furo = 1.9  # mm
altura_furo = altura_paralelepipedo  # mm
raio_furo = diametro_furo / 2
distancia_furos = 14  # mm

# Posições dos quatro furos
posicoes_furos = [
    (-distancia_furos / 2, -distancia_furos / 2),  # Furo 1 (canto inferior esquerdo)
    (distancia_furos / 2, -distancia_furos / 2),   # Furo 2 (canto inferior direito)
    (-distancia_furos / 2, distancia_furos / 2),   # Furo 3 (canto superior esquerdo)
    (distancia_furos / 2, distancia_furos / 2)     # Furo 4 (canto superior direito)
]

# Criar e subtrair os furos
for pos in posicoes_furos:
    furo = Part.makeCylinder(raio_furo, altura_furo)
    # Posicionar cada furo no paralelepípedo
    furo.translate(App.Vector(pos[0], pos[1], -altura_paralelepipedo))
    # Subtrair o furo da peça
    peca_combinada = peca_combinada.cut(furo)

# --- SEGUNDA PEÇA: Cilindro com Furos Retangulares ---

# Dimensões do cilindro adicional
diametro = 19.5  # mm
altura = 14  # mm
cilindro_adicional = Part.makeCylinder(diametro / 2, altura)

# Adicionar furos retangulares maiores
lado_longo = 5.9  # mm
lado_curto = 4  # mm
profundidade_retangulo = 5  # mm
raio = diametro / 2
offset_radial = 2.3  # mm

for i in range(3):
    angulo = math.radians(i * 120)
    x = (raio - offset_radial) * math.cos(angulo)
    y = (raio - offset_radial) * math.sin(angulo)
    retangulo = Part.makeBox(lado_longo, lado_curto, profundidade_retangulo)
    retangulo.translate(Base.Vector(-lado_longo / 2, -lado_curto / 2, 0))
    retangulo.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), math.degrees(angulo))
    retangulo.translate(Base.Vector(x, y, altura - profundidade_retangulo))
    cilindro_adicional = cilindro_adicional.cut(retangulo)

# Adicionar furos retangulares menores
lado_longo2 = 5.9  # mm
lado_curto2 = 4  # mm
profundidade_retangulo2 = 5  # mm
offset_radial2 = 1.55  # mm

for i in range(3):
    angulo = math.radians(i * 120)
    x = (raio - offset_radial2) * math.cos(angulo)
    y = (raio - offset_radial2) * math.sin(angulo)
    retangulo_menor = Part.makeBox(lado_longo2, lado_curto2, profundidade_retangulo2)
    retangulo_menor.translate(Base.Vector(-lado_longo2 / 2, -lado_curto2 / 2, 0))
    retangulo_menor.rotate(Base.Vector(0, 0, 0), Base.Vector(0, 0, 1), math.degrees(angulo))
    retangulo_menor.translate(Base.Vector(x, y, altura - profundidade_retangulo2))
    cilindro_adicional = cilindro_adicional.cut(retangulo_menor)

# Posicionar o cilindro adicional exatamente acima da peça combinada
cilindro_adicional.translate(App.Vector(0, 0, altura_cilindro + altura_paralelepipedo - altura_paralelepipedo))

# --- Combinar as duas peças ---
peca_final = peca_combinada.fuse(cilindro_adicional)

# Adicionar a peça final ao documento
objeto = doc.addObject("Part::Feature", "CilindroComParalelepipedoEVariosFurosEAdicional")
objeto.Shape = peca_final

# Atualizar a visualização
doc.recompute()

print("Peça com cilindro adicional colada criada com sucesso!")
