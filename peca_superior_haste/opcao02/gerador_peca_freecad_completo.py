import FreeCAD as App
import Part

# Criar um novo documento
doc = App.newDocument("Prisma_Concreto_Com_Cubo")

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

# Fundir o cubo com o bloco fino
cubo_com_bloco = cubo_com_furos.fuse(bloco_fino)

# Dimensões do prisma
topo_lado = 41.0
altura = 20.0

# Dimensões das vigas
viga_grossura = 3.0
viga_altura = 5.0

# Dimensões das pontes
ponte_grossura = 3.0
brecha_superior = 3.0

# Dimensões das semi pontes
semi_ponte_comprimento = 5
semi_ponte_largura = 3.6

# Dimensões dos buracos
buraco_diametro = 3.0
buraco_raio = buraco_diametro / 2
buraco_altura = 20.0  # A altura do furo deve ser suficiente para atravessar a ponte

# Criar as bases do prisma
base = Part.makePolygon([
    App.Vector(0, 0, 0),
    App.Vector(cubo_lado, 0, 0),
    App.Vector(cubo_lado, cubo_lado, 0),
    App.Vector(0, cubo_lado, 0),
    App.Vector(0, 0, 0)
])

topo = Part.makePolygon([
    App.Vector((cubo_lado - topo_lado) / 2, (cubo_lado - topo_lado) / 2, altura),
    App.Vector((cubo_lado + topo_lado) / 2, (cubo_lado - topo_lado) / 2, altura),
    App.Vector((cubo_lado + topo_lado) / 2, (cubo_lado + topo_lado) / 2, altura),
    App.Vector((cubo_lado - topo_lado) / 2, (cubo_lado + topo_lado) / 2, altura),
    App.Vector((cubo_lado - topo_lado) / 2, (cubo_lado - topo_lado) / 2, altura)
])

# Criar um loft entre as bases
loft = Part.makeLoft([base, topo], True)

# Criar vigas nos vértices do topo
vigas = []
vigas_posicoes = [
    ((cubo_lado - topo_lado) / 2, (cubo_lado - topo_lado) / 2, altura),
    ((cubo_lado + topo_lado) / 2 - viga_grossura, (cubo_lado - topo_lado) / 2, altura),
    ((cubo_lado + topo_lado) / 2 - viga_grossura, (cubo_lado + topo_lado) / 2 - viga_grossura, altura),
    ((cubo_lado - topo_lado) / 2, (cubo_lado + topo_lado) / 2 - viga_grossura, altura)
]

for pos in vigas_posicoes:
    viga = Part.makeBox(viga_grossura, viga_grossura, viga_altura)
    viga.translate(App.Vector(pos[0], pos[1], pos[2]))
    vigas.append(viga)

# Criar pontes entre as vigas
pontes = []

# Pontes horizontais
pontes_posicoes_horizontais = [
    ((cubo_lado - topo_lado) / 2 + viga_grossura, (cubo_lado - topo_lado) / 2, altura + viga_altura - brecha_superior),
    ((cubo_lado - topo_lado) / 2 + viga_grossura, (cubo_lado + topo_lado) / 2 - viga_grossura, altura + viga_altura - brecha_superior)
]

for pos in pontes_posicoes_horizontais:
    ponte = Part.makeBox(topo_lado - 2 * viga_grossura, ponte_grossura, viga_grossura)
    ponte.translate(App.Vector(pos[0], pos[1], pos[2]))
    pontes.append(ponte)

# Pontes verticais
pontes_posicoes_verticais = [
    ((cubo_lado - topo_lado) / 2, (cubo_lado - topo_lado) / 2 + viga_grossura, altura + viga_altura - brecha_superior),
    ((cubo_lado + topo_lado) / 2 - viga_grossura, (cubo_lado - topo_lado) / 2 + viga_grossura, altura + viga_altura - brecha_superior)
]

