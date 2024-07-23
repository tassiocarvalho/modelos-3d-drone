import FreeCAD as App
import Part
import Sketcher

# Criar um novo documento
doc = App.newDocument()

# Definir as dimensões do cubo
cubo_lado = 47.4
furo_diametro = 4.5
furo_profundidade = 20.0
distancia_inferior = 20.0

# Criar o cubo
cubo = Part.makeBox(cubo_lado, cubo_lado, cubo_lado)

# Definir a posição inicial dos furos nas superfícies do cubo
furo_posicao_front = App.Vector(cubo_lado / 2, 0, distancia_inferior)
furo_posicao_right = App.Vector(cubo_lado, cubo_lado / 2, distancia_inferior)
furo_posicao_rear = App.Vector(cubo_lado / 2, cubo_lado, distancia_inferior)
furo_posicao_left = App.Vector(0, cubo_lado / 2, distancia_inferior)

# Criar os cilindros (furos) com a profundidade especificada
furo_front = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_front, App.Vector(0, 1, 0))
furo_right = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_right, App.Vector(-1, 0, 0))
furo_rear = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_rear, App.Vector(0, -1, 0))
furo_left = Part.makeCylinder(furo_diametro / 2, furo_profundidade, furo_posicao_left, App.Vector(1, 0, 0))

# Subtrair os furos do cubo
cubo_com_furos = cubo.cut(furo_front).cut(furo_right).cut(furo_rear).cut(furo_left)

# Adicionar o cubo com os furos ao documento
cubo_obj = doc.addObject("Part::Feature", "CuboComFuros")
cubo_obj.Shape = cubo_com_furos

# Definir as dimensões do bloco fino
bloco_largura = 50.0
bloco_profundidade = 50.0
bloco_altura = 0.6

# Criar o bloco fino
bloco_fino = Part.makeBox(bloco_largura, bloco_profundidade, bloco_altura)

# Posicionar o bloco fino no topo do cubo e centralizado
posicao_x = (cubo_lado - bloco_largura) / 2
posicao_y = (cubo_lado - bloco_profundidade) / 2
bloco_fino.translate(App.Vector(posicao_x, posicao_y, cubo_lado))

# Adicionar o bloco fino ao documento
bloco_obj = doc.addObject("Part::Feature", "BlocoFino")
bloco_obj.Shape = bloco_fino

# Atualizar o documento para visualizar o cubo com furos e bloco fino
doc.recompute()

# --- Adicionar a peça previamente criada em cima do bloco fino ---

# Criação do esboço da base quadrada
base = doc.addObject('Sketcher::SketchObject', 'Base')
base.Placement = App.Placement(App.Vector(posicao_x + bloco_largura / 2, posicao_y + bloco_profundidade / 2, cubo_lado + bloco_altura), App.Rotation(0, 0, 0, 1))
geoList = [
    Part.LineSegment(App.Vector(-23.7, -23.7, 0), App.Vector(23.7, -23.7, 0)),
    Part.LineSegment(App.Vector(23.7, -23.7, 0), App.Vector(23.7, 23.7, 0)),
    Part.LineSegment(App.Vector(23.7, 23.7, 0), App.Vector(-23.7, 23.7, 0)),
    Part.LineSegment(App.Vector(-23.7, 23.7, 0), App.Vector(-23.7, -23.7, 0))
]
for geo in geoList:
    base.addGeometry(geo)

# Criar o esboço do topo redondo
topo = doc.addObject('Sketcher::SketchObject', 'Topo')
topo.Placement = App.Placement(App.Vector(posicao_x + bloco_largura / 2, posicao_y + bloco_profundidade / 2, cubo_lado + bloco_altura + 20), App.Rotation(0, 0, 0, 1))
topo.addGeometry(Part.Circle(App.Vector(0, 0, 20), App.Vector(0, 0, 1), 20.5))

# Atualizar documento
doc.recompute()

# Criar o Loft entre os dois esboços
loft = doc.addObject('Part::Loft', 'Loft')
loft.Sections = [base, topo]
loft.Solid = True
loft.Ruled = False
loft.Closed = False

# Atualizar o documento para visualizar o Loft
doc.recompute()

# Criar as vigas no topo
viga_coords = [
    (0, 19),  # Norte
    (0, -19), # Sul
    (19, 0),  # Leste
]

vigas = []
for i, (x, y) in enumerate(viga_coords):
    viga = doc.addObject('Part::Box', f'Viga_{i+1}')
    viga.Length = 3  # Espessura
    viga.Width = 3   # Largura
    viga.Height = 5  # Altura
    viga.Placement = App.Placement(App.Vector(posicao_x + bloco_largura / 2 + x - 1.5, posicao_y + bloco_profundidade / 2 + y - 1.5, cubo_lado + bloco_altura + 20), App.Rotation(0, 0, 0, 1))
    vigas.append(viga)

