from __future__ import annotations

from django.db import models
from django.utils import timezone


class Autor(models.Model):
    """
    Representa a un autor/a.
    Requerido: nombre, email único, biografía opcional.
    """

    # TODO: implementar los campos del modelo
    # Ejemplo de campo:
    nombre = models.CharField(max_length=120)
    #
    # nombre   → CharField (max_length a elección)
    email    = models.EmailField (unique=True)
    biografia = models.TextField (blank=True)

    pass

    # Opcional: definir __str__ para que sea legible en el admin y en el shell
    def __str__(self) -> str:
         return self.nombre


class Categoria(models.Model):
    """
    Categoría temática de libros.
    Ejemplos: 'fantasía', 'ciencia ficción', 'historia'.
    """

    # TODO: implementar el campo nombre (unique=True)
    nombre = models.CharField(max_length=120,unique=True)
    

    def __str__(self) -> str:
         return self.nombre


class Libro(models.Model):
    """
    Libro del catálogo de la biblioteca.
    Tiene relación N:1 con Autor y N:M con Categoria.
    """

    # TODO: implementar los campos:
    titulo          = models.CharField(max_length=200)
    isbn            = models.CharField (unique=True)
    fecha_publicacion = models.DateField()
    cantidad_total  = models.PositiveIntegerField()
    autor           = models.ForeignKey(Autor, on_delete=models.PROTECT)
    categorias      = models.ManyToManyField(Categoria)
    #
    # Preguntas guía:
    # ¿Qué pasa si eliminás un autor que tiene libros? (PROTECT vs CASCADE)
    #no se puede eliminar  porque hay libros de dependen del autor
    # ¿Por qué isbn debe ser único?

    pass

    def prestamos_activos(self) -> int:
        """
        Retorna la cantidad de préstamos activos (fecha_devolucion IS NULL).

        Un préstamo es "activo" cuando no se ha registrado devolución.
        """
        # TODO: implementar con ORM usando filter sobre los préstamos relacionados
        return self.prestamo_set.filter(fecha_devolucion__isnull=True).count()
        #        (o el related_name que hayas definido en Prestamo.libro)
        
       

    def disponibles(self) -> int:
        """
        Retorna cuántas copias están disponibles:
        cantidad_total - prestamos_activos()
        """
        # TODO: implementar
        return self.cantidad_total - self.prestamos_activos()


    def tiene_disponibles(self) -> bool:
        """Retorna True si hay al menos una copia disponible."""
        # TODO: implementar
        return self.disponibles() >= 1
    
    def __str__(self) -> str:
         return self.titulo


class Prestamo(models.Model):
    """
    Registro de un préstamo de libro a un usuario.
    Si fecha_devolucion es NULL → el préstamo está activo.
    """

    # TODO: implementar los campos:
    libro              = models.ForeignKey(Libro, on_delete=models.CASCADE)
    nombre_prestatario = models.CharField(max_length=100)
    fecha_prestamo     = models.DateField(default=timezone.now) #de Django, conoce zonas horarias
    fecha_devolucion   = models.DateField (null=True, blank=True)
    #
    # Preguntas guía:
    # ¿Por qué usamos CASCADE aquí y PROTECT en Libro→Autor?
    #es cascade porque si elimino un libro no tiene sentido que existan prestamos asociados a este

    # ¿Qué valor por defecto tendría sentido para fecha_prestamo?
    #la fecha de hoy

    # Tip: podés usar default=timezone.now si querés fecha automática,
    #      o dejarlo sin default para que el test lo defina explícitamente.

    pass
