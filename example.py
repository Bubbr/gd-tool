from gdtool import Level

if __name__ == "__main__":
    print(
        '\n\tBienvenido a GDT (Geometry Dash Tool) by Felis\n'
        'Documentación y codigo fuente disponible en https://github.com/Bubbr/gd-tool\n'
        )
    lvl = Level(byName="Bloodbath")
    
    print(
        f'\n\tNombre: {lvl.name}\n'
        f'\tId: {lvl.id}\n'
        f'\tCreador: {lvl.author.name}\n'
        )
