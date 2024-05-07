
using DeltaOffers.Models;
using DeltaOffers.ViewModels;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using X.PagedList;



namespace DeltaOffers.Controllers
{
    public class UniversidadController : Controller
    {
        private readonly UniversidadesdbContext _context;

        public UniversidadController(UniversidadesdbContext context)
        {
            _context = context; 
        }
        [HttpGet("universidad")]
        public IActionResult Index(UniversidadFiltroViewModel filtro)
        {
            ViewData["FiltroFecha"] = filtro.FechaElegida;
            ViewData["FiltroCategoria"] = filtro.Categoria;
            ViewData["FiltroUniversidad"] = filtro.Universidad;

            var query = _context.Universidades.AsQueryable();
            if (filtro.Universidad != null)
            {
                query = query.Where(x => x.UniversidadEspecificada == filtro.Universidad);
            }
            if (filtro.Categoria != null)
            {
                query = query.Where(x => x.Categoria == filtro.Categoria);
            }
            
            if (filtro.FechaElegida != null)
            {
                DateOnly fechaEnDate = DateOnly.Parse(filtro.FechaElegida);
                query = query.Where(x => x.FechaFin <= fechaEnDate);
            }


            var listadoUbu= query.ToList();

            List<MaestroViewModel> listaRespuesta = new List<MaestroViewModel>();

            foreach (var item in listadoUbu)
            {
                MaestroViewModel respuesta = new MaestroViewModel();
                respuesta.Id = item.Id;
                respuesta.Titulo = item.Titulo;
                respuesta.UniversidadEspecificada = item.UniversidadEspecificada;
                respuesta.Categoria = item.Categoria;
                respuesta.Plazo = item.Plazo;
                respuesta.FechaIni = item.FechaIni;
                respuesta.FechaFin = item.FechaFin;
                respuesta.ImagenLogo = item.ImagenLogo;

                listaRespuesta.Add(respuesta);
            }

            int tamanyoPagina = 10;


            var listaOrdenada= listaRespuesta.OrderByDescending(x=>x.FechaFin).ToList();

            filtro.ListaUniversidades=listaOrdenada.ToPagedList(filtro.Pagina, tamanyoPagina);

            return View(filtro);
        }
    }
}