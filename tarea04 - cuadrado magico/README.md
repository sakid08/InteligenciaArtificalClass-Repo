# Solución al cuadrado magico

## El problema lleva la solucion en la imagen
##  Solución

Se puede calcular el nuemero magico a alcanzar con la formula:
---
M = n (n ^ 2 +1 ) / 2

---

n = dimencion del cuadrado, ya se a 3x3 o 4x4

--- 

### Patron

Empiezas poniendo el numero 1 en el cuadrito del centro de la fila de arriba. Luego vas poniendo los numeros seguidos moviendote siempre en diagonal, o sea, un pasito pa’ arriba y otro a la derecha. Si al hacer eso te sales del tablero, no pasa nada, entras de nuevo por el lado contraro. Y si resulta que ese cuadrito ya estaba ocupado, entoncs lo que haces es poner el sigiente numero justito debajo del ultimo que escribiste.