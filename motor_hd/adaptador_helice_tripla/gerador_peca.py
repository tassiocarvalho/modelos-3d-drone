import FreeCAD as App
import Part
import math

def criar_triangulo_equilatero(lado, altura):
    """
    Cria um triângulo equilátero com lado especificado e altura (extrusão)
    """
    # Calcular altura do triângulo equilátero
    altura_triangulo = (lado * math.sqrt(3)) / 2
    
    # Criar os vértices do triângulo equilátero centrado na origem
    vertices = [
        App.Vector(0, altura_triangulo * 2/3, 0),  # Vértice superior
        App.Vector(-lado/2, -altura_triangulo * 1/3, 0),  # Vértice inferior esquerdo
        App.Vector(lado/2, -altura_triangulo * 1/3, 0),   # Vértice inferior direito
        App.Vector(0, altura_triangulo * 2/3, 0)   # Fechar o triângulo
    ]
    
    # Criar as arestas
    edges = []
    for i in range(len(vertices) - 1):
        edges.append(Part.makeLine(vertices[i], vertices[i + 1]))
    
    # Criar o wire (contorno fechado)
    wire = Part.Wire(edges)
    
    # Criar a face
    face = Part.Face(wire)
    
    # Extrudar para criar o sólido
    triangulo = face.extrude(App.Vector(0, 0, altura))
    
    return triangulo

def criar_anel_inferior():
    """
    Cria o anel inferior: Ø33.9 x Ø25.1 x 2.5mm com 3 furos
    Posição: Z = -0.5 a 2mm (expandido 0.5mm para baixo)
    """
    diametro_externo = 33.9
    diametro_interno = 25.1
    altura = 2.5  # Aumentado de 2.0 para 2.5mm
    
    raio_externo = diametro_externo / 2
    raio_interno = diametro_interno / 2
    
    cilindro_externo = Part.makeCylinder(raio_externo, altura)
    cilindro_interno = Part.makeCylinder(raio_interno, altura)
    anel = cilindro_externo.cut(cilindro_interno)
    
    diametro_furo_pequeno = 2.05
    raio_furo_pequeno = diametro_furo_pequeno / 2
    raio_posicao_furos = (raio_externo + raio_interno) / 2
    
    for i in range(3):
        angulo = i * 120 * math.pi / 180
        x = raio_posicao_furos * math.cos(angulo)
        y = raio_posicao_furos * math.sin(angulo)
        
        furo = Part.makeCylinder(raio_furo_pequeno, altura)
        furo.translate(App.Vector(x, y, 0))
        anel = anel.cut(furo)
    
    # Deslocar para baixo 0.5mm para manter o topo em Z=2mm
    anel.translate(App.Vector(0, 0, -0.5))
    
    return anel

def criar_anel_medio():
    """
    Cria o anel médio: Ø25.2 x Ø14.6 x 3mm com 4 furos
    Posição: Z = 0.6 a 3.6mm (deslocado mais 0.5mm para baixo)
    """
    diametro_externo = 25.2
    diametro_interno = 15
    altura = 3.0
    
    raio_externo = diametro_externo / 2
    raio_interno = diametro_interno / 2
    
    cilindro_externo = Part.makeCylinder(raio_externo, altura)
    cilindro_interno = Part.makeCylinder(raio_interno, altura)
    anel = cilindro_externo.cut(cilindro_interno)
    
    diametro_furo = 2.05
    raio_furo = diametro_furo / 2
    separacao_linear = 14.0
    
    raio_circunferencia_furos = separacao_linear / (2 * math.sin(math.pi / 4))
    
    for i in range(4):
        angulo = i * 90 * math.pi / 180
        x = raio_circunferencia_furos * math.cos(angulo)
        y = raio_circunferencia_furos * math.sin(angulo)
        
        furo = Part.makeCylinder(raio_furo, altura)
        furo.translate(App.Vector(x, y, 0))
        anel = anel.cut(furo)
    
    anel.translate(App.Vector(0, 0, 0.6))  # Deslocado mais 0.5mm para baixo (de 1.1 para 0.6)
    
    return anel

