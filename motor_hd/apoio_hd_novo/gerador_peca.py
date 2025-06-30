import FreeCAD as App
import Part
import Mesh
import math

# Criar o documento
doc = App.newDocument("CuboEestrutura")

# ** Definição do cubo **
# Parâmetros do cubo
cubo_lado = 47.4
furo_diametro = 4.5
furo_profundidade = 20.0
distancia_centro_topo = 20.0

# Criar o cubo
cubo = Part.makeBox(cubo_lado, cubo_lado, cubo_lado)

# Calcular a posição dos furos no cubo
distancia_superior = cubo_lado - distancia_centro_topo

# Definir a posição dos furos nas superfícies do cubo
furo_posicao_front = App.Vector(cubo_lado / 2, 0, distancia_superior)
furo_posicao_right = App.Vector(cubo_lado, cubo_lado / 2, distancia_superior)
furo_posicao_rear = App.Vector(cubo_lado / 2, cubo_lado, distancia_superior)
furo_posicao_left = App.Vector(0, cubo_lado / 2, distancia_superior)

# Criar os cilindros (furos)
furo_front = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_front, App.Vector(0, 1, 0))
furo_right = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_right, App.Vector(-1, 0, 0))
furo_rear = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_rear, App.Vector(0, -1, 0))
furo_left = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_left, App.Vector(1, 0, 0))

# Subtrair os furos do cubo
cubo_com_furos = cubo.cut(furo_front).cut(furo_right).cut(furo_rear).cut(furo_left)

# ** Definição da estrutura superior **
# Parâmetros da estrutura superior
base_lado = 47.4
topo_raio = 26
altura = 27
diametro_furo = 2.9
distancia_entre_furos = 40

# Parâmetros do vazio central
vazio_diametro = 38.1
vazio_profundidade = 10

# Parâmetros do paralelepípedo lateral
paralelepipedo_altura = 20 # Altura do paralelepípedo
paralelepipedo_lado = 37 # Lado do paralelepípedo
paralelepipedo_pos_z = 17  # Posição Z do paralelepípedo
paralelepipedo_espessura = 21 # Profundidade do paralelepípedo

# Calcular o raio do círculo onde os furos serão posicionados
raio_furo_posicao = distancia_entre_furos / (2 * math.sin(math.pi / 3))

# Criar a base da estrutura
base = Part.makePolygon([
    App.Vector(-base_lado / 2, -base_lado / 2, 0),
    App.Vector(base_lado / 2, -base_lado / 2, 0),
    App.Vector(base_lado / 2, base_lado / 2, 0),
    App.Vector(-base_lado / 2, base_lado / 2, 0),
    App.Vector(-base_lado / 2, -base_lado / 2, 0)
])
base_wire = Part.Wire(base)

# Criar o topo da estrutura
topo = Part.makeCircle(topo_raio, App.Vector(0, 0, altura))
topo_wire = Part.Wire(topo)

# Criar o loft
estrutura = Part.makeLoft([base_wire, topo_wire], True)

# Criar o vazio central
vazio_central = Part.makeCylinder(vazio_diametro / 2, vazio_profundidade, App.Vector(0, 0, altura - vazio_profundidade))

# Subtrair o vazio central
estrutura = estrutura.cut(vazio_central)

# Criar os furos no topo
furos = []
for i in range(3):
    angulo = math.radians(i * 120)
    x = raio_furo_posicao * math.cos(angulo)
    y = raio_furo_posicao * math.sin(angulo)
    furo = Part.makeCylinder(diametro_furo / 2, altura-10, App.Vector(x, y, altura), App.Vector(0, 0, -1))
    furos.append(furo)

# Subtrair os furos
for furo in furos:
    estrutura = estrutura.cut(furo)

# Criar o paralelepípedo lateral (ajustado para aproximar de um dos furos superiores)
paralelepipedo = Part.makeBox(
    paralelepipedo_lado,  # Lado do paralelepípedo
    paralelepipedo_espessura,  # Espessura do paralelepípedo
    paralelepipedo_altura,  # Altura do paralelepípedo
    App.Vector(2, paralelepipedo_espessura / 3, paralelepipedo_pos_z)  # Posicionado mais próximo de um furo superior
)

# Subtrair o paralelepípedo lateral
estrutura = estrutura.cut(paralelepipedo)

# Ajustar a posição da estrutura superior sobre o cubo
estrutura.translate(App.Vector(cubo_lado / 2, cubo_lado / 2, cubo_lado))

# ** Combinar as peças **
final_modelo = cubo_com_furos.fuse(estrutura)

# Adicionar a peça final ao documento
final_obj = doc.addObject("Part::Feature", "ModeloFinal")
final_obj.Shape = final_modelo

# Recalcular o documento
doc.recompute()

# Salvar o documento como STL
stl_file = "Cubo_E_Estrutura.stl"
Mesh.export([final_obj], stl_file)

print(f"Peça combinada exportada como {stl_file} com sucesso!")