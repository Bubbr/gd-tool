import gdmt
from gdmt import Level
import os
import logging

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
        f'\tCreador: {lvl.creator.name}\n'
        )
    print(
        'Datos del creador\n\n'
        f'\tNombre: {lvl.creator.name}\n'
        f'\tId: {lvl.creator.id}\n'
        f'\tSecret coins: {lvl.creator.secretCoins}\n'
        f'\tUser coins: {lvl.creator.userCoins}\n'
        f'\tStars: {lvl.creator.stars}\n'
        f'\tDiamonds: {lvl.creator.diamonds}\n'
        f'\tDemons: {lvl.creator.demons}\n'
        )
    lvl.saveAsJSON()

if __name__ == "__main__":
    print("secret:",gdmt.secret)
    try:
        main()
    except:
        print("\nAlgo salió mal, quizas el nivel no existe :/\n")
    
    while True:
        op = input("¿Intentar de nuevo?\n\t[1] Sí\n\t[2] No\n> ")
        if op == "1":
            os.system('cls')
            try:
                main()
            except:
                print("\nAlgo salió mal, quizas el nivel no existe :/\n")
        else:
            input('\n\tHasta la próxima! Gracias por usar GDMT.\n'
                  '\nPresione enter para salir...'
                  )
            break
        