def criar_anel_central():
    """
    Cria o anel central: Ø33.9 x Ø25.1 x 3mm com 3 furos grandes de Ø10mm
    e 3 furos triangulares de 30mm de lado x 3mm de altura (SUBTRAÍDOS do anel)
    Posição: Z = 2 a 5mm (na mesma posição do anel médio original)
    """
    diametro_externo = 33.9
    diametro_interno = 25.1
    altura = 3.0
    
    raio_externo = diametro_externo / 2
    raio_interno = diametro_interno / 2
    
    # Criar o anel básico
    cilindro_externo = Part.makeCylinder(raio_externo, altura)
    cilindro_interno = Part.makeCylinder(raio_interno, altura)
    anel = cilindro_externo.cut(cilindro_interno)
    
    # Parâmetros dos furos e triângulos
    diametro_furo_grande = 10.0
    raio_furo_grande = diametro_furo_grande / 2
    raio_posicao_furos = (raio_externo + raio_interno) / 2
    
    lado_triangulo = 30
    altura_triangulo = 3.0
    
    for i in range(3):
        angulo = i * 120 * math.pi / 180
        x = raio_posicao_furos * math.cos(angulo)
        y = raio_posicao_furos * math.sin(angulo)
        
        # Criar e posicionar o furo circular
        furo = Part.makeCylinder(raio_furo_grande, altura)
        furo.translate(App.Vector(x, y, 0))
        anel = anel.cut(furo)
        
        # Criar e posicionar o triângulo no centro do furo
        triangulo = criar_triangulo_equilatero(lado_triangulo, altura_triangulo)
        
        # Rotacionar o triângulo para que uma ponta aponte para o centro do anel
        # O triângulo é criado com uma ponta apontando para cima (Y+)
        # Precisamos rotacionar para que aponte para o centro (origem)
        angulo_rotacao = angulo + math.pi/2  # +90° para alinhar ponta com o centro
        triangulo.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), math.degrees(angulo_rotacao))
        
        # Posicionar o triângulo no centro do furo
        triangulo.translate(App.Vector(x, y, 0))
        
        # SUBTRAIR o triângulo do anel (criar furo triangular)
        anel = anel.cut(triangulo)
    
    anel.translate(App.Vector(0, 0, 2.0))  # Mantém posição original
    
    return anel

def criar_anel_superior_extra():
    """
    Cria o anel superior extra: Ø25.2 x Ø14.6 x 4.4mm com 4 furos de Ø5mm
    Centro tampado (disco sólido)
    Posição: Z = 3.6 a 8mm (deslocado mais 0.5mm para baixo + 0.5mm altura adicional)
    """
    diametro_externo = 25.2
    diametro_interno = 14.6
    altura = 4.4  # Aumentado de 3.9 para 4.4mm (+0.5mm)
    
    raio_externo = diametro_externo / 2
    
    # Criar disco sólido (sem furo central)
    cilindro_externo = Part.makeCylinder(raio_externo, altura)
    
    diametro_furo = 5
    raio_furo = diametro_furo / 2
    separacao_linear = 14.0
    
    raio_circunferencia_furos = separacao_linear / (2 * math.sin(math.pi / 4))
    
    # Criar apenas os 4 furos externos
    for i in range(4):
        angulo = i * 90 * math.pi / 180
        x = raio_circunferencia_furos * math.cos(angulo)
        y = raio_circunferencia_furos * math.sin(angulo)
        
        furo = Part.makeCylinder(raio_furo, altura)
        furo.translate(App.Vector(x, y, 0))
        cilindro_externo = cilindro_externo.cut(furo)
    
    cilindro_externo.translate(App.Vector(0, 0, 3.6))  # Deslocado de 4.1 para 3.6mm (-0.5mm)
    
    return cilindro_externo

def criar_anel_superior():
    """
    Cria o anel superior: Ø33.9 x Ø25.1 x 3mm com 3 furos de 2.05mm
    + 3 rebaixos de Ø10mm com 1.1mm de altura partindo de baixo
    Posição: Z = 5 a 8mm
    """
    diametro_externo = 33.9
    diametro_interno = 25.1
    altura = 3.0
    
    raio_externo = diametro_externo / 2
    raio_interno = diametro_interno / 2
    
    cilindro_externo = Part.makeCylinder(raio_externo, altura)
    cilindro_interno = Part.makeCylinder(raio_interno, altura)
    anel = cilindro_externo.cut(cilindro_interno)
    
    # Furos pequenos de Ø2.05mm (atravessam toda a altura)
    diametro_furo_pequeno = 2.05
    raio_furo_pequeno = diametro_furo_pequeno / 2
    raio_posicao_furos = (raio_externo + raio_interno) / 2
    
    for i in range(3):
        angulo = i * 120 * math.pi / 180
        x = raio_posicao_furos * math.cos(angulo)
        y = raio_posicao_furos * math.sin(angulo)
        
        furo = Part.makeCylinder(raio_furo_pequeno, altura)
        furo.translate(App.Vector(x, y, 0))
        anel = anel.cut(furo)
    
    # Rebaixos grandes de Ø10mm com altura 1.1mm (partindo de baixo)
    diametro_furo_grande = 19.3
    raio_furo_grande = diametro_furo_grande / 2
    altura_rebaixo = 0.1
    
    for i in range(3):
        angulo = i * 120 * math.pi / 180
        x = raio_posicao_furos * math.cos(angulo)
        y = raio_posicao_furos * math.sin(angulo)
        
        # Rebaixo de 1.1mm partindo de baixo (Z=0 relativo ao anel)
        rebaixo = Part.makeCylinder(raio_furo_grande, altura_rebaixo)
        rebaixo.translate(App.Vector(x, y, 0))
        anel = anel.cut(rebaixo)
    
    anel.translate(App.Vector(0, 0, 5.0))
    
    return anel

def criar_conjunto_aneis():
    """
    Cria o conjunto completo dos cinco anéis empilhados como uma peça única
    """
    doc = App.newDocument("Conjunto_Aneis_com_Furos_Triangulares")
    
    # Criar cada anel
    anel_inferior = criar_anel_inferior()
    anel_medio = criar_anel_medio()  # Agora deslocado 0.9mm para baixo
    anel_central = criar_anel_central()  # Com furos triangulares
    anel_superior = criar_anel_superior()
    anel_superior_extra = criar_anel_superior_extra()
    
    # Combinar todos os anéis em uma única peça
    conjunto_unido = anel_inferior.fuse(anel_medio).fuse(anel_central).fuse(anel_superior).fuse(anel_superior_extra)
    
    # Criar apenas o objeto conjunto
    obj_conjunto = doc.addObject("Part::Feature", "Conjunto_Completo")
    obj_conjunto.Shape = conjunto_unido
    obj_conjunto.Label = "Conjunto_Completo_com_Furos_Triangulares"
    
    doc.recompute()
    
    try:
        import FreeCADGui as Gui
        Gui.activeDocument().activeView().fitAll()
    except:
        pass
    
    return obj_conjunto

def exportar_stl(obj_conjunto, nome_arquivo="conjunto_aneis_furos_triangulares.stl"):
    """
    Exporta o conjunto para arquivo STL
    """
    try:
        obj_conjunto.Shape.exportStl(nome_arquivo)
        print(f"Conjunto exportado para: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao exportar STL: {e}")

if __name__ == "__main__":
    conjunto = criar_conjunto_aneis()
    print("Conjunto de aneis criado como peça única com furos triangulares!")
    print("Modificações realizadas:")
    print("- Anel central agora inclui 3 furos triangulares equiláteros de 30mm")
    print("- Furos triangulares posicionados no centro dos furos circulares de Ø10mm")
    print("- Triângulos orientados com uma ponta apontando para o centro")
    print("- Triângulos SUBTRAÍDOS do anel (criando vazios triangulares)")
    print("- Anel médio (4 furos de 2mm) deslocado total de 1.4mm para baixo")
    print("- Nova posição do anel médio: Z = 0.6 a 3.6mm")
    print("- Anel superior extra (4 furos de 5mm) deslocado total de 1.4mm para baixo e altura aumentada em 1.4mm")
    print("- Nova posição do anel superior extra: Z = 3.6 a 8.0mm (altura 4.4mm)")
    print("- Anel inferior expandido 0.5mm para baixo: altura 2.5mm")
    print("- Nova posição do anel inferior: Z = -0.5 a 2.0mm")
    
    # Exportar para STL
    exportar_stl(conjunto)