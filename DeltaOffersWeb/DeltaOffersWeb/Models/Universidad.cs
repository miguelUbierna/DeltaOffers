using System;
using System.Collections.Generic;

namespace DeltaOffers.Models;

public partial class Universidad
{
    public int Id { get; set; }

    public string? Titulo { get; set; }

    public string? Plazo { get; set; }

    public string? UniversidadEspecificada { get; set; }

    public DateOnly? FechaIni { get; set; }

    public DateOnly? FechaFin { get; set; }

    public string? Categoria { get; set; }

    public string? Enlace { get; set; }

    public string? Descripcion { get; set; }

    public DateOnly? FechaPublic { get; set; }

    public string? Convocante { get; set; }

    public string? Destinatarios { get; set; }

    public string? Tipo { get; set; }

    public string? NombrePlaza { get; set; }

    public string? ConvocatoriaAsociada { get; set; }

    public string? Clasificacion { get; set; }

    public byte[]? ImagenLogo { get; set; }
}
