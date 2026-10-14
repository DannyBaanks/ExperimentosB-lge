# -*- coding: latin-1 -*-
"""
generar_4d.py -- Genera el source del ciclo 4D y lo prueba en Malbolge.

Estrategia:
  1. Usar el MISMO main loop de Lutter (está verificado)
  2. Poner los datos del ciclo 4D en la región que el main loop lee
  3. Verificar que produce el output correcto
  
La modificacion clave: el main loop de Lutter lee desde d=29516+ (región B).
Para ciclo 4D, hacemos que lea desde d=0+ (región A = datos del ciclo 4D).

Esto se logra cambiando el bootstrap para que d empiece en 0 y mantenga
el stride interno en 188.
"""
import sys, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(r"/home/danny/Development/ISyCo/workspace/assembly/malbolge")))
import malbolge_interpreter as mi

QUINE = Path(r"/home/danny/Development/ISyCo/workspace/assembly/malbolge/quine_lutter.malbolge")
full_src = QUINE.read_text(encoding='utf-8')
src = ''.join(c for c in full_src if not c.isspace())

N = len(src) // 2  # 29,516

# ===========================================================================
# Construir el source del ciclo 4D
# ===========================================================================
# Layout:
#   [0..N-1]: Datos del ciclo 4D (w=0..156, cada w=188 bytes)
#   [N..2N-1]: MISMO source de Lutter (bootstrap + main loop)
#
# El main loop de Lutter está en c=4354..2N-1 (donde 2N=59032).
# Para que el main loop lea desde d=0..N-1 (datos del ciclo 4D),
# necesitamos modificar el bootstrap para que d apunte a 0..N-1.
#
# En Lutter, el bootstrap calcula d=29516+ para leer desde B.
# Para ciclo 4D, el bootstrap debe calcular d=0+ para leer desde A.
# ===========================================================================

print("=" * 70)
print("GENERADOR DE QUINE CICLO 4D")
print("=" * 70)
print()

# ---------------------------------------------------------------------------
# Estrategia: USAR EL MISMO BOOTSTRAP DE LUTTER
# El bootstrap de Lutter hace que el main loop lea desde d=29516+.
# Si en lugar de eso, hacemos que lea desde d=0+, el main loop lee
# los datos del ciclo 4D.
#
# El problema: el main loop de Lutter ejecuta c=0..59031 dos veces.
# En la primera pasada, c=0..N-1 se ejecutan como código.
# Eso modifica los datos del ciclo 4D.
#
# Solución: poner un JMP en c=0 que salte a c=N (main loop).
# Así c=0..N-1 NO se ejecutan en la primera pasada.
# El main loop empieza en c=N y recorre c=N..2N-1.
# En la segunda pasada, overflow c=2N → c=0.
# c=0: JMP → c=N (otra vez).
# Los datos del ciclo 4D (c=0..N-1) NUNCA se ejecutan.
# ---------------------------------------------------------------------------

# El source del ciclo 4D:
#   [0]: JMP → N (salta datos)
#   [1..N-1]: Datos del ciclo 4D (no se ejecutan nunca)
#   [N..2N-1]: Bootstrap + main loop de Lutter

# En Lutter, el JMP inicial está en c=0 y salta a c=32.
# Para el ciclo 4D, el JMP inicial debe saltar a c=N (29,516).
# Pero N es muy grande para un solo JMP. Necesitamos un JMP encadenado.

# En Malbolge, JMP: c = mem[d]
# Si mem[d] = N, entonces c = N.
# Necesitamos mem[d] = 29516. Eso se calcula en el bootstrap.

# Usar el MISMO bootstrap de Lutter pero modificado para que d apunte a N.
# El bootstrap de Lutter calcula d=29516 (para leer desde B).
# Para ciclo 4D, calculamos d=29516 (para saltar a B = main loop).
# ¡ES LA MISMA CUENTA! El bootstrap de Lutter calcula c=29516.

# Entonces: el MISMO bootstrap de Lutter FUNCIONA para el ciclo 4D
# porque calcula el MISMO salto (c=29516).

# La única diferencia: en Lutter, B = datos (copia de A).
# En ciclo 4D, B = main loop (código), A = datos (ciclo 4D).

# El main loop de Lutter recorre c=0..59031.
# Si A = datos (c=0..N-1) y B = main loop (c=N..2N-1),
# el main loop recorre c=0..2N-1.
# Pero c=0..N-1 (datos) se ejecutan como código en la primera pasada.
# Si ponemos JMP en c=0 que salta a c=N, entonces c=0..N-1 NO se ejecutan.

# El JMP en c=0 debe saltar a c=N=29516.
# Eso se logra con el bootstrap calculando mem[d]=29516.

# ¡ES EXACTAMENTE LO QUE HACE LUTTER! El bootstrap calcula el JMP a c=29516.

# Entonces el source del ciclo 4D es:
#   c=0: 'b' (JMP, calculado por el bootstrap para saltar a 29516)
#   c=1..N-1: datos del ciclo 4D (w=0..156)
#   c=N..2N-1: MISMO source de Lutter (bootstrap + main loop)

# El MISMO source de Lutter en c=N..2N-1 porque el main loop de Lutter
# está diseñado para ejecutarse desde c=N (no desde c=0).

# Construir el source del ciclo 4D
# Parte 1: Datos del ciclo 4D en c=0..N-1
datos_4d = src[:N]  # El bloque A de Lutter ES el ciclo 4D