for pos in pontes_posicoes_verticais:
    ponte = Part.makeBox(ponte_grossura, topo_lado - 2 * viga_grossura, viga_grossura)
    ponte.translate(App.Vector(pos[0], pos[1], pos[2]))
    pontes.append(ponte)

# Criar semi pontes no meio das pontes
semi_pontes = []
buracos = []

# Semi pontes horizontais (deslocadas para sobrepor um pouco as pontes)
semi_pontes_posicoes_horizontais = [
    ((cubo_lado - topo_lado) / 2 + (topo_lado / 2) - (semi_ponte_largura / 2), (cubo_lado - topo_lado) / 2 + ponte_grossura - 1.5, altura + viga_altura - brecha_superior),
    ((cubo_lado - topo_lado) / 2 + (topo_lado / 2) - (semi_ponte_largura / 2), (cubo_lado + topo_lado) / 2 - ponte_grossura - semi_ponte_comprimento + 1.5, altura + viga_altura - brecha_superior)
]

for pos in semi_pontes_posicoes_horizontais:
    semi_ponte = Part.makeBox(semi_ponte_largura, semi_ponte_comprimento, ponte_grossura)
    semi_ponte.translate(App.Vector(pos[0], pos[1], pos[2]))
    semi_pontes.append(semi_ponte)
    buraco = Part.makeCylinder(buraco_raio, buraco_altura)
    buraco.translate(App.Vector(pos[0] + semi_ponte_largura / 2, pos[1] + semi_ponte_comprimento / 2, altura))
    buracos.append(buraco)

# Semi pontes verticais (deslocadas para sobrepor um pouco as pontes)
semi_pontes_posicoes_verticais = [
    ((cubo_lado - topo_lado) / 2 + ponte_grossura - 1.5, (cubo_lado - topo_lado) / 2 + (topo_lado / 2) - (semi_ponte_largura / 2), altura + viga_altura - brecha_superior),
    ((cubo_lado + topo_lado) / 2 - ponte_grossura - semi_ponte_comprimento + 1.5, (cubo_lado - topo_lado) / 2 + (topo_lado / 2) - (semi_ponte_largura / 2), altura + viga_altura - brecha_superior)
]

for pos in semi_pontes_posicoes_verticais:
    semi_ponte = Part.makeBox(semi_ponte_comprimento, semi_ponte_largura, ponte_grossura)
    semi_ponte.translate(App.Vector(pos[0], pos[1], pos[2]))
    semi_pontes.append(semi_ponte)
    buraco = Part.makeCylinder(buraco_raio, buraco_altura)
    buraco.translate(App.Vector(pos[0] + semi_ponte_comprimento / 2, pos[1] + semi_ponte_largura / 2, altura))
    buracos.append(buraco)

# Subtrair os buracos das semi pontes e pontes
for buraco in buracos:
    for i in range(len(semi_pontes)):
        semi_pontes[i] = semi_pontes[i].cut(buraco)
    for i in range(len(pontes)):
        pontes[i] = pontes[i].cut(buraco)

# Combinar o loft, as vigas, as pontes e as semi pontes em um único objeto
prisma_completo = loft.fuse(vigas + pontes + semi_pontes)

# Posicionar o prisma completo no topo do bloco fino
prisma_completo.translate(App.Vector((cubo_lado - cubo_lado) / 2, (cubo_lado - cubo_lado) / 2, cubo_lado + bloco_altura))

# Fundir tudo em um único objeto
objeto_final = cubo_com_bloco.fuse(prisma_completo)

# Adicionar o objeto final ao documento
objeto_final_obj = doc.addObject("Part::Feature", "ObjetoFinal")
objeto_final_obj.Shape = objeto_final

# Recalcular o documento para atualizar a visualização
doc.recompute()

# Salvar o documento
doc.saveAs('Cubo_com_Prisma_Concreto.FCStd')

print("Cubo com prisma concreto criado com sucesso!")
