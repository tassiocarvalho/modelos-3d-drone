import Part
import math
from FreeCAD import Base

# Definir as dimensões do cilindro
diametro = 19.5  # em mm
altura = 24  # em mm

# Criar um novo documento no FreeCAD
doc = App.newDocument()

# Criar o cilindro
cilindro = Part.makeCylinder(diametro/2, altura)

# Definir as dimensões do primeiro furo circular (no topo)
diametro_furo = 2.5 # em mm
profundidade_furo = 13  # em mm

# Criar o furo partindo do topo do cilindro
furo_topo = Part.makeCylinder(diametro_furo/2, profundidade_furo)

# Posicionar o furo no topo do cilindro
furo_topo.translate(Base.Vector(0, 0, altura - profundidade_furo))

# Subtrair o furo do cilindro
cilindro_com_furo = cilindro.cut(furo_topo)

# Definir as dimensões do segundo furo circular (no fundo)
diametro_furo_fundo = 3.1  # em mm
profundidade_furo_fundo = 11  # em mm

# Criar o furo partindo do fundo do cilindro
furo_fundo = Part.makeCylinder(diametro_furo_fundo/2, profundidade_furo_fundo)

# Subtrair o furo do fundo do cilindro
cilindro_com_furo = cilindro_com_furo.cut(furo_fundo)

# Definir as dimensões do furo horizontal
diametro_furo_horizontal = 3.2  # em mm
comprimento_furo_horizontal = diametro  # atravessando todo o cilindro

# Criar o furo horizontal
furo_horizontal = Part.makeCylinder(diametro_furo_horizontal/2, comprimento_furo_horizontal)

# Posicionar o furo horizontal
furo_horizontal.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)  # Rotacionar o furo para a horizontal
furo_horizontal.translate(Base.Vector(-diametro/2, 0, 5))  # Posicionar o furo no centro lateral a 4mm de altura

# Subtrair o furo horizontal do cilindro
cilindro_com_furo = cilindro_com_furo.cut(furo_horizontal)

# Adicionar furos retangulares
lado_longo = 4.7  # mm
lado_curto = 4  # mm
profundidade_retangulo = 5  # mm
raio = diametro / 2  # raio do cilindro
offset_radial = 2.3  # mm

for i in range(3):
    angulo = math.radians(i * 120)
    x = (raio - offset_radial) * math.cos(angulo)
    y = (raio - offset_radial) * math.sin(angulo)
    
    # Criar o retângulo
    retangulo = Part.makeBox(lado_longo, lado_curto, profundidade_retangulo)
    
    # Centralizar o retângulo
    retangulo.translate(Base.Vector(-lado_longo/2, -lado_curto/2, 0))
    
    # Rotacionar o retângulo para alinhar radialmente
    retangulo.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), math.degrees(angulo))
    
    # Posicionar o retângulo na borda do círculo e no topo do cilindro
    retangulo.translate(Base.Vector(x, y, altura - profundidade_retangulo))
    
    # Subtrair o retângulo do cilindro
    cilindro_com_furo = cilindro_com_furo.cut(retangulo)

# Adicionar furos retangulares menores
lado_longo2 = 4.7  # mm
lado_curto2 = 4  # mm
profundidade_retangulo2 = 5  # mm
offset_radial2 = 1.55 

for i in range(3):
    angulo = math.radians(i * 120)
    x = (raio - offset_radial2) * math.cos(angulo)
    y = (raio - offset_radial2) * math.sin(angulo)
    
    # Criar o retângulo menor
    retangulo_menor = Part.makeBox(lado_longo2, lado_curto2, profundidade_retangulo2)
    
    # Centralizar o retângulo menor
    retangulo_menor.translate(Base.Vector(-lado_longo2/2, -lado_curto2/2, 0))
    
    # Rotacionar o retângulo menor para alinhar radialmente
    retangulo_menor.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), math.degrees(angulo))
    
    # Posicionar o retângulo menor na borda do círculo e no topo do cilindro
    retangulo_menor.translate(Base.Vector(x, y, altura - profundidade_retangulo2))
    
    # Subtrair o retângulo menor do cilindro
    cilindro_com_furo = cilindro_com_furo.cut(retangulo_menor)

# Adicionar o cilindro com todos os furos ao documento
Part.show(cilindro_com_furo)

# Recalcular o documento para aplicar as mudanças
doc.recompute()