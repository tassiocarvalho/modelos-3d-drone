import FreeCAD as App
import Part
import math
from FreeCAD import Base

# Criar um novo documento no FreeCAD
doc = App.newDocument("CilindroComBaseRedondaEChanfro")

# --- PRIMEIRA PEÇA: Cilindro com Base Redonda e Múltiplos Furos ---

# Dimensões do cilindro principal
diametro_cilindro = 19.5  # mm
altura_cilindro = 11.5  # mm
raio_cilindro = diametro_cilindro / 2

# Criar o cilindro principal
cilindro_principal = Part.makeCylinder(raio_cilindro, altura_cilindro)
cilindro_principal.translate(App.Vector(0, 0, 3))  # Mover para cima da base

# Dimensões da base redonda
diametro_base = 25  # mm (modificado de base quadrada para redonda)
altura_base = 3  # mm (mantida a mesma altura)
raio_base = diametro_base / 2

# Criar a base redonda (cilindro achatado)
base_redonda = Part.makeCylinder(raio_base, altura_base)

# Posicionar a base abaixo do cilindro principal
base_redonda.translate(App.Vector(0, 0, 0))

# Abordagem alternativa para criar chanfro usando a API de FreeCAD
# Primeiro, vamos criar a união das peças
peca_sem_chanfro = cilindro_principal.fuse(base_redonda)

# Criar um objeto sólido a partir da forma
solid_obj = doc.addObject("Part::Feature", "SolidoTemporario")
solid_obj.Shape = peca_sem_chanfro
doc.recompute()

# Identificar a aresta circular na junção (onde z = 3)
edge_index = None
for i, edge in enumerate(solid_obj.Shape.Edges):
    # Calcular o centro aproximado da aresta
    center = edge.CenterOfMass
    # Verificar se a aresta está na altura z = 3 (onde os cilindros se encontram)
    if abs(center.z - 3) < 0.01:
        # Verificar se a aresta tem o raio do cilindro principal
        try:
            curve = edge.Curve
            if hasattr(curve, "Radius") and abs(curve.Radius - raio_cilindro) < 0.01:
                edge_index = i
                break
        except:
            pass

# Aplicar o chanfro
if edge_index is not None:
    # Criar o chanfro
    chamfer = doc.addObject("Part::Chamfer", "Chanfro")
    chamfer.Base = solid_obj
    chamfer.Edges = [(edge_index+1, 1.0, 1.0)]  # Formato: (edge_index+1, size1, size2)
    doc.recompute()
    
    # Obter a forma chanfrada
    peca_combinada = chamfer.Shape.copy()
    
    # Remover os objetos temporários
    doc.removeObject(chamfer.Name)
    doc.removeObject(solid_obj.Name)
else:
    # Se não encontrar a aresta, continuar com a peça sem chanfro
    peca_combinada = peca_sem_chanfro
    print("ATENÇÃO: Não foi possível encontrar a aresta para aplicar o chanfro")

# Dimensões do vazio principal
diametro_vazio = 15  # mm
altura_vazio = altura_cilindro - 8.6  # mm
raio_vazio = diametro_vazio / 2

# Criar o vazio principal
vazio_principal = Part.makeCylinder(raio_vazio, altura_vazio)

# Posicionar o vazio principal
vazio_principal.translate(App.Vector(0, 0, 0))

# Subtrair o vazio principal da peça combinada
peca_combinada = peca_combinada.cut(vazio_principal)

# Dimensões dos furos pequenos
diametro_furo = 1.9  # mm
altura_furo = altura_base  # mm
raio_furo = diametro_furo / 2
distancia_furos = 14  # mm

# Posições dos quatro furos (mantidas as mesmas posições)
posicoes_furos = [
    (-distancia_furos / 2, -distancia_furos / 2),  # Furo 1 (canto inferior esquerdo)
    (distancia_furos / 2, -distancia_furos / 2),   # Furo 2 (canto inferior direito)
    (-distancia_furos / 2, distancia_furos / 2),   # Furo 3 (canto superior esquerdo)
    (distancia_furos / 2, distancia_furos / 2)     # Furo 4 (canto superior direito)
]

# Criar e subtrair os furos
for pos in posicoes_furos:
    furo = Part.makeCylinder(raio_furo, altura_furo)
    # Posicionar cada furo na base
    furo.translate(App.Vector(pos[0], pos[1], 0))
    # Subtrair o furo da peça
    peca_combinada = peca_combinada.cut(furo)

# Adicionar vazios cilíndricos de 5mm de diâmetro e 10mm de altura sobre cada furo
diametro_vazio_cilindrico = 5.0  # mm
altura_vazio_cilindrico = 10.0  # mm
raio_vazio_cilindrico = diametro_vazio_cilindrico / 2

# Criar e subtrair os vazios cilíndricos sobre os furos
for pos in posicoes_furos:
    vazio_cilindrico = Part.makeCylinder(raio_vazio_cilindrico, altura_vazio_cilindrico)
    # Posicionar cada vazio cilíndrico centralizado sobre o furo, na superfície da base
    vazio_cilindrico.translate(App.Vector(pos[0], pos[1], 3))  # z=3 é a superfície superior da base
    # Subtrair o vazio cilíndrico da peça
    peca_combinada = peca_combinada.cut(vazio_cilindrico)

# --- SEGUNDA PEÇA: Cilindro com Furos Retangulares ---

# Dimensões do cilindro adicional
diametro = 19.5  # mm
altura = 10  # mm
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
cilindro_adicional.translate(App.Vector(0, 0, altura_cilindro + 3))  # Ajustado para a altura correta (3 é a altura da base)

# --- Combinar as duas peças ---
peca_final = peca_combinada.fuse(cilindro_adicional)

# --- ADIÇÃO DO FURO CENTRAL (2 mm diâmetro, 13 mm profundidade) ---
# O topo da peça final (cilindro adicional) está em z = 3 + altura_cilindro + altura = 3 + 11.5 + 10 = 24.5 mm
# Queremos um furo descendo 13 mm a partir do topo.
# Raio do furo = 1 mm (para ter diâmetro de 2 mm)
furo_central = Part.makeCylinder(1.35, 13.0)
# Transladar para que o topo do furo fique em z = 24.5 e a base em z = 11.5
furo_central.translate(App.Vector(0, 0, 24.5 - 13.0))

# Subtrair o furo central da peça final
peca_final = peca_final.cut(furo_central)

# Adicionar a peça final ao documento
objeto = doc.addObject("Part::Feature", "CilindroComBaseRedondaEChanfro")
objeto.Shape = peca_final

# Atualizar a visualização
doc.recompute()

print("Peça com base redonda, chanfro de 1mm e vazios cilíndricos criada com sucesso!")