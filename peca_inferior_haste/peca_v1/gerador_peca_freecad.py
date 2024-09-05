import FreeCAD as App
import Part

# Criar um novo documento
doc = App.newDocument("Montagem")

# Dimensões do cubo
cubo_lado = 47.3
furo_diametro = 4.5
furo_profundidade = 20.0
distancia_inferior = 20.0

# Dimensões do bloco inferior
largura = 55  # mm
comprimento = 55  # mm
altura = 17  # mm
furo_lado = 13  # mm
furo_altura = 8  # mm
furo_raio = furo_diametro / 2

# Criar o cubo com os furos
cubo = Part.makeBox(cubo_lado, cubo_lado, cubo_lado)

# Definir a posição inicial dos furos nas superfícies do cubo
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

# Posicionar o cubo em cima do bloco inferior
cubo_posicionado = cubo_com_furos.copy()
cubo_posicionado.translate(App.Vector((largura - cubo_lado) / 2, (comprimento - cubo_lado) / 2, altura))

# Combinar o cubo e o bloco inferior em uma única peça
peca_final = cubo_posicionado.fuse(bloco_inferior)

# Adicionar a peça final ao documento
Part.show(peca_final)

# Recalcular o documento para atualizar a visualização
doc.recompute()

# Salvar o documento
doc.saveAs('Montagem_Cubo_Bloco.FCStd')
