using System.ComponentModel.DataAnnotations;
using X.PagedList;

namespace DeltaOffers.ViewModels
{
    public class UniversidadFiltroViewModel
    { 
        public string Universidad { get; set; }
        public string Categoria { get; set;}
        public string FechaElegida { get; set;}
        public int Pagina { get; set; } = 1;
        public IPagedList<MaestroViewModel> ListaUniversidades { get; set; }

    }
}