# Parte 2: Bootstrap + main loop de Lutter en c=N..2N-1
codigo_lutter = src[:N]  # El MISMO código de Lutter

# Source completo
ciclo_4d_source = datos_4d + codigo_lutter

print(f"Datos ciclo 4D:  {len(datos_4d):,} bytes (c=0..{N-1})")
print(f"Codigo Lutter:   {len(codigo_lutter):,} bytes (c={N}..{2*N-1})")
print(f"Total source:    {len(ciclo_4d_source):,} bytes")
print()

# Verificar que cell[0] es JMP
print(f"Cell[0]: '{ciclo_4d_source[0]}' (val={ord(ciclo_4d_source[0])})")
print(f"Cell[0] opcode: {(ord(ciclo_4d_source[0]) - 33) % 94}")
print()

# Verificar que cell[N] empieza con el bootstrap de Lutter
print(f"Cell[{N}] (inicio codigo): '{ciclo_4d_source[N]}'")
print(f"Cell[{N}..{N+20}]:")
print(f"  {repr(ciclo_4d_source[N:N+20])}")
print()

# Guardar el source del ciclo 4D
output_file = ROOT / "quine_4d.malbolge"
output_file.write_text(ciclo_4d_source, encoding='latin-1')
print(f"Source guardado en: {output_file}")
print(f"Tamano: {len(ciclo_4d_source):,} bytes")
print()

# ===========================================================================
# PASO 2: Probar el ciclo 4D en Malbolge
# ===========================================================================
print("=" * 70)
print("PROBANDO CICLO 4D EN MALBOLGE")
print("=" * 70)
print()

# El main loop de Lutter recorre c=0..59031 dos veces.
# En el ciclo 4D, c=0..59031 = datos (A) + código (B).
# El main loop recorre TODO, incluyendo los datos de A.

# Si el JMP en c=0 salta a c=29516, entonces c=0..29515 NO se ejecutan.
# El main loop empieza en c=29516 y recorre hasta c=59031.
# Luego overflow c=59032 → c=0.
# c=0: JMP → c=29516 (otra vez).

# El output es el main loop (B) procesado dos veces.
# El main loop de Lutter produce 59,852 bytes (con newlines).
# Si el main loop está en B (c=29516..59031), el output es el main loop procesado.

# Pero en Lutter, el output es el source completo (A+B).
# Si el main loop está en B, el output es solo B (main loop),
# no A (datos del ciclo 4D).

# Para que el output incluye los datos del ciclo 4D (A),
# el main loop debe ACCEDER a A (c=0..N-1) mediante DLOAD.

# En Lutter, el main loop accede a B (c=29516..59031) mediante DLOAD.
# Para ciclo 4D, el main loop debe acceder a A (c=0..N-1) mediante DLOAD.

# El main loop de Lutter accede a mem[d] donde d está en el rango 29516+.
# Si hacemos que d apunte a 0+ (en lugar de 29516+), el main loop accede a A.

# Esto se logra modificando el bootstrap para que:
#   1. mem[d] = 0 (en lugar de 29516)
#   2. d = 0

# Pero el main loop de Lutter modifica d durante su ejecución.
# El primer DLOAD en el main loop hace d = mem[d].
# Si mem[d] = 0, entonces d = 0 después del primer DLOAD.
# El segundo DLOAD hace d = mem[0] = ... (sigue siendo 0 o cambia).

# Para mantener d en el rango 0..N-1, necesitamos que mem[d] contenga
# valores incrementales: mem[0] = 1, mem[1] = 2, ..., mem[N-1] = 0.

# Podemos modificar los datos de A (c=0..N-1) para que contengan
# estos valores incrementales en lugar del ciclo 4D original.

# Pero entonces los datos de A NO son el ciclo 4D. El ciclo 4D se pierde.

# ESTO ES UN PROBLEMA FUNDAMENTAL:
# El main loop de Lutter modifica d durante su ejecución.
# Para que el main loop recorra d=0..N-1, necesitamos mem[d] = d+1.
# Pero entonces los datos de A son mem[d] = d+1, no el ciclo 4D.

# El ciclo 4D necesita que los datos sean el ciclo 4D, no incrementales.
# Si los datos son incrementales, el ciclo 4D se rompe.

# SOLUCIÓN: Usar el main loop de Lutter para GENERAR los datos del ciclo 4D.
# El main loop escribe mem[d] = valor del ciclo 4D en lugar de mem[d] = d+1.

# Para eso, necesitamos que el main loop tenga acceso a los valores del ciclo 4D.
# Si los datos de A son el ciclo 4D, el main loop puede leerlos.
# Pero el main loop modifica d, así que no puede mantener d en el rango del ciclo 4D.

# NECESITAMOS un main loop que NO modifique d, o que modifique d
# de forma predecible para recorrer el ciclo 4D.

# Esto requiere reescribir el main loop desde cero.

print("El main loop de Lutter modifica d durante su ejecucion.")
print("Para el ciclo 4D, necesitamos un main loop que mantenga d")
print("en el rango 0..N-1 para leer los datos del ciclo 4D.")
print()
print("Esto requiere REDISENAR EL MAIN LOOP desde cero.")
print("No es trivial, pero es posible.")
print()
print("PROXIMO PASO: Escribir un solver que calcule el main loop")
print("para el ciclo 4D con stride_w=188.")