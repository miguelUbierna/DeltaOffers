namespace DeltaOffers.ViewModels
{
    public class UvaViewModel
    {

        public int Id { get; set; }

        public string? Titulo { get; set; }

        public string? Plazo { get; set; }

        public string? UniversidadEspecificada { get; set; }

        public DateOnly? FechaIni { get; set; }

        public DateOnly? FechaFin { get; set; }

        public string? Categoria { get; set; }

        public string? Enlace { get; set; }

        public string? Tipo { get; set; }

        public string? Clasificacion { get; set; }

        public byte[]? ImagenLogo { get; set; }
    }
}