# Atualizar o documento para visualizar as vigas
doc.recompute()

# Criar o anel com espessura ajustada para 4 mm
anel_externo = doc.addObject('Part::Cylinder', 'AnelExterno')
anel_externo.Radius = 20.5
anel_externo.Height = 3
anel_externo.Placement = App.Placement(App.Vector(posicao_x + bloco_largura / 2, posicao_y + bloco_profundidade / 2, cubo_lado + bloco_altura + 22), App.Rotation(0, 0, 0, 1))

anel_interno = doc.addObject('Part::Cylinder', 'AnelInterno')
anel_interno.Radius = 16.5  # Ajuste para espessura de 4 mm
anel_interno.Height = 3
anel_interno.Placement = App.Placement(App.Vector(posicao_x + bloco_largura / 2, posicao_y + bloco_profundidade / 2, cubo_lado + bloco_altura + 22), App.Rotation(0, 0, 0, 1))

# Fazer a diferença entre o cilindro externo e interno para formar o anel
anel = doc.addObject('Part::Cut', 'Anel')
anel.Base = anel_externo
anel.Tool = anel_interno

# Atualizar o documento para visualizar o anel
doc.recompute()

# Criar as semipontes
# Dimensões das semipontes
semiponte_altura = 3
semiponte_grossura = 5
semiponte_comprimento = 5
semiponte_deslocamento = 2

# Coordenadas das semipontes, movidas mais para dentro do anel
semiponte_coords = [
    (11.7, 11.7),   # Nordeste
    (-11.7, 11.7),  # Noroeste
    (11.7, -11.7),  # Sudeste
    (-11.7, -11.7)  # Sudoeste
]

semipontes = []
for i, (x, y) in enumerate(semiponte_coords):
    semiponte = doc.addObject('Part::Box', f'Semiponte_{i+1}')
    semiponte.Length = semiponte_comprimento
    semiponte.Width = semiponte_grossura
    semiponte.Height = semiponte_altura
    semiponte.Placement = App.Placement(App.Vector(posicao_x + bloco_largura / 2 + x - semiponte_comprimento / 2, posicao_y + bloco_profundidade / 2 + y - semiponte_grossura / 2, cubo_lado + bloco_altura + 22), App.Rotation(0, 0, 0, 1))
    semipontes.append(semiponte)

# Atualizar o documento para visualizar as semipontes
doc.recompute()

# Criar furos no centro de cada semiponte
diametro_furo = 3
raio_furo = diametro_furo / 2

# Função para criar e aplicar o furo em uma semiponte e no anel
def criar_furo(x, y, nome):
    furo = doc.addObject('Part::Cylinder', nome)
    furo.Radius = raio_furo
    furo.Height = 10  # Altura suficiente para atravessar a semiponte e o anel
    furo.Placement = App.Placement(App.Vector(posicao_x + bloco_largura / 2 + x, posicao_y + bloco_profundidade / 2 + y, cubo_lado + bloco_altura + 22), App.Rotation(0, 0, 0, 1))
    return furo

furos = []
# Criar furos e subtrair das semipontes e do anel
for i, (x, y) in enumerate(semiponte_coords):
    furo = criar_furo(x, y, f'Furo_{i+1}')
    furos.append(furo)
    # Subtrair o furo da semiponte
    semiponte_furada = doc.addObject('Part::Cut', f'SemiponteFurada_{i+1}')
    semiponte_furada.Base = semipontes[i]
    semiponte_furada.Tool = furo
    semipontes[i] = semiponte_furada

# Subtrair os furos do anel
anel_furado = anel
for i, furo in enumerate(furos):
    anel_furado_temp = doc.addObject('Part::Cut', f'AnelFurado_{i+1}')
    anel_furado_temp.Base = anel_furado
    anel_furado_temp.Tool = furo
    anel_furado = anel_furado_temp

# Atualizar o documento para visualizar os furos no anel e nas semipontes
doc.recompute()

# Combinar todas as partes em uma única peça
parts_to_combine = [loft] + vigas + [anel_furado] + semipontes + [cubo_obj, bloco_obj]
combined_part = doc.addObject('Part::MultiFuse', 'CombinedPart')
combined_part.Shapes = parts_to_combine

# Atualizar o documento para visualizar a peça combinada
doc.recompute()

# Salvar o documento
doc.saveAs('/mnt/data/peca_combinada.FCStd')

print("Peça combinada criada com sucesso!")
