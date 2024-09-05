import FreeCAD as App
import Part

# Criar um novo documento
doc = App.newDocument("Montagem_Final_Com_Furos")

# Dimensões do cubo
cubo_lado = 47.3
cubo_altura = 44.3  # Altura reduzida em 3 mm
furo_diametro = 4.5
furo_profundidade = 20.0
distancia_inferior = 17
raio_curva = 3.0
base_altura = 3  # Altura da base curvada

# Dimensões da base inferior (que cresce com a curva)
base_largura_inferior = cubo_lado + 2 * raio_curva  # A base cresce pelo raio da curva em ambos os lados
base_comprimento_inferior = cubo_lado + 2 * raio_curva

# Criar o cubo superior com os furos
cubo = Part.makeBox(cubo_lado, cubo_lado, cubo_altura)

# Definir a posição inicial dos furos nas superfícies do cubo
furo_raio = furo_diametro / 2
furo_posicao_front = App.Vector(cubo_lado / 2, 0, distancia_inferior)
furo_posicao_right = App.Vector(cubo_lado, cubo_lado / 2, distancia_inferior)
furo_posicao_rear = App.Vector(cubo_lado / 2, cubo_lado, distancia_inferior)
furo_posicao_left = App.Vector(0, cubo_lado / 2, distancia_inferior)

# Criar os cilindros (furos) com a profundidade especificada
furo_front = Part.makeCylinder(furo_raio, furo_profundidade, furo_posicao_front, App.Vector(0, 1, 0))
furo_right = Part.makeCylinder(furo_raio, furo_profundidade, furo_posicao_right, App.Vector(-1, 0, 0))
furo_rear = Part.makeCylinder(furo_raio, furo_profundidade, furo_posicao_rear, App.Vector(0, -1, 0))
furo_left = Part.makeCylinder(furo_raio, furo_profundidade, furo_posicao_left, App.Vector(1, 0, 0))

# Subtrair os furos do cubo
cubo_com_furos = cubo.cut(furo_front).cut(furo_right).cut(furo_rear).cut(furo_left)

# Criar a base curva com o tamanho expandido para a parte inferior
base = Part.makeBox(base_largura_inferior, base_comprimento_inferior, base_altura)

# Criar as curvas nas laterais da base
curva_lateral_frontal = Part.makeCylinder(raio_curva, base_comprimento_inferior, App.Vector(0, 0, base_altura), App.Vector(1, 0, 0))
curva_lateral_traseira = Part.makeCylinder(raio_curva, base_comprimento_inferior, App.Vector(0, base_largura_inferior, base_altura), App.Vector(1, 0, 0))
curva_lateral_esquerda = Part.makeCylinder(raio_curva, base_largura_inferior, App.Vector(0, 0, base_altura), App.Vector(0, 1, 0))
curva_lateral_direita = Part.makeCylinder(raio_curva, base_largura_inferior, App.Vector(base_comprimento_inferior, 0, base_altura), App.Vector(0, 1, 0))

# Subtrair as curvas das laterais para criar o perfil curvado
base = base.cut(curva_lateral_frontal)
base = base.cut(curva_lateral_traseira)
base = base.cut(curva_lateral_esquerda)
base = base.cut(curva_lateral_direita)

# Posicionar a base curvada corretamente no eixo Z
base.translate(App.Vector((cubo_lado - base_largura_inferior) / 2, (cubo_lado - base_comprimento_inferior) / 2, 0))

# Posicionar o cubo em cima da base curvada
cubo_posicionado = cubo_com_furos.copy()
cubo_posicionado.translate(App.Vector(0, 0, base_altura))

# Combinar o cubo e a base curvada
peca_superior = cubo_posicionado.fuse(base)

# Dimensões do bloco inferior (paralelepípedo)
largura = 55  # mm
comprimento = 55  # mm
altura = 18  # mm
furo_lado = 13  # mm
furo_altura = 16  # mm
furo_diametro = 4.5
furo_raio = furo_diametro / 2

# Criar o bloco inferior
bloco_inferior = Part.makeBox(largura, comprimento, altura)

# Criar o furo quadrado no bloco inferior
furo_posicao_x = (largura - furo_lado) / 2
furo_posicao_z = (altura - furo_lado) / 2
furo = Part.makeBox(furo_lado, comprimento, furo_lado)
furo.translate(App.Vector(furo_posicao_x, 0, furo_posicao_z))

# Subtrair o furo quadrado do bloco inferior
bloco_inferior = bloco_inferior.cut(furo)

# Criar os furos cilíndricos no bloco inferior
furo1_posicao_y = 5  # mm (medida do centro do furo até a borda)
furo1 = Part.makeCylinder(furo_raio, furo_altura)
furo1.translate(App.Vector(largura / 2, furo1_posicao_y, 0))

# Atualizar a posição do segundo furo para garantir 15 mm entre os centros
furo2_posicao_y = 5 + 15  # 5 mm do centro do primeiro furo + 15 mm de distância entre os furos
furo2 = Part.makeCylinder(furo_raio, furo_altura)
furo2.translate(App.Vector(largura / 2, furo2_posicao_y, 0))

# Subtrair os furos cilíndricos do bloco inferior
bloco_inferior = bloco_inferior.cut(furo1)
bloco_inferior = bloco_inferior.cut(furo2)

# Centralizar a peça superior (cubo com base curva) em relação ao bloco inferior
offset_x = (largura - cubo_lado) / 2
offset_y = (comprimento - cubo_lado) / 2
offset_z = altura  # Coloca o cubo em cima do bloco

peca_superior.translate(App.Vector(offset_x, offset_y, offset_z))

# Combinar a peça superior (cubo com base curva) e o bloco inferior com os furos
montagem_final = bloco_inferior.fuse(peca_superior)

# Adicionar a montagem final ao documento
Part.show(montagem_final)

# Recalcular o documento para atualizar a visualização
doc.recompute()

# Salvar o documento final
doc.saveAs('Montagem_Final_Com_Furos.FCStd')
