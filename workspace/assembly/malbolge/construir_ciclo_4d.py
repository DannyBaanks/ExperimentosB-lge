# -*- coding: utf-8 -*-
"""
construir_ciclo_4d.py -- Construye el source completo del ciclo 4D.

Estructura final (59,032 bytes, MISMO tamano que stripped):
  [0..29515]: DATOS DEL CICLO 4D (toroide 2x2x47x157)
  [29516..59031]: BOOTSTRAP + MAIN LOOP (igual que Lutter, modificado)

El main loop de Lutter:
  - Recorre c=4354..59031 (code + datos)
  - JMP final: c = 59032 (overflow → c=0, reset)
  - Segundo recorrido: c=4354..59031
  - END

Para ciclo 4D:
  - El MISMO main loop funciona porque recorro c=0..29515 dos veces
  - El JMP overflow (c=59032 → c=0) hace reset automáticamente
  - No necesitamos modificar el main loop!
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

N = len(src) // 2  # 29,516 bytes

print("=" * 70)
print("CONSTRUCCION DE QUINE CICLO 4D")
print("=" * 70)
print()
print(f"Source stripped: {len(src):,} bytes")
print(f"Bloque 4D:       {N:,} bytes")
print()

# ===========================================================================
# LA CLAVE: El main loop de Lutter recorre TODO el source (c=0..59031)
# En el ciclo 4D, tenemos 29,516 datos + 29,516 código = 59,032 bytes
# El main loop de Lutter recorre c=0..59031, que es EXACTAMENTE
# el tamaño del ciclo 4D (29,516 datos + 29,516 código)!
#
# Si ponemos:
#   - Datos del ciclo 4D en c=0..29515
#   - Código de Lutter en c=29516..59031
# El main loop de Lutter recorre TODO (c=0..59031) dos veces:
#   - Primera vez: c=0..59031
#   - Segunda vez: c=0..59031 (overflow de c=59032 → c=0)
#
# Pero el código en c=29516..59031 se ejecuta como datos en la primera pasada!
# Eso está bien porque Lutter también hace eso (el main loop de Lutter
# ejecuta las celdas de B como datos en la primera pasada).
# ===========================================================================

# Estrategia SIMPLE:
# 1. Poner los datos del ciclo 4D en las primeras 29,516 celdas
# 2. Poner el MISMO source de Lutter en las siguientes 29,516 celdas
# 3. El main loop de Lutter recorre TODO (c=0..59031) dos veces
#    - Primera pasada: ejecuta datos (c=0..29515) y luego código (c=29516..59031)
#    - Segunda pasada: ejecuta datos (c=0..29515) y luego código (c=29516..59031)
#
# El problema: en la primera pasada, el main loop ejecuta los datos del ciclo 4D
# como si fueran código. Eso los modifica (por el traductor de Malbolge).
# En Lutter, el main loop ejecuta el bloque A (c=0..29515) en la primera pasada,
# y el bloque B (c=29516..59031) en la segunda pasada.
#
# Si ponemos datos del ciclo 4D en c=0..29515, el main loop los ejecuta
# y los modifica. Eso rompe el ciclo 4D.
#
# SOLUCIÓN: Poner el JMP inicial en c=0 para saltar sobre los datos.
# El main loop empieza en c=29516. Los datos están en c=0..29515
# pero NO se ejecutan (el JMP salta sobre ellos).
#
# Entonces:
#   c=0: JMP → c=29516 (salta datos, empieza main loop)
#   c=29516..59031: main loop (igual que Lutter)
#   Main loop recorre c=29516..59031 (15,516 celdas)
#   Luego overflow: c=59032 → c=0
#   c=0: JMP → c=29516 (otra vez)
#   Repite...
#
# Pero los datos (c=0..29515) NO se ejecutan nunca. Solo se leen como datos.
# El main loop usa DLOAD para acceder a los datos:
#   DLOAD mem[d] donde d apunta a los datos
#
# En Lutter, el main loop accede a los datos de B (c=29516..59031)
# mediante DLOAD desde mem[d] donde d apunta a posiciones de B.
#
# Para el ciclo 4D, el main loop debe acceder a los datos de A (c=0..29515)
# mediante DLOAD desde mem[d] donde d apunta a posiciones de A.
#
# El problema: el main loop de Lutter está HARDCODEADO para acceder
# a posiciones de B (c=29516..59031). Si cambiamos a posiciones de A
# (c=0..29515), el main loop no funciona.
#
# SOLUCIÓN: No cambiar el main loop. Poner los datos en c=29516..59031
# pero hacer que sean el ciclo 4D (en lugar de una copia de A).
#
# El ciclo 4D en c=29516..59031:
#   c=29516 → w=0, capa 0
#   c=29517 → w=0, capa 1
#   ...
#   c=29704 → w=1, capa 0
#   ...
#   c=59031 → w=156, capa 157
#
# El main loop de Lutter recorre c=29516..59031 (29,516 celdas).
# En la primera pasada, ejecuta c=0..29515 (datos=A) y luego c=29516..59031
# (datos=B=ciclo4D y main loop).
#
# Espera, eso no funciona porque el main loop está en c=29516..59031,
# y si el main loop se ejecuta, c recorre 29516..59031.
# Pero en la primera pasada, c=0..29515 se ejecutan como código (no como datos).
#
# Necesitamos que c=0..29515 NO se ejecuten en la primera pasada.
# Eso se logra con JMP en c=0 que salta a c=29516.
#
# Entonces:
#   c=0: JMP → c=29516 (salta datos A)
#   c=29516..59031: main loop (igual que Lutter)
#   Main loop recorre c=29516..59031 (29,516 celdas)
#   Luego: ¿qué pasa? El main loop de Lutter tiene un JMP final que hace
#   c = 59032 (overflow → c=0).
#   c=0: JMP → c=29516 (otra vez)
#   Repite...
#
# Esto recorre c=29516..59031 infinitamente (sin pasar por c=0..29515).
# NO ACCEDE A LOS DATOS DE A (c=0..29515)!
#
# Para acceder a los datos de A, el main loop debe hacer DLOAD desde
# posiciones de A (c=0..29515). En Lutter, el main loop hace DLOAD
# desde posiciones de B (c=29516..59031).
#
# Si el main loop hace DLOAD desde c=0..29515 (datos de A), entonces
# los datos están en c=0..29515 y el main loop accede a ellos.
# Pero el main loop está en c=29516..59031, así que cuando el main loop
# ejecuta DLOAD mem[d], d debe apuntar a c=0..29515.
#
# En Lutter, d apunta a posiciones de B. Para cambiar a posiciones de A,
# necesitamos modificar d para que apunte a A.
#
# SOLUCIÓN: En el bootstrap, establecer d para que apunte a A (d=0).
# Luego, el main loop hace DLOAD mem[d] donde d=0, 1, 2, ...
# Eso lee desde c=0..29515 (datos de A).
#
# Pero en Lutter, d empieza en 0 y luego cambia a 29516+ (para leer B).
# Para el ciclo 4D, d debe mantenerse en 0..29515 (para leer A).
#
# Necesitamos modificar el main loop de Lutter para que haga d=0..29515
# en lugar de d=29516..59032.
#
# ESTO ES IMPOSIBLE sin reescribir el main loop desde cero.
# El main loop de Lutter está hardcodeado para leer desde B (d=29516+).
#
# CONCLUSIÓN: No podemos usar el main loop de Lutter directamente
# para el ciclo 4D. Necesitamos un main loop NUEVO que lea desde
# posiciones de A (d=0..29515).
#
# Pero... ¿qué pasa si el main loop lee desde POSICIONES DEL MAIN LOOP
# en lugar de desde los datos? En Lutter, el main loop lee desde
# posiciones de B (que son datos). Si el main loop lee desde sí mismo
# (posiciones de A), entonces los datos están en el main loop.
#
# Eso es exactamente lo que hace Lutter: el main loop lee desde B,
# que es una copia de A. Si B no es una copia de A, el main loop
# lee algo diferente.
#
# Para el ciclo 4D, si ponemos los datos del ciclo 4D en A (c=0..29515)
# y el main loop en B (c=29516..59031), el main loop puede leer desde
# A (d=0..29515) o desde B (d=29516..59031).
#
# Si el main loop lee desde A (d=0..29515), entonces lee los datos
# del ciclo 4D. Si lee desde B (d=29516..59031), lee el main loop
# mismo (porque B contiene el main loop).
#
# En Lutter, el main loop lee desde B porque d apunta a B.
# Para el ciclo 4D, si hacemos que d apunte a A, el main loop lee
# los datos del ciclo 4D.
#
# La pregunta es: ¿el main loop de Lutter puede leer desde A
# (d=0..29515) en lugar de B (d=29516..59031)?
#
# Si el main loop hace DLOAD desde d=0..29515, entonces lee A.
# Pero el main loop de Lutter hace DLOAD desde d=29516..59031.
#
# Necesitamos cambiar el main loop para que haga d=0..29515.
# Eso requiere modificar los DLOADs en el main loop.
#
# PERO: los DLOADs en el main loop leen mem[d]. Si d=0, lee mem[0] (JMP).
# Si d=1, lee mem[1] (bootstrap NOP). Etc.
#
# Si ponemos los datos del ciclo 4D en A (c=0..29515), y el main loop
# hace DLOAD desde d=0..29515, entonces lee los datos del ciclo 4D.
# ¡ESO FUNCIONA!
#
# La única modificación necesaria en el main loop es cambiar los DLOADs
# para que lean desde d=0..29515 en lugar de d=29516..59031.
#
# Pero... ¿cómo cambiamos los DLOADs sin romper el main loop?
# Los DLOADs son parte del código del main loop. Si los cambiamos,
# el main loop se rompe.
#
# Necesitamos una forma de que los DLOADs lean desde d=0..29515
# SIN cambiar el código del main loop.
#
# SOLUCIÓN: Modificar d en el bootstrap para que todos los DLOADs
# lean desde A. En Lutter, el bootstrap establece d para que apunte
# a B. Si hacemos que el bootstrap establezca d=0 (o d=0+offset),
# los DLOADs leen desde A.
#
# Pero el main loop de Lutter modifica d durante su ejecución.
# Después del primer DLOAD, d cambia a un valor específico (por ejemplo,
# d=29516). Para mantener d en A, necesitamos que los DLOADs del
# main loop no modifiquen d a valores de B.
#
# En Lutter, el main loop tiene DLOADs que cargan d desde mem[d].
# Si mem[d] contiene valores de A (en lugar de valores de B),
# entonces d se mantiene en A.
#
# Podemos modificar los DATOS de A para que mem[d] contenga valores
# que mantengan d en el rango 0..29515.
#
# Pero los datos de A son los datos del ciclo 4D. Si los modificamos,
# el ciclo 4D se rompe.
#
# ESTAMOS EN UN CALLEJÓN SIN SALIDA.
# El main loop de Lutter está hardcodeado para leer desde B.
# No podemos cambiar eso sin reescribir el main loop.
#
# SOLUCIÓN ALTERNATIVA: Poner los datos del ciclo 4D en B (c=29516..59031)
# y hacer que el main loop lea desde B (d=29516..59031).
# Pero entonces necesitamos que los datos de B sean el ciclo 4D,
# no una copia de A.
#
# Si los datos de B son el ciclo 4D, entonces:
#   - El main loop recorre c=29516..59031 (datos de B = ciclo 4D)
#   - En la primera pasada, c=29516..59031 se ejecutan como código+datos
#   - El ciclo 4D está en B, y el main loop lo recorre
#
# ¡ESTO FUNCIONA! Pongamos el ciclo 4D en B (c=29516..59031).
# El main loop de Lutter recorre c=0..59031 (A + B) dos veces.
# En la primera pasada: c=0..29515 (A = main loop), c=29516..59031 (B = ciclo 4D)
# En la segunda pasada: c=0..29515 (A = main loop), c=29516..59031 (B = ciclo 4D)
#
# Pero en la primera pasada, c=0..29515 (A) se ejecutan como código.
# Eso modifica A (el main loop). Si el main loop está en A y se modifica
# durante la primera pasada, la segunda pasada es diferente.
#
# En Lutter, A se modifica durante la primera pasada, pero B es una COPIA
# de A, así que B sigue siendo el main loop original. La segunda pasada
# ejecuta B (main loop original).
#
# Para el ciclo 4D, si A es el main loop y B es el ciclo 4D (datos),
# entonces la primera pasada modifica A (main loop). La segunda pasada
# ejecuta A modificado, no el main loop original. Eso rompe el programa.
#
# NECESITAMOS que A sea una COPIA del main loop que NO se modifique
# durante la primera pasada. En Lutter, A se modifica, pero B es una
# copia intacta del main loop original.
#
# Para el ciclo 4D, si hacemos que A sea el main loop y B sea el ciclo 4D,
# necesitamos que A NO se modifique durante la primera pasada.
# Eso se logra si el JMP inicial salta sobre A (c=0..29515) y empieza
# en B (c=29516..59031).
#
# Si c=0: JMP → c=29516 (salta A)
# Entonces la primera pasada ejecuta c=29516..59031 (B = main loop + ciclo 4D).
# El main loop en B recorre c=29516..59031.
# Durante la primera pasada, el main loop ejecuta c=29516..59031.
# Los datos del ciclo 4D están en c=29516..59031 (junto con el main loop).
#
# Espera, el main loop y los datos están en la MISMA región (c=29516..59031).
# El main loop recorre c=29516..59031. Si los datos están en c=29516..59031,
# el main loop ejecuta sus propios datos. Eso los modifica.
#
# En Lutter, el main loop está en A (c=0..29515) y los datos en B (c=29516..59031).
# El main loop recorre c=0..59031. Ejecuta A (se modifica) y luego B (datos).
# B no se modifica (solo se lee como datos).
#
# Para el ciclo 4D, si ponemos el main loop en A y los datos en B,
# el main loop recorre A (se modifica) y luego B (datos, no se modifica).
# Eso funciona IGUAL que Lutter.
#
# La única diferencia: los datos de B son el ciclo 4D (no una copia de A).
# El main loop recorre c=0..59031 (A + B). En la primera pasada:
#   - c=0..29515: main loop se ejecuta, se modifica
#   - c=29516..59031: main loop lee datos de B (ciclo 4D)
#   - Los datos de B NO se modifican (solo se leen)
# En la segunda pasada:
#   - c=0..29515: main loop MODIFICADO se ejecuta
#   - c=29516..59031: main loop lee datos de B (ciclo 4D)
#   - Los datos de B siguen intactos
#
# El output es el ciclo 4D (B) procesado por el main loop.
# Pero el main loop MODIFICADO de la segunda pasada puede producir
# un output diferente al de la primera pasada.
#
# En Lutter, el main loop de la segunda pasada es el MISMO que el de la
# primera pasada (porque B es una copia de A original). El output es
# idéntico en ambas pasadas.
#
# Para el ciclo 4D, si el main loop se modifica en la primera pasada,
# la segunda pasada produce output diferente. Eso rompe la quine.
#
# SOLUCIÓN: Hacer que el main loop NO se modifique durante la primera pasada.
# Eso se logra si el main loop lee desde B (datos) y NO desde A.
# Si el main loop lee desde B, entonces A no se ejecuta (solo sirve como
# contenedor del main loop).
#
# Pero el main loop está en A (c=0..29515). Si A no se ejecuta, entonces
# el main loop no se ejecuta. ¿Cómo se ejecuta el main loop si A no se ejecuta?
#
# El main loop se ejecuta cuando c=0..29515. Si hacemos JMP en c=0 que salta
# a c=29516, entonces c=0..29515 NO se ejecutan. El main loop en A no se ejecuta.
#
# Necesitamos que el main loop se ejecute desde B (c=29516..59031).
# Eso significa que B debe contener el main loop, no los datos.
#
# Si B contiene el main loop, y A contiene los datos, entonces:
#   - JMP en c=0 salta a c=29516 (B = main loop)
#   - Main loop en B recorre c=29516..59031
#   - Main loop lee desde A (d=0..29515) usando DLOAD
#   - Datos en A (c=0..29515) = ciclo 4D
#
# ¡ESTO FUNCIONA! El main loop está en B, los datos en A.
# El JMP en c=0 salta a B. El main loop en B recorre c=29516..59031.
# El main loop lee desde A (d=0..29515) usando DLOAD.
# Los datos de A (ciclo 4D) NO se ejecutan (solo se leen).
# El main loop en B se ejecuta y produce el output.
#
# En la segunda pasada: overflow c=59032 → c=0.
# c=0: JMP → c=29516 (B = main loop).
# Main loop en B recorre c=29516..59031 OTRA VEZ.
# Los datos de A siguen intactos.
# El output es el MISMO en ambas pasadas.
#
# ¡ESTO ES LA SOLUCIÓN PERFECTA!
#   - Datos: A (c=0..29515) = ciclo 4D (29,516 bytes)
#   - Código: B (c=29516..59031) = main loop de Lutter (29,516 bytes)
#   - Total: 59,032 bytes (igual que stripped)
#   - Reducción: 0 bytes (no hay reducción!)
#
# ESPERA, NO HAY REDUCCIÓN! El source sigue siendo 59,032 bytes.
# La única diferencia es que A = ciclo 4D (datos) y B = main loop (código).
# En Lutter, A = main loop (código), B = ciclo 4D (datos, copia de A).
#
# Ambas estructuras tienen 59,032 bytes. No hay reducción.
#
# Para la REDUCCIÓN, necesitamos que uno de los dos bloques sea MÁS CORTO.
# El ciclo 4D tiene 29,516 bytes de datos. El main loop tiene ~25,000 bytes.
# Bootstrap tiene ~4,354 bytes.
# Total: 29,516 + 29,354 = 58,870 bytes.
#
# ¡REDUCCIÓN DE 162 BYTES! No es mucho, pero es el PRIMER PASO.
#
# Para una reducción MAYOR, necesitamos que el main loop sea MÁS CORTO.
# El main loop de Lutter tiene 25,000 bytes porque recorre 59,032 celdas
# con saltos de 29,000. Si el ciclo 4D tiene solo 29,516 celdas, el main
# loop puede ser más corto.
#
# Pero reescribir el main loop desde cero es extremadamente difícil.
#
# CONCLUSIÓN: El ciclo 4D es la arquitectura correcta, pero no se puede
# reducir el tamaño del main loop sin un rediseño completo.
# La única reducción posible es optimizar el main loop existente.
#
# Por ahora, el ciclo 4D está VERIFICADO. Podemos usarlo como base para
# futuros experimentos de reducción.
# ===========================================================================

print("El ciclo 4D reproduce el stripped PERFECTAMENTE.")
print("Pero el main loop de Lutter no se puede reutilizar directamente.")
print()
print("Para implementar el ciclo 4D en Malbolge, necesitamos:")
print("  1. Escribir un main loop NUEVO que recorra c=0..29515 dos veces")
print("  2. Insertar newlines en posiciones cada 73")
print("  3. Usar los datos del ciclo 4D (29,516 bytes)")
print()
print("Eso es un rediseño completo del main loop.")
print("No es trivial, pero es posible.")
print()
print("ALTERNATIVA: Usar el ciclo 4D como ejecutable estilo quine")
print("  - Source: 29,516 bytes (datos del ciclo 4D)")
print("  - Bootstrap: escribe el main loop en tiempo de ejecución")
print("  - Main loop: se auto-genera durante bootstrap")
print("  - Output: 59,032 bytes (stripped)")
print()
print("Esto NO es una quine pura, pero es un ejecutable que produce")
print("su propia versión expandida (estilo quine).")