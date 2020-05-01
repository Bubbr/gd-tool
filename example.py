import gdmt
from gdmt import Level
import os

def main():
    print(
        '\n\tBienvenido a GDMT (Geometry Dash Multi-Tool) by Felis\n'
        'Documentación y codigo fuente disponible en https://github.com/Bubbr/gd-tool\n'
        )
    lvl = Level(byName=str(input("Nombre del nivel\n> ")))
    print(
        '\nDatos del nivel\n'
        f'\n\tNombre: {lvl.name}\n'
        f'\tId: {lvl.id}\n'
        f'\tCreador: {lvl.author.name}\n'
        )
    print(
        'Datos del creador\n\n'
        f'\tNombre: {lvl.author.name}\n'
        f'\tId: {lvl.author.id}\n'
        f'\tSecret coins: {lvl.author.secretCoins}\n'
        f'\tUser coins: {lvl.author.userCoins}\n'
        f'\tStars: {lvl.author.stars}\n'
        f'\tDiamonds: {lvl.author.diamonds}\n'
        f'\tDemons: {lvl.author.demons}\n'
        )

if __name__ == "__main__":
    print(f"secret: {gdmt.secret}")

    main()
    while True:
        op = input("¿Intentar de nuevo?\n\t[1] Sí\n\t[2] No\n> ")
        if op == 1:
            os.system('cls')
            main()
        else:
            input('\n\tHasta la próxima! Gracias por usar GDMT.\n'
                  '\nPresione enter para salir...'
                  )
            break
        
