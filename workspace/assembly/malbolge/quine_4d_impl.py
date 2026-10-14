# -*- coding: utf-8 -*-
"""
quine_4d_impl.py -- Implementa el ciclo 4D en Malbolge.

Estructura del source:
  [0]: JMP -> salta sobre el bootstrap
  [1..B-1]: Bootstrap (prepara estado para ciclo 4D)
  [B..B+29515]: TOROIDE 4D (29,516 bytes, capas w=0..156)
  [B+29516]: END

El bootstrap:
  1. Establece d = stride_w = 188 (para saltos entre capas w)
  2. Establece contador de w = 0
  3. Loop:
     a. Output 188 bytes (c=0..187)
     b. c += 188 (c = c + stride_w, salta a siguiente w)
     c. w++
     d. Si w < 157: repetir paso a
     e. Si w = 157: reset w=0, repetir paso a (segunda pasada)
  4. Después de 2 pasadas: END
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(r"/home/danny/Development/ISyCo/workspace/assembly/malbolge")))
import malbolge_interpreter as mi

QUINE = Path(r"/home/danny/Development/ISyCo/workspace/assembly/malbolge/quine_lutter.malbolge")
full_src = QUINE.read_text(encoding='utf-8')
src = ''.join(c for c in full_src if not c.isspace())

N = len(src) // 2  # 29,516 bytes (un solo bloque)
nx, ny, nz, nw = 2, 2, 47, 157
stride_w = nx * ny * nz  # 188
layer_size = nx * ny * nz  # 188
BOOTSTRAP_SIZE = 500  # Bootstrap de ~500 bytes

print("=" * 70)
print("IMPLEMENTACION DE QUINE CICLO 4D")
print("=" * 70)
print()

# ===========================================================================
# Estrategia de bootstrap
# ===========================================================================
# El bootstrap debe:
# 1. Poner 'd' en una posición donde mem[d] = 188 (stride)
# 2. Hacer un loop que recorra w=0→156 dos veces
#
# En Malbolge, el loop se implementa con JMPs condicionales.
# El patrón de Lutter usa JMPs hacia celdas específicas que
# modifican c para saltar a la siguiente w.
#
# Para el ciclo 4D, necesitamos:
# - JMP de w=k a w=k+1: c = c + 188
# - JMP de w=156 a w=0: c = c - 156*188 = c - 29328
#
# Esto se calcula en el bootstrap almacenando los valores en memoria.
# ===========================================================================

def Char(op, c=0):
    """Devuelve el carácter que produce 'op' con contador 'c'."""
    for val in range(33, 127):
        if (val + c) % 94 == op:
            return chr(val)
    return None

# ===========================================================================
# Diseñar el bootstrap para ciclo 4D
# ===========================================================================
# Necesitamos que el bootstrap haga:
# 1. Establecer d para stride=188
# 2. Loop: recorrer 188 bytes, luego c+=188, repetir 157 veces
# 3. Después de 157 iteraciones: reset c=0, repetir
#
# El problema: Malbolge no tiene "if w==157: goto X".
# Necesitamos que el propio código se modifique para hacer el reset.
#
# Solución: El JMP final de w=156 salta a una celda que modifica c a 0.
# Eso es lo que hace Lutter: el bootstrap calcula los JMPs para hacer
# c=0 después de recorrer todas las w.
# ===========================================================================

class Bootstrap4D:
    def __init__(self, stride, num_w, block_size):
        self.stride = stride  # 188
        self.num_w = num_w    # 157
        self.block_size = block_size  # 29,516
    
    def design(self):
        """
        Diseña el código del bootstrap.
        
        Layout del bootstrap:
          [BOOT0]: JMP a BOOT_START (salta setup)
          [BOOT1..BOOT_START-1]: Setup DLOAD/ROT para inicializar d
          [BOOT_START]: INICIO DEL LOOP 4D
          
        El loop 4D (para cada w):
          1. OUT celdas 0..187 (output de la capa w)
          2. CRAZY/DLOAD/ROT para modificar c += 188
          3. JMP al siguiente w
          
        Después de w=156:
          4. Modificar c a 0 (reset a w=0)
          5. Volver al paso 1 (segunda pasada)
          
        Después de 2 pasadas:
          6. END
        """
        
        # El objetivo: escribir el código que hace MALBOLGE EJECUTAR
        # el ciclo 4D. Esto es la parte difícil.
        
        # Por ahora, reportamos qué hace falta
        print("Diseño del bootstrap para ciclo 4D:")
        print()
        print(f"  Stride w: {self.stride}")
        print(f"  Número de capas w: {self.num_w}")
        print(f"  Tamaño de bloque: {self.block_size:,}")
        print()
        print("Instrucciones necesarias:")
        print(f"  1. DLOAD inicial para establecer d")
        print(f"  2. CRAZY para calcular c_target = c + {self.stride}")
        print(f"  3. ROT para ajustar d para próxima iteración")
        print(f"  4. JMP para saltar a la siguiente capa w")
        print(f"  5. Reset c=0 después de w=156")
        print()
        
        return None

bootstrap = Bootstrap4D(stride_w, nw, N)
bootstrap.design()

# ===========================================================================
# Verificación: El ciclo 4D ya funciona con los datos de Lutter
# ===========================================================================
print("=" * 70)
print("VERIFICACION: CICLO 4D vs LUTTER ORIGINAL")
print("=" * 70)
print()

# El output de Lutter es el source completo CON newlines
# Si el ciclo 4D produce el MISMO output, tenemos una quine de 29,516 bytes

# Simular el ciclo 4D con 2 pasadas
class Toroide4D:
    def __init__(self, data, nx, ny, nz, nw):
        self.data = data
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.nw = nw
        self.size = nx * ny * nz * nw
        self.stride_w = nx * ny * nz
    
    def idx4d(self, x, y, z, w):
        return ((w * self.nz + z) * self.ny + y) * self.nx + x
    
    def get_layer(self, w):
        layer = []
        for z in range(self.nz):
            for y in range(self.ny):
                for x in range(self.nx):
                    idx = self.idx4d(x, y, z, w)
                    if idx < len(self.data):
                        layer.append(self.data[idx])
        return layer

toro = Toroide4D(src[:N], nx, ny, nz, nw)

# Generar output de 2 pasadas del ciclo 4D
output_2passes = []
for pass_num in range(2):
    for w in range(nw):
        layer = toro.get_layer(w)
        output_2passes.extend(layer)

output_2passes_str = ''.join(output_2passes)

# Comparar con source original (con newlines)
original_with_nl = full_src
print(f"Comparando output ciclo 4D vs Lutter original:")
print(f"  Output 4D: {len(output_2passes_str):,} bytes")
print(f"  Lutter:    {len(original_with_nl):,} bytes")
print()

match_count = sum(1 for i in range(min(len(output_2passes_str), len(original_with_nl)))
                  if output_2passes_str[i] == original_with_nl[i])
print(f"  Coinciden: {match_count}/{min(len(output_2passes_str), len(original_with_nl))}")
print(f"  Match exacto: {output_2passes_str == original_with_nl}")
print()

# Mostrar primeros 50 chars de cada uno
print(f"  Output 4D (primeros 50): {repr(output_2passes_str[:50])}")
print(f"  Lutter (primeros 50):   {repr(original_with_nl[:50])}")
print()

# Comparar última parte
print(f"  Output 4D (últimos 50): {repr(output_2passes_str[-50:])}")
print(f"  Lutter (últimos 50):   {repr(original_with_nl[-50:])}")
print()

# ===========================================================================
# RESULTADO
# ===========================================================================
if output_2passes_str == original_with_nl:
    print("=" * 70)
    print("¡ÉXITO! El ciclo 4D reproduce EXACTAMENTE el output de Lutter.")
    print("=" * 70)
    print()
    print(f"Quine de ciclo 4D: {N:,} bytes (50% reducción)")
    print(f"Stride w: {stride_w}")
    print()
    print("Próximo paso: Escribir el bootstrap Malbolge que hace el ciclo 4D.")
else:
    print("=" * 70)
    print("El Ciclo 4D no reproduce exactamente el output de Lutter.")
    print("Necesitamos ajustar el recorrido o los datos.")
    print("=" * 70)
    print()
    
    # Encontrar la primera diferencia
    for i in range(min(len(output_2passes_str), len(original_with_nl))):
        if output_2passes_str[i] != original_with_nl[i]:
            print(f"Primera diferencia en posición {i}:")
            print(f"  4D: {repr(output_2passes_str[i])}")
            print(f"  Lutter: {repr(original_with_nl[i])}")
            print()
            print(f"  Contexto 4D (pos {max(0,i-10)}:{i+10}):")
            print(f"    {repr(output_2passes_str[max(0,i-10):i+10])}")
            print(f"  Contexto Lutter (pos {max(0,i-10)}:{i+10}):")
            print(f"    {repr(original_with_nl[max(0,i-10):i+10])}")
            break

print()
print("=" * 70)
print("PROXIMOS PASOS")
print("=" * 70)
print("""
1. Si el ciclo 4D funciona: escribir bootstrap Malbolge
2. Verificar que el bootstrap produce el output correcto
3. Si funciona: tenemos una quine de 29,516 bytes (50% reducción)
4. Si no: ajustar el stride_w o el número de capas w
""")